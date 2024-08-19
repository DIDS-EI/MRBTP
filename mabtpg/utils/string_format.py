import re

def parse_predicate_logic(predicate_instance):

    match = re.match(r"(\w+)\((.*)\)", predicate_instance)
    if match:
        type = match.group(1)
        args_str = match.group(2).strip()
        args = tuple(arg.strip() for arg in args_str.split(','))
        return type, args
    else:
        return predicate_instance,()
        # raise ValueError("Invalid predicate logic format")