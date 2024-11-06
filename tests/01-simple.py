from . import Test, type_check

# Simple Examples
Test(type_check, 1, int) >> True
Test(type_check, "", int) >> False

Test(type_check, [1, 2, 3], list[int]) >> True
Test(type_check, [1, 2, ""], list[int]) >> False

# Literals
from typing import Literal
Test(type_check, 1, Literal[1]) >> True
Test(type_check, 2, Literal[1]) >> False
Test(type_check, "alex", Literal["alex", "bob"]) >> True
Test(type_check, "alex", Literal["bob"]) >> False
