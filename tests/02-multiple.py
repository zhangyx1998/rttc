from . import Test, type_check

# List
Test(type_check, [1, "2", 3.0], list[int, str, float]) >> True
Test(type_check, [1, "2", "3"], list[int, str, float]) >> False
Test(type_check, [1, "2"], list[int, str, float]) >> False

# Tuple
Test(type_check, (1, "2", 3.0), tuple[int, str, float]) >> True
Test(type_check, (1, "2", "3"), tuple[int, str, float]) >> False

# Set
Test(type_check, {1, "2", 3.0}, set[int | str | float]) >> True
Test(type_check, {1, "2", None}, set[int | str | float]) >> False

# Dict
Test(type_check, {1: "2", 3: 4.0}, dict[int, str | float]) >> True
Test(type_check, {1: "2", "3": 4.0}, dict[int, str | float]) >> False # key type mismatch
Test(type_check, {1: "2", 3: None}, dict[int, str | float]) >> False # value type mismatch
