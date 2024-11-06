## Python run-time type checking utility

Author: [Yuxuan Zhang](mailto:python@z-yx.cc) | [GitHub Repository](https://github.com/zhangyx1998/rttc)

The `rttc` project originates from this [post](https://discuss.python.org/t/runtime-type-checking-using-parameterized-types/70173) on the python discussion forum.

### Usage

#### Want to do something like this?

```python
>>> isinstance(["hello type check"], list[str])
TypeError: isinstance() argument 2 cannot be a parameterized generic
```

#### Just drop-in replace `isinstance()` with `type_check()`

```python
from type_check import type_check

type_check(["hello type check"], list[str]) # True
type_check([1], list[str]) # False
```

And of course you can use type variables!

```
DataType = list[tuple[float, str]]

type_check([(1.0, "hello rttc")], DataType) # True
type_check([(1, 2), [3.0, "4"]] , DataType) # False
```

#### Wondering how far you can go?

These features all work recursively with each other!

- **Union types** are supported:

    ```python
    type_check(1   , int | bool) # True
    type_check(True, int | bool) # True
    type_check("1" , int | bool) # False
    ```

- **Literals** are supported:

    ```python
    type_check("alex", Literal["alex", "bob"]) # True
    type_check("hack", Literal["alex", "bob"]) # False
    ```

- **Inherited classes** are supported:

    ```python
    class C(list[int]):
        pass

    type_check(C([1])  , C) # True
    type_check(C([1.0]), C) # False
    ```

- **Type-hinted classes** are supported:

    ```python
    from typing import TypeVar, Generic, Literal
    from dataclasses import dataclass

    T = TypeVar("T")
    P = TypeVar("P")

    @dataclass
    class C(Generic[T, P]):
        x: T
        y: P
        z: Literal[1]

    type_check(C(x=1  , y="y", z=1), C[int, str]) # True
    type_check(C(x=1.0, y="y", z=1), C[int, str]) # False - C.x = float(1.0) is not int
    type_check(C(x=1  , y="y", z=2), C[int, str]) # False - C.z = int(2) is not Literal[1]
    ```


- **Custom checking hooks**:

    Examples coming soon...

    For now, please refer to [type_check/builtin_checks.py](https://github.com/zhangyx1998/rttc/blob/master/type_check/builtin_checks.py).

### Other tools in the box

### `type_assert()`

Similar to type_check(), but it raises `TypeCheckError` instead of returns `bool`.
The raised `TypeCheckError` contains debug-friendly information indicating what caused type check to fail (check below for details).

### `type_guard`

This decorator allows you to convert a class or a function into a type-guarded object.
It is analogous to performing a `type_assert` on function return values or on returned class instances.

```python
from type_check import type_guard

@type_guard
def fn(x) -> int | float | str:
    return x

fn(1) # ok

fn([]) # TypeCheckError: list([]) is not int | float | str

from dataclasses import dataclass

@type_guard
@dataclass
class A:
    x: int

A(x=1) # ok
A(x=1.0) # TypeCheckError: A.x = float(1.0) is not int
```

Since `1.0.4`, the following is made possible:

```python
@type_guard
@dataclass
class B:
    x: int

B[int](x=1)   # ok
B[int](x=1.0) # TypeCheckError: A.x = float(1.0) is not int
B[float](x=1) # TypeCheckError: A.x = int(1) is not float
```

### Info-rich return values and exceptions

### `TypeCheckResult`

`TypeCheckResult` is the return type of `type_check()` function.
It can be used directly as a `bool` or compared with a `bool`.

For example:

```python
from type_check import type_check

result = type_check([1], list[int])

print(bool(result), result == True, result == False)
# True, True, False
print(str(result))
# [1] is list[int] => True
print(repr(result))
# type_check([1] is list[int] => True)
```

And when a result evaluates to `False`, you can use `TypeCheckResult.reason` to know why:

```python
result = type_check(["1"], list[int])

print(result)
# ['1'] is list[int] => False
print(result.reason)
# list[0] = str('1') is not int
```

### `TypeCheckError`

`TypeCheckError` is inherited from `TypeError`, it will be raised by `type_assert()` and `@type_guard` when type check fails.

It contains chained attributes and keys to help you locate the data that cause type check to fail:

```python
from type_check import type_assert

type_assert([1, 2, '3', 4], list[int])
```

Will raise:

```
TypeCheckError                            Traceback (most recent call last)
Cell In[47], line 10
    6 print(result.reason)
    8 from type_check import type_assert
---> 10 type_assert([1, 2, "3", 4], list[int])

File rttc/type_check/core.py:45, in type_assert(obj, t, chain)
    43     # Clear traceback to avoid confusion
    44     type_check_error = e.with_traceback(None)
---> 45     raise type_check_error
    46 except TypeError as e:
    47     type_error = e.with_traceback(None)

TypeCheckError: list[2] = str('3') is not int
```

### Testing

Test cases live under `tests/` and are grouped by categories. Test results are available at [docs/test-results.txt](https://github.com/zhangyx1998/rttc/blob/master/docs/test-results.txt). _PRs to add more test cases to it will be deeply appreciated._

#### Instructions to run tests locally

```sh
git clone git@github.com:zhangyx1998/rttc.git

cd rttc && python3 -m pip install -r tests/requirements.txt # termcolor

python3 -m tests
```

#### Testing against well-known library `typeguard`:

```sh
pip3 install typeguard

TARGET=typegurad python3 -m tests
```
