from . import Test
from src.type_check import type_check

# Recursive type checking is automatically supported
Test(type_check, [[1, 2], [3, 4]], list[list[int]]) >> True
Test(type_check, [[1, 2], [3, "4"]], list[list[int]]) >> False
