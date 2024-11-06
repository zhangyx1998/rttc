from . import Test
from type_check import type_check

# Union types are also supported
Test(type_check, [[1, 2], [3.0, 4.0]], list[list[int] | list[float]]) >> True
Test(type_check, [[1, 2.0], [3, 4.0]], list[list[int] | list[float]]) >> False
