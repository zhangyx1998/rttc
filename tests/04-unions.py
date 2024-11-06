from . import Test, type_check

# Union types are also supported
Test(type_check, [[1, 2], ["3", "4"]], list[list[int] | list[str]]) >> True
Test(type_check, [[1, "2"], [3, "4"]], list[list[int] | list[float]]) >> False
