"""Functional programming utilities."""
from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Iterable, Tuple


def pipe(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Apply functions left-to-right."""
    def _pipe(value: Any) -> Any:
        for func in funcs:
            value = func(value)
        return value
    return _pipe


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose functions right-to-left."""
    def _compose(value: Any) -> Any:
        for func in reversed(funcs):
            value = func(value)
        return value
    return _compose


def curry(func: Callable[..., Any]) -> Callable[..., Any]:
    """Transform a function into its curried form."""
    @wraps(func)
    def _curried(*args: Any) -> Any:
        if len(args) >= func.__code__.co_argcount:
            return func(*args)
        return lambda *more: _curried(*args, *more)
    return _curried


def pure(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to assert a function has no side effects on globals."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        before = dict(globals())
        result = func(*args, **kwargs)
        after = dict(globals())
        for key in before:
            if before[key] != after.get(key):
                raise RuntimeError(f"Side effect detected on global '{key}'")
        return result
    return wrapper


def rec(func: Callable[..., Any]) -> Callable[..., Any]:
    """Tail recursion optimization decorator."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        call = func
        while True:
            result = call(*args, **kwargs)
            if isinstance(result, Tuple) and result and result[0] is wrapper:
                _, args, kwargs = result
                continue
            return result
    return wrapper


def match(value: Any, patterns: Iterable[Tuple[Any, Callable[[Any], Any]]]) -> Any:
    """Pattern matching utility."""
    for pattern, action in patterns:
        if callable(pattern) and pattern(value):
            return action(value)
        if pattern == value:
            return action(value)
    raise ValueError("No pattern matched")


if __name__ == "__main__":
    def double(x: int) -> int:
        return x * 2

    def increment(x: int) -> int:
        return x + 1

    pipeline = pipe(double, increment)
    print("pipe:", pipeline(3))  # 7

    composed = compose(increment, double)
    print("compose:", composed(3))  # 8

    @curry
    def add(a: int, b: int, c: int) -> int:
        return a + b + c

    add1 = add(1)
    print("curry:", add1(2)(3))  # 6

    @pure
    def pure_add(a: int, b: int) -> int:
        return a + b

    print("pure:", pure_add(2, 4))

    @rec
    def factorial(n: int, acc: int = 1) -> Any:
        if n == 0:
            return acc
        return factorial, (n - 1, acc * n), {}

    print("rec:", factorial(5))

    result = match(3, [
        (1, lambda _: "one"),
        (lambda x: x > 2, lambda _: "greater than two"),
    ])
    print("match:", result)
