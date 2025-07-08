"""Reactive programming utilities."""
from __future__ import annotations

from typing import Any, Callable, List


class Signal:
    """Simple reactive signal."""

    def __init__(self, value: Any = None):
        self._value = value
        self._subscribers: List[Callable[[Any], Any]] = []

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new: Any) -> None:
        self._value = new
        for sub in list(self._subscribers):
            sub(new)

    def subscribe(self, func: Callable[[Any], Any]) -> None:
        self._subscribers.append(func)

    def map(self, func: Callable[[Any], Any]) -> 'Signal':
        result = Signal(func(self._value))

        def update(val: Any) -> None:
            result.value = func(val)

        self.subscribe(update)
        return result

    def filter(self, predicate: Callable[[Any], bool]) -> 'Signal':
        result = Signal(self._value if predicate(self._value) else None)

        def update(val: Any) -> None:
            if predicate(val):
                result.value = val

        self.subscribe(update)
        return result


if __name__ == "__main__":
    s = Signal(1)
    doubled = s.map(lambda x: x * 2)
    filtered = doubled.filter(lambda x: x > 2)
    filtered.subscribe(lambda v: print('filtered value', v))

    for i in range(4):
        s.value = i
