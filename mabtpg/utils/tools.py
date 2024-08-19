import pandas as pd
import numpy as np
def print_colored(text, color):
    """
    Prints the provided text in the specified color in the terminal.

    Parameters:
    - text: str, the text to print.
    - color: str, a named color as the desired color output.
    """
    # Mapping color names to ANSI escape sequences
    color_codes = {
        "green": '\033[92m',   # Green
        "blue": '\033[94m',    # Blue
        "yellow": '\033[93m',  # Yellow
        "orange": '\033[38;2;255;165;0m',  # RGB for Orange
        "red": '\033[91m',     # Red
        "purple": '\033[95m',   # Purple
        'magenta': '\033[35m'
    }

    color_code = color_codes.get(color, '\033[0m')  # Default to no color if not found
    reset_color_code = '\033[0m'  # ANSI escape sequence to reset color to default

    print(f"{color_code}{text}{reset_color_code}")


import re
def extract_parameters_from_action_name(action_str):
    match = re.search(r'\(([^)]+)\)', action_str)
    if match:
        parameters = [param.strip() for param in match.group(1).split(',')]
        return parameters
    return []

def extract_predicate_from_action_name(action_str):
    match = re.match(r'^[^(]+', action_str)
    if match:
        return match.group()
    return None


def extract_agent_id_from_action_name(action_str):
    match = re.search(r'agent-\d+', action_str)
    if match:
        return match.group()
    return None


def filter_action_lists(action_lists, agents_actions):
    num_agents = len(action_lists)
    filtered_action_lists = [[] for _ in range(num_agents)]

    for i, action_list in enumerate(action_lists):
        for action in action_list:
            predicate = extract_predicate_from_action_name(action.name)
            if predicate in agents_actions[i]:
                filtered_action_lists[i].append(action)

    return filtered_action_lists



# experience
def save_results_to_csv(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)

def print_summary_table(summary_results, formatted=True):
    df = pd.DataFrame(summary_results)
    if formatted:
        print(df.to_string(index=False))
    else:
        print(df.to_csv(index=False, sep='\t'))


def calculate_variance(results, key, max_depth, max_branch, num_agent, with_comp_action):
    return np.var([res[key] for res in results if
                   res['max_depth'] == max_depth and res['max_branch'] == max_branch and res[
                       'num_agent'] == num_agent and res['with_comp_action'] == with_comp_action])


def append_summary_results(results, summary_results, max_depth, max_branch, num_agent, with_comp_action, total_entries,
                           totals):
    avg_values = {k: v / total_entries for k, v in totals.items()}
    variances = {k: calculate_variance(results, k, max_depth, max_branch, num_agent, with_comp_action) for k in
                 totals.keys()}

    summary = {
        'depth': max_depth,
        'branch': max_branch,
        'num_agent': num_agent,
        'with_comp_action': with_comp_action,
        **{f'avg_{k}': v for k, v in avg_values.items()},
        **{f'variance_{k}': v for k, v in variances.items()}
    }
    summary['success_rate'] = avg_values['success']
    del summary['avg_success']

    summary_results.append(summary)