# Type guard tests
from . import Test
from src.type_check import type_guard

@type_guard
class C(list[int]):
    pass

Test(C, [1, 2, 3]) >> True
Test(C, [1, 2, 0.0]) >> False

from dataclasses import dataclass

@type_guard
@dataclass
class C:
    x: int
    y: float


Test(C, x=1, y=2.0) >> True
Test(C, x=1.0, y=2) >> False

@type_guard
def add(x: int | str, y: int | str) -> int | str:
    return x + y

Test(add, 1, 2) >> True
Test(add, '1', '2') >> True
Test(add, [1], [2]) >> False
