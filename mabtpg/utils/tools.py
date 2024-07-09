

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
