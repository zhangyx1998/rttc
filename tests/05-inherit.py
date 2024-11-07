from . import Test, type_check


# Custom class type checking
class A(list[int]):
    pass


Test(type_check, A([1, 2, 3]), A) >> True
Test(type_check, A([1, 2, 0.0]), A) >> False


from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")
P = TypeVar("P")
V = TypeVar("V")


@dataclass
class B(Generic[T, P]):
    x: T
    y: P


Test(type_check, B(x=1, y="2"), B[int, str]) >> True
Test(type_check, B(x=1, y=2.0), B[int, str]) >> False
# Since 1.0.6 - 2nd argument can be omitted
Test(type_check, B[int, str](x=1, y="2")) >> True
Test(type_check, B[int, str](x=1, y=2.0)) >> False


@dataclass
class C(B[T, P], Generic[T, P, V]):
    z: V


Test(type_check, C(x=1, y="2", z=False), C[int, str, bool]) >> True
Test(type_check, C(x=1, y=2.0, z=False), C[int, str, bool]) >> False
Test(type_check, C(x=1, y="2", z=None), C[int, str, bool]) >> False
# Since 1.0.6 - 2nd argument can be omitted
Test(type_check, C[int, str, bool](x=1, y="2", z=False)) >> True
Test(type_check, C[int, str, bool](x=1, y=2.0, z=False)) >> False
Test(type_check, C[int, str, bool](x=1, y="2", z=None)) >> False
