from dataclasses import dataclass

def type_repr(t: type) -> str:
    if type(t) is type and hasattr(t, "__name__"):
        return t.__name__
    else:
        return str(t).removeprefix('typing.')


class Chain(list["str | Chain.Attr | Chain.Key"]):
    def enter(self, el: "str | Attr | Key"):
        return self.__class__(self + [el])

    @dataclass
    class Key:
        key: str | int | float | bool | None

        def __str__(self) -> str:
            return f"[{repr(self.key)}]"

    @dataclass
    class Attr:
        attr: str

        def __str__(self) -> str:
            return f".{str(self.attr)}"


class TypeCheckError(TypeError):
    value: object
    type_to_check: type

    def __init__(self, chain: Chain, expected: list[type], got: object):
        desc = "".join(map(str, chain))
        _exp = " | ".join((type_repr(t) for t in expected))
        _got = f"{type(got).__name__}({repr(got)})"
        if len(chain) > 1:
            super().__init__(f"{desc} = {_got} is not {_exp}")
        else:
            super().__init__(f"{_got} is not {_exp}")


@dataclass
class TypeCheckResult:
    value: object
    type_to_check: type

    passed: bool
    reason: str | None

    def __bool__(self) -> bool:
        return self.passed

    def __repr__(self) -> str:
        return f"{repr(self.value)} is {type_repr(self.type_to_check)} => {self.passed}"

    def __eq__(self, value):
        return bool(self) == value

    def __neq__(self, value):
        return bool(self) != value

    def __str__(self) -> str:
        if self.reason is not None:
            return str(self.reason)
        else:
            return "Type check passed" if self.passed else "Type check failed"
