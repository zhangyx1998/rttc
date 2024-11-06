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


@dataclass
class B(Generic[T, P]):
    x: T
    y: P

Test(type_check, B(x=1, y="2"), B[int, str]) >> True
Test(type_check, B(x=1, y=2.0), B[int, str]) >> False
