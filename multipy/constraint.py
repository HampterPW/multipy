"""Simple constraint programming utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List


@dataclass
class Variable:
    name: str
    domain: Iterable[Any]


class Solver:
    """Backtracking constraint solver."""

    def __init__(self, variables: List[Variable]):
        self.variables = variables
        self.constraints: List[Callable[[Dict[str, Any]], bool]] = []

    def add_constraint(self, constraint: Callable[[Dict[str, Any]], bool]) -> None:
        self.constraints.append(constraint)

    def solve(self) -> List[Dict[str, Any]]:
        solutions: List[Dict[str, Any]] = []

        def backtrack(env: Dict[str, Any], index: int) -> None:
            if index == len(self.variables):
                if all(c(env) for c in self.constraints):
                    solutions.append(env.copy())
                return
            var = self.variables[index]
            for value in var.domain:
                env[var.name] = value
                if all(c(env) for c in self.constraints if set(env).issuperset(c.__code__.co_varnames)):
                    backtrack(env, index + 1)
                env.pop(var.name)

        backtrack({}, 0)
        return solutions


if __name__ == "__main__":
    x = Variable('x', range(5))
    y = Variable('y', range(5))

    solver = Solver([x, y])
    solver.add_constraint(lambda env: env['x'] + env['y'] == 4)

    for sol in solver.solve():
        print(sol)
