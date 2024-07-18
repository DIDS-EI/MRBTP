

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
        "purple": '\033[95m'   # Purple
    }

    color_code = color_codes.get(color, '\033[0m')  # Default to no color if not found
    reset_color_code = '\033[0m'  # ANSI escape sequence to reset color to default

    print(f"{color_code}{text}{reset_color_code}")


import re
def extract_parameters_from_action_name(action_str):
    # 使用正则表达式提取括号内的参数部分
    match = re.search(r'\(([^)]+)\)', action_str)
    if match:
        # 将参数部分按逗号分割并去掉多余的空格
        parameters = [param.strip() for param in match.group(1).split(',')]
        return parameters
    return []

def extract_predicate_from_action_name(action_str):
    match = re.match(r'^[^(]+', action_str)
    if match:
        return match.group()
    return None


def extract_agent_id_from_action_name(action_str):
    # 使用正则表达式提取 agent 的 ID
    match = re.search(r'agent-\d+', action_str)
    if match:
        return match.group()
    return None