from typing import Union, Callable, NoReturn, Literal, TypeVar
from typing import get_args, get_origin, get_type_hints
from typing_extensions import Unpack
from types import UnionType
from functools import wraps

from .primitives import Chain, TypeCheckError, TypeCheckResult

# By default, raise TypeError (not TypeCheckError) upon encountering objects that
# do not support type check (i.e. with no __type_check__ method and no type hints)
# Otherwise, type check will skip type check on items that do not support type_check
STRICT = True

# If True, type check will raise TypeCheckError upon missing attribute
# i.e. an attribute declared in type hint but not present in object
CHECK_MISSING_ATTR = False

# Returns None on success, raises TypeError or TypeCheckError on failure
TypeChecker = Callable[[object, Unpack[list[type]]], None | NoReturn]
builtin_checks = dict[type, TypeChecker]()


def type_check(obj, t: type) -> bool:
    try:
        type_assert(obj, t)
        return TypeCheckResult(obj, t, passed=True, reason=None)
    except TypeCheckError as e:
        return TypeCheckResult(obj, t, passed=False, reason=str(e))
    except TypeError as e:
        type_error = e.with_traceback(None)
        raise type_error


def type_assert(obj, t: type, *, chain: Chain | None = None) -> None | NoReturn:
    if chain is None:
        chain = Chain(type(obj).__name__)
    try:
        __type_assert__(obj, t, chain=chain)
    except TypeCheckError as e:
        # Attach the original object to exception
        setattr(e, "value", obj)
        setattr(e, "type_to_check", t)
        # Clear traceback to avoid confusion
        type_check_error = e.with_traceback(None)
        raise type_check_error
    except TypeError as e:
        type_error = e.with_traceback(None)
        raise type_error


def __type_assert__(obj, t: type, *, chain: Chain) -> None | NoReturn:
    origin, args = get_origin(t), get_args(t)
    if origin is None:
        # t is not a generic type, fallback to direct type check
        if not isinstance(obj, t):
            raise TypeCheckError(chain, [t], obj)
        # Check for python primitive types (int, str, float, etc.)
        if t in (int, str, float, bool, None, type(None)):
            return
        # Python classes
        if type(t) is type:
            if hasattr(t, "__orig_bases__"):
                # Try to retrieve the inheritance chain
                for orig in t.__orig_bases__:
                    __type_assert__(obj, orig, chain=chain)
        origin = t

    if origin is UnionType or origin is Union:
        # Union type, check if any of the types match
        for arg in args:
            try:
                return __type_assert__(obj, arg, chain=chain)
            except TypeCheckError:
                continue
        raise TypeCheckError(chain, args, obj)

    if origin is Literal:
        # Literal type, check if obj is one of the literals
        if obj not in args:
            raise TypeCheckError(chain, [t], obj)
        return

    if not isinstance(obj, origin):
        # Origin type mismatch
        raise TypeCheckError(chain, [origin], obj)

    try:
        # Use custom type checker whenever possible
        if hasattr(origin, "__type_check__"):
            return origin.__type_check__(obj, *args, chain=chain)
        if hasattr(obj, "__type_check__"):
            return obj.__type_check__(*args, chain=chain)
    except TypeError:
        bad_checker = repr(origin.__type_check__)
        raise TypeError(f"Type checker {bad_checker} not implemented correctly")

    # No custom type checker, try match with builtin type checkers
    if origin in builtin_checks:
        return builtin_checks[origin](obj, *args, chain=chain)

    # Try to fallback to type hints
    parameters = getattr(origin, "__parameters__", tuple())
    if len(parameters) == len(args): # Fully parameterized
        try:
            hints: dict[str, TypeVar | type] = get_type_hints(obj)
        except:  # No type hints available in user defined class
            return
        templates = dict(zip(parameters, args))
        for attr, hint in hints.items():
            if not hasattr(obj, attr):
                if CHECK_MISSING_ATTR:
                    raise TypeCheckError(chain, [t], obj)
                else:
                    continue
            else:
                item = getattr(obj, attr)
            if isinstance(hint, TypeVar):
                if hint in templates:
                    hint = templates[hint]
                else:
                    raise TypeError(f"Type variable {hint} not instantiated")
            __type_assert__(item, hint, chain=chain(Chain.Attr(attr)))
        return
    else:  # Partially parameterized, wait for full parameterization
        return


def type_guard(t: type):
    """
    ## Decorate classes or functions to enforce type checking

    ### Usage:

    1. Decorating classes - do not use parentheses
    ```
    @type_guard
    class C(list[int]):
        pass
    ```

    2. Decorating functions - use type annotation pass type hint
    ```
    @type_guard
    def f(x) -> list[int]:
        return x
    ```

    3. Decorating functions - (alterative) use parenthesis to pass type hint
    ```
    @type_guard(list[int])
    def f(x):
        return x
    ```
    """
    if isinstance(t, type):  # class decorator

        from .transparent import Transparent

        class TypeGuard(Transparent, t):
            def __call__(self, *args, **kwargs):
                result = super().__call__(*args, **kwargs)
                type_assert(result, t)
                if hasattr(result, "__orig_class__"):
                    type_assert(result, result.__orig_class__)
                return result

            def __repr__(self):
                return f"TypeGuard({t.__repr__(self)})"

        return TypeGuard(t)

    elif callable(t):  # annotated function
        import inspect

        spec = inspect.getfullargspec(t)
        if not "return" in spec.annotations:
            raise TypeError("Type guarded function missing return type hint")

        return_type = spec.annotations["return"]

        def wrapper(*args, **kwargs):
            result = t(*args, **kwargs)
            try:
                type_assert(result, return_type)
            except TypeCheckError as e:
                type_check_error = e.with_traceback(None)
                raise type_check_error
            return result

        return wraps(t)(wrapper)

    else:
        raise TypeError(f"{repr(t)} is neither a class nor a function")
