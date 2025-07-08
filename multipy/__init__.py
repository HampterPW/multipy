"""Multipy: Multi-paradigm programming support for Python."""

from .functional import pipe, compose, curry, pure, rec, match
from .logic import fact, rule, query
from .constraint import Variable, Solver
from .reactive import Signal
from .declarative import declare
from .actor import actor, send
from .meta import auto_repr, auto_eq, transform_ast

__all__ = [
    'pipe', 'compose', 'curry', 'pure', 'rec', 'match',
    'fact', 'rule', 'query',
    'Variable', 'Solver',
    'Signal',
    'declare',
    'actor', 'send',
    'auto_repr', 'auto_eq', 'transform_ast',
]
