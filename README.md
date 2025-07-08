# Multipy

Multipy is a multi-paradigm programming toolkit for Python 3.10+. It bundles
functional, logic, constraint, reactive, declarative, actor-based and
metaprogramming utilities in a single library.

Each module contains examples that can be executed directly from the command
line, demonstrating the available APIs.

## Modules
- `functional` – composition helpers, currying, tail recursion optimization
- `logic` – simple Prolog-style facts, rules and queries
- `constraint` – constraint variables and a backtracking solver
- `reactive` – a lightweight `Signal` class for reactive programming
- `declarative` – basic `@declare` decorator for declarative configurations
- `actor` – actor model concurrency utilities
- `meta` – metaprogramming helpers like auto generated methods

Install the package locally with:

```bash
pip install -e .
```

Run examples:

```bash
python -m multipy.functional
python -m multipy.logic
python -m multipy.constraint
python -m multipy.reactive
python multipy/actor.py
python -m multipy.meta
```
