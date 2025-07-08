"""Declarative programming utilities."""
from __future__ import annotations

from typing import Any, Dict


REGISTRY: Dict[Any, Dict[str, Any]] = {}


def declare(**kwargs: Any):
    """Decorator to attach declarative metadata."""
    def decorator(obj: Any) -> Any:
        REGISTRY[obj] = kwargs
        return obj
    return decorator


def get_declaration(obj: Any) -> Dict[str, Any] | None:
    return REGISTRY.get(obj)


if __name__ == "__main__":
    @declare(role='service', version=1)
    class Service:
        pass

    print(get_declaration(Service))
