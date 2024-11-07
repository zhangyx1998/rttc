# Type guard tests
from . import Test, type_guard


@type_guard
class A(list[int]):
    pass


Test(A, [1, 2, 3]) >> True
Test(A, [1, 2, "3"]) >> False

from dataclasses import dataclass


@type_guard
@dataclass
class B:
    x: int
    y: str


Test(B, x=1, y="2") >> True
Test(B, x="1", y=2) >> False


from typing import TypeVar, Generic

T = TypeVar("T")


@type_guard
@dataclass
class C(Generic[T]):
    x: T


Test(C[int], x=1) >> True
Test(C[int], x="1") >> False

ValType = int | str | list[int] | list[str]


@type_guard
def add(x: ValType, y: ValType) -> ValType:
    return x + y


Test(add, 1, 2) >> True
Test(add, "1", "2") >> True
Test(add, [], []) >> True
Test(add, [1], [2]) >> True
Test(add, ["1"], ["2"]) >> True
Test(add, [None], []) >> False
Test(add, (), ()) >> False
