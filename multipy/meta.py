"""Metaprogramming utilities."""
from __future__ import annotations

import ast
import inspect
import textwrap
from typing import Any, Callable


def auto_repr(cls: type) -> type:
    """Class decorator to automatically generate __repr__."""
    def __repr__(self) -> str:
        attrs = ', '.join(f"{name}={getattr(self, name)!r}" for name in vars(self))
        return f"{self.__class__.__name__}({attrs})"

    cls.__repr__ = __repr__
    return cls


def auto_eq(cls: type) -> type:
    """Class decorator to automatically generate __eq__."""
    def __eq__(self, other: Any) -> bool:
        if self.__class__ is not other.__class__:
            return False
        return vars(self) == vars(other)

    cls.__eq__ = __eq__
    return cls


def transform_ast(func: Callable[..., Any], transformer: Callable[[ast.AST], ast.AST]) -> Callable[..., Any]:
    """Transform a function's AST at runtime."""
    source = textwrap.dedent(inspect.getsource(func))
    tree = ast.parse(source)
    tree = transformer(tree)
    code = compile(tree, filename=inspect.getsourcefile(func) or "<ast>", mode="exec")
    namespace: dict[str, Any] = {}
    exec(code, func.__globals__, namespace)
    return namespace[func.__name__]


if __name__ == "__main__":
    @auto_repr
    @auto_eq
    class Point:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    p1 = Point(1, 2)
    p2 = Point(1, 2)
    print("repr:", repr(p1))
    print("eq:", p1 == p2)

    def add(a: int, b: int) -> int:
        return a + b

    def transformer(tree: ast.AST) -> ast.AST:
        for node in ast.walk(tree):
            if isinstance(node, ast.Return) and isinstance(node.value, ast.BinOp):
                node.value = ast.BinOp(node.value.left, ast.Mult(), node.value.right)
                ast.fix_missing_locations(node)
        return ast.fix_missing_locations(tree)

    new_add = transform_ast(add, transformer)
    print("transform_ast:", new_add(2, 3))  # should multiply
