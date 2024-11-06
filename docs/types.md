### `TypeCheckResult`

`TypeCheckResult` is the return type of `type_check()` function.

It can be used directly as a `bool` or compared with a `bool`.

For example:

```python
from type_check import type_check

result = type_check([1], list[int])

print(bool(result), result == True, result == False)
# True, True, False

print(str(result))
# [1] is list[int] => True

print(repr(result))
# type_check([1] is list[int] => True)
```

### `TypeCheckError`

`TypeCheckError` is inherited from `TypeError`, it is the expected exception raised by `type_assert()` and `@type_guard`.

