from .primitives import Chain, TypeCheckError
from .core import builtin_checks, type_assert

# Checkers for builtin types
from typing import Sequence, Any


def sequence_check(seq: Sequence, *args: type, chain: Chain) -> bool:
    if len(args) == 0:
        # No type hint, anything is allowed
        pass
    elif len(args) == 1:
        # Single type hint, all elements must be of this type
        typ = args[0]
        for i, el in enumerate(seq):
            type_assert(el, typ, chain=chain(Chain.Key(i)))
    elif len(args) == len(seq):
        # Type check each item with corresponding type hint
        for i, (el, typ) in enumerate(zip(seq, args)):
            type_assert(el, typ, chain=chain(Chain.Key(i)))
    else:
        # Number of items mismatches with number of type hints
        raise TypeCheckError(chain, [type(seq)[args]], seq)


builtin_checks[list] = sequence_check
builtin_checks[tuple] = sequence_check
builtin_checks[Sequence] = sequence_check

def set_check(s: set, typ: type, *, chain: Chain) -> bool:
    for el in s:
        type_assert(el, typ, chain=chain("[?]"))

builtin_checks[set] = set_check


def dict_check(d: dict, key_type: type, value_type: type=Any, *, chain: Chain) -> bool:
    for key, val in d.items():
        type_assert(key, key_type, chain=chain("<key>"))
        type_assert(val, value_type, chain=chain(Chain.Key(key)))

builtin_checks[dict] = dict_check


def no_check(item, *args: type, chain: Chain) -> bool:
    raise TypeError(f"Type check on {repr(item)} is potentially destructive")


from typing import Iterable
builtin_checks[Iterable] = no_check
builtin_checks[frozenset] = no_check
