"""Miscellaneous helpers used across the project.

Includes:
* ANSI-coloured ``print`` helper.
* Regex helpers for action-name parsing.
* Small experiment-aggregation helpers (CSV dump / summary table).
"""

import re

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Colour printing
# --------------------------------------------------------------------------- #

_COLOR_CODES = {
    "green":   "\033[92m",
    "blue":    "\033[94m",
    "yellow":  "\033[93m",
    "orange":  "\033[38;2;255;165;0m",
    "red":     "\033[91m",
    "purple":  "\033[95m",
    "magenta": "\033[35m",
}
_RESET_CODE = "\033[0m"


def print_colored(text, color: str) -> None:
    """Print ``text`` in the requested ANSI colour.

    Falls back to the terminal default colour if ``color`` is unknown.
    """
    color_code = _COLOR_CODES.get(color, _RESET_CODE)
    print(f"{color_code}{text}{_RESET_CODE}")


# --------------------------------------------------------------------------- #
# Action-name parsing
# --------------------------------------------------------------------------- #

_PARAMS_RE = re.compile(r"\(([^)]+)\)")
_PREDICATE_RE = re.compile(r"^[^(]+")
_AGENT_ID_RE = re.compile(r"agent-\d+")


def extract_parameters_from_action_name(action_str: str):
    """Return the comma-separated arguments inside ``action_str``'s parens."""
    match = _PARAMS_RE.search(action_str)
    if match:
        return [p.strip() for p in match.group(1).split(",")]
    return []


def extract_predicate_from_action_name(action_str: str):
    """Return the predicate (text before ``(``) from an action name."""
    match = _PREDICATE_RE.match(action_str)
    return match.group() if match else None


def extract_agent_id_from_action_name(action_str: str):
    """Return the ``agent-<n>`` token in ``action_str`` (or ``None``)."""
    match = _AGENT_ID_RE.search(action_str)
    return match.group() if match else None


def filter_action_lists(action_lists, agents_actions):
    """Keep only the actions whose predicate appears in ``agents_actions[i]``."""
    num_agents = len(action_lists)
    filtered = [[] for _ in range(num_agents)]

    for i, action_list in enumerate(action_lists):
        allowed = agents_actions[i]
        for action in action_list:
            predicate = extract_predicate_from_action_name(action.name)
            if predicate in allowed:
                filtered[i].append(action)

    return filtered


# --------------------------------------------------------------------------- #
# Experiment-result helpers
# --------------------------------------------------------------------------- #

def save_results_to_csv(results, filename: str) -> None:
    """Dump ``results`` (list of dicts) to ``filename`` as CSV."""
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)


def print_summary_table(summary_results, formatted: bool = True) -> None:
    """Pretty-print a table of summary dicts."""
    df = pd.DataFrame(summary_results)
    if formatted:
        print(df.to_string(index=False))
    else:
        print(df.to_csv(index=False, sep="\t"))


def calculate_variance(results, key, max_depth, max_branch, num_agent, with_comp_action):
    """Return the variance of ``key`` over the rows matching the filters."""
    return np.var([
        res[key]
        for res in results
        if res["max_depth"] == max_depth
        and res["max_branch"] == max_branch
        and res["num_agent"] == num_agent
        and res["with_comp_action"] == with_comp_action
    ])


def append_summary_results(
    results,
    summary_results,
    max_depth,
    max_branch,
    num_agent,
    with_comp_action,
    total_entries,
    totals,
):
    """Aggregate ``totals`` into a single summary row and append it."""
    avg_values = {k: v / total_entries for k, v in totals.items()}
    variances = {
        k: calculate_variance(
            results, k, max_depth, max_branch, num_agent, with_comp_action
        )
        for k in totals
    }

    summary = {
        "depth":            max_depth,
        "branch":           max_branch,
        "num_agent":        num_agent,
        "with_comp_action": with_comp_action,
        **{f"avg_{k}":      v for k, v in avg_values.items()},
        **{f"variance_{k}": v for k, v in variances.items()},
    }
    summary["success_rate"] = avg_values["success"]
    del summary["avg_success"]

    summary_results.append(summary)
