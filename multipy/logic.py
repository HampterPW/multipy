"""Mini Prolog-like logic programming utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Generator, Iterable, List, Tuple

FACTS: List[Tuple[str, Tuple[Any, ...]]] = []
RULES: List[Tuple[Tuple[str, ...], List[Tuple[str, ...]]]] = []


def fact(predicate: str, *args: Any):
    """Decorator to register a fact."""
    def decorator(func):
        FACTS.append((predicate, args))
        return func
    return decorator


def rule(head: Tuple[str, ...], *body: Tuple[str, ...]):
    """Decorator to register a rule."""
    def decorator(func):
        RULES.append((head, list(body)))
        return func
    return decorator


@dataclass
class Goal:
    pred: str
    args: Tuple[Any, ...]


def is_var(x: Any) -> bool:
    return isinstance(x, str) and x.startswith("?")


def unify(pattern: Iterable[Any], fact: Iterable[Any], env: Dict[str, Any]) -> Dict[str, Any] | None:
    env = dict(env)

    def deref(x: Any) -> Any:
        while is_var(x) and x in env and env[x] != x:
            x = env[x]
        return x

    for p, f in zip(pattern, fact):
        p_val = deref(p)
        f_val = deref(f)
        if is_var(p_val):
            env[p_val] = f_val
        elif is_var(f_val):
            env[f_val] = p_val
        elif p_val != f_val:
            return None
    return env


def deref_env(env: Dict[str, Any]) -> Dict[str, Any]:
    """Resolve variables to their concrete values."""
    def deref(x: Any) -> Any:
        while is_var(x) and x in env and env[x] != x:
            x = env[x]
        return x

    return {k: deref(v) for k, v in env.items()}


def resolve(goal: Goal, env: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    for pred, args in FACTS:
        if pred != goal.pred:
            continue
        new_env = unify(goal.args, args, env)
        if new_env is not None:
            yield new_env
    for head, body in RULES:
        if head[0] != goal.pred:
            continue
        new_env = unify(goal.args, head[1:], env)
        if new_env is None:
            continue
        yield from resolve_body([Goal(b[0], b[1:]) for b in body], new_env)


def resolve_body(goals: List[Goal], env: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
    if not goals:
        yield deref_env(env)
        return
    first, rest = goals[0], goals[1:]
    for env2 in resolve(first, env):
        yield from resolve_body(rest, env2)


def query(predicate: str, *args: Any) -> Generator[Dict[str, Any], None, None]:
    """Query the knowledge base."""
    return resolve(Goal(predicate, args), {})


if __name__ == "__main__":
    @fact('parent', 'alice', 'bob')
    def _():
        pass

    @fact('parent', 'bob', 'carol')
    def _():
        pass

    @rule(('grandparent', '?x', '?z'), ('parent', '?x', '?y'), ('parent', '?y', '?z'))
    def _():
        pass

    for solution in query('grandparent', 'alice', '?who'):
        print('grandparent:', solution['?who'])
