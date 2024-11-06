# Type guard tests
from . import Test
from type_check import type_guard

@type_guard
class A(list[int]):
    pass

Test(A, [1, 2, 3]) >> True
Test(A, [1, 2, 0.0]) >> False

from dataclasses import dataclass

@type_guard
@dataclass
class B:
    x: int
    y: float


Test(B, x=1, y=2.0) >> True
Test(B, x=1.0, y=2) >> False


from typing import TypeVar, Generic

T = TypeVar("T")

@type_guard
@dataclass
class C(Generic[T]):
    x: T


# Test(C[int], x=1) >> True
# Test(C[int], x=1.0) >> False


@type_guard
def add(x: int | str, y: int | str) -> int | str:
    return x + y

Test(add, 1, 2) >> True
Test(add, '1', '2') >> True
Test(add, [1], [2]) >> False
