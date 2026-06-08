"""Predicate-logic string parsing helpers."""

import re

_PREDICATE_RE = re.compile(r"(\w+)\((.*)\)")


def parse_predicate_logic(predicate_instance: str):
    """Split ``"Pred(a, b)"`` into ``("Pred", ("a", "b"))``.

    If the string does not match a predicate-logic pattern the original
    string is returned together with an empty argument tuple.
    """
    match = _PREDICATE_RE.match(predicate_instance)
    if not match:
        return predicate_instance, ()

    pred_name = match.group(1)
    args_str = match.group(2).strip()
    args = tuple(arg.strip() for arg in args_str.split(","))
    return pred_name, args
