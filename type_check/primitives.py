from dataclasses import dataclass
from typing import _type_repr as type_repr


class Chain:
    def __init__(self, item: "str | Chain.Attr | Chain.Key", parent: "Chain" = None):
        self.value = item
        self.parent = parent

    def __call__(self, el: "str | Attr | Key"):
        return self.__class__(el, parent=self)
    
    def __iter__(self):
        if self.parent is not None:
            yield from self.parent
        yield self.value

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
        _exp = " | ".join((type_repr(t) for t in expected))
        _got = f"{type(got).__name__}({repr(got)})"
        if chain.parent is None:
            super().__init__(f"{_got} is not {_exp}")
        else:
            desc = "".join(map(str, chain))
            super().__init__(f"{desc} = {_got} is not {_exp}")
    
    @property
    def result(self):
        return TypeCheckResult(self.value, self.type_to_check, False, str(self))


@dataclass
class TypeCheckResult:
    value: object
    type_to_check: type

    passed: bool
    reason: str | None

    def __str__(self) -> str:
        return f"{repr(self.value)} is {type_repr(self.type_to_check)} => {self.passed}"

    def __repr__(self) -> str:
        return f"type_check({self})"

    def __bool__(self) -> bool:
        return self.passed

    def __eq__(self, value):
        return bool(self) == value

    def __neq__(self, value):
        return bool(self) != value
