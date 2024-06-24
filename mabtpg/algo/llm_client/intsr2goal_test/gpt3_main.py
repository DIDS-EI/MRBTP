import time

import numpy as np

from mabtpg.algo.llm_client.llms.ERNIE_Bot_4 import LLMERNIE
from mabtpg.algo.llm_client.llms.gpt3 import LLMGPT3
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, Not, Or, And, to_dnf
from sympy import symbols, simplify_logic
import re
from mabtpg.algo.llm_client.dataset.data_process_check import format_check,word_correct,goal_transfer_ls_set
def print_green(text):
    """
    Prints the provided text in green color in the terminal.
    """
    green_color_code = '\033[92m'  # ANSI escape sequence for green color
    reset_color_code = '\033[0m'   # ANSI escape sequence to reset color to default
    print(f"{green_color_code}{text}{reset_color_code}")


def generate_prompt1(num_examples):
    # Basic prompt structure
    prompt1 = """
[Condition Predicates]
RobotNear_<items_place>, On_<items>_<place>, Holding_<items>, Exists_<items>, Dirty_<furniture>, Active_<appliance>, Closed_<furnishing>, Low_<control>

[Objects]
<items>=['Coffee', 'Water', 'Dessert', 'Softdrink', 'BottledDrink', 'Yogurt', 'ADMilk', 'MilkDrink', 'Milk', 'VacuumCup', 'Chips', 'NFCJuice', 'Bernachon', 'ADMilk', 'SpringWater', 'Apple', 'Banana', 'Mangosteen', 'Orange', 'Kettle', 'PaperCup', 'Bread', 'LunchBox', 'Teacup', 'Chocolate', 'Sandwiches', 'Mugs', 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk', 'SugarlessGum', 'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup', 'Tissue', 'YogurtDrink', 'Newspaper', 'Box', 'PaperCupStarbucks', 'CoffeeMachine', 'Straw', 'Cake', 'Tray', 'Bread', 'Glass', 'Door', 'Mug', 'Machine', 'PackagedCoffee', 'CubeSugar', 'Apple', 'Spoon', 'Drinks', 'Drink', 'Ice', 'Saucer', 'TrashBin', 'Knife', 'Cube']
<place>=['Bar', 'Bar2', 'WaterStation', 'CoffeeStation', 'Table1', 'Table2', 'Table3', 'WindowTable6', 'WindowTable4', 'WindowTable5', 'QuietTable7', 'QuietTable8', 'QuietTable9', 'ReadingNook', 'Entrance', 'Exit', 'LoungeArea', 'HighSeats', 'VIPLounge', 'MerchZone']
<items_place>=<items>+<place>
<furniture>=['Table1', 'Floor', 'Chairs']
<appliance>=['AC', 'TubeLight', 'HallLight']
<furnishing>=['Curtain']
<control>=['ACTemperature']

[Few-shot Demonstrations]
"""
    # Define the examples
    examples = [
        "Instruction: Would you be able to provide some chips at the third table?\nOn_Chips_Table3",
        "Instruction: If the curtains are already closed or the AC is running, could you please grab me a hot milk?\n( Closed_Curtain | Active_AC ) & Holding_Milk",
        "Instruction: Please turn up the air conditioning and come to the bar counter.\nRobotNear_Bar & ~Low_ACTemperature",
        "Instruction: Please ensure the water is ready for service, and deliver the yogurt to table number one.\nExists_Water & On_Yogurt_Table1",
        "Instruction: It's a bit messy here, could you rearrange the chairs? And, if possible, could you bring me an apple or a banana to the reading nook?\n~Dirty_Chairs & ( On_Apple_ReadingNook | On_Banana_ReadingNook )"
    ]

    # Add the desired number of examples
    if num_examples > 0:
        prompt1 += "\n".join(examples[:num_examples])

    prompt1 += "\n[System]\n[Condition Predicates] Lists all predicates representing conditions and their optional parameter sets.\n[Objects] Lists all parameter sets.\n[Few-shot Demonstrations] Provide several examples of Instruction to Goal mapping."
    return prompt1


# Example of using the function
print(generate_prompt1(1))  # Generate a prompt with 1 example

def get_feedback_prompt_last(id,prompt,result,error_list,error_black_set):
    # wrong_format_set,wrong_predicate_set,wrong_object_set = error_list

    error_message=""


    if error_list[0]!=None:
        error_message += "It contains syntax errors or illegal characters."
            # ("It Contains syntax errors or illegal characters that cannot be converted to disjunctive normal form (DNF) using sympy.to_dnf. ")
                          # "Please check the syntax in your input and ensure there are no prohibited characters. The answer should consist only of ~, |, &, and the given [Condition] and  [Object].. ")
    else:
        if error_list[1]!=set():
            # error_strings = ", ".join(error_list[1])
            # error_message += f"\"{error_strings}\" have format errors. They should consist only of ~, |, &, and the given [Condition] and  [Object].\n"
            error_black_set[0] |= set(error_list[1])
        if error_list[2]!=set():
            # error_strings = ", ".join(error_list[2])
            # error_message +=  f"\"{error_strings}\" are not in [Condition]. Please select the closest predicates from the [Condition] table to form the answer.\n"
            error_black_set[1] |= set(error_list[2])
        if error_list[3]!=set():
            # error_strings = ", ".join(error_list[3])
            # error_message +=  f"\"{error_strings}\" are not in [Object]. Please select the closest parameter from the [Object] table to form the answer.\n"
            error_black_set[2] |= set(error_list[3])

    # error_strings = "Do not include: "+", ".join(list(error_black_set))+"." +"Please select the closest parameter from the [Condition] and [Object] table to form the answer."

    er_word0 = ", ".join(list(error_black_set[0]))
    er_word1 = ", ".join(list(error_black_set[1]))
    er_word2 = ", ".join(list(error_black_set[2]))

    error_message += f"\"{er_word0}\" have format errors. The answer should consist only of ~, |, &, and the given [Condition] and  [Object].\n"
    error_message += f"\"{er_word1}\" are not in [Condition]. Please select the closest predicates from the [Condition] table to form the answer.\n"
    error_message += f"\"{er_word2}\" are not in [Object]. Please select the closest parameter from the [Object] table to form the answer.\n"


    print("** Error_message: ",error_message)
    prompt += "\n"+ error_message
    return prompt

def get_feedback_prompt0123(id,prompt,result,error_list,error_black_set):
    # wrong_format_set,wrong_predicate_set,wrong_object_set = error_list

    error_message=""

    if error_list[0]!=None:
        error_message += "It contains syntax errors or illegal characters."
    else:
        if error_list[1]!=set():
            error_black_set[0] |= set(error_list[1])
            er_word0 = ", ".join(list(error_black_set[0]))
            error_message += f"\"{er_word0}\" have format errors. The answer should consist only of ~, |, &, and the given [Condition] and  [Object].\n"

        if error_list[2]!=set():
            error_black_set[1] |= set(error_list[2])
            er_word1 = ", ".join(list(error_black_set[1]))
            error_message += f"\"{er_word1}\" are not in [Condition]. Please select the closest predicates from the [Condition] table to form the answer.\n"

        if error_list[3]!=set():
            error_black_set[2] |= set(error_list[3])
            er_word2 = ", ".join(list(error_black_set[2]))
            error_message += f"\"{er_word2}\" are not in [Object]. Please select the closest parameter from the [Object] table to form the answer.\n"

    print("** Error_message: ",error_message)
    prompt += "\n"+ error_message
    return prompt




def get_feedback_prompt(id,prompt1,prompt2,question,result,error_list,error_black_set):

    error_message=""
    er_word0=""
    er_word1=""
    er_word2=""

    if error_list[0]!=None:
        error_message = ""
    else:
        if error_list[1]!=set():
            error_black_set[0] |= set(error_list[1])

        if error_list[2]!=set():
            error_black_set[1] |= set(error_list[2])

        if error_list[3]!=set():
            error_black_set[2] |= set(error_list[3])

        er_word0 = ", ".join(list(error_black_set[0]))
        er_word1 = ", ".join(list(error_black_set[1]))
        er_word2 = ", ".join(list(error_black_set[2]))

        error_message += f"\n[Blacklist]\n<Illegal Condition>=[{er_word1}]\n<Illegal Object>=[{er_word2}]\n<Other Illegal Words or Characters>=[{er_word0}]\n"
        error_message += "\n[Blacklist] Contains restricted elements.\n"+\
    "If a word from <Illegal Condition> is encountered, choose the nearest parameter with a similar meaning from the [Condition] table to formulate the answer.\n"+\
    "If a word from <Illegal Object> is encountered, choose the nearest parameter with a similar meaning from the [Object] table to formulate the answer."

    print("** Blacklist: ",f"[Blacklist]\n<Illegal Characters>=[{er_word0}]\n<Illegal Condition>=[{er_word1}]\n<Illegal Object>=[{er_word2}]")

    # prompt = prompt1+prompt2+error_message
    # prompt = error_message
    # print(prompt)
    prompt = prompt1+prompt2
    # prompt+= question + result
    prompt += error_message
    print(error_message)
    return prompt

def evaluate_answer(correct_answer, user_answer):
    # 你可以根据需要调整这个函数来评估答案的正确性
    return correct_answer == user_answer


# data_set_file = "easy.txt"

easy_data_set_file = "../dataset/easy_instr_goal.txt"
medium_data_set_file = "../dataset/medium_instr_goal.txt"
hard_data_set_file = "../dataset/hard_instr_goal.txt"

test_data_set_file = "../dataset/test.txt"

data_set_file = "../dataset/data100.txt"
prompt_file1 = "../dataset/prompt_test1.txt"
prompt_file2 = "../dataset/prompt_test2.txt"
# prompt_file1 = "prompt1.txt"
# prompt_file2 = "prompt2.txt"
test_num = 1


with open(easy_data_set_file, 'r', encoding="utf-8") as f:
    easy_data_set = f.read().strip()
with open(medium_data_set_file, 'r', encoding="utf-8") as f:
    medium_data_set = f.read().strip()
with open(hard_data_set_file, 'r', encoding="utf-8") as f:
    hard_data_set = f.read().strip()
# with open(data_set_file, 'r', encoding="utf-8") as f:
#     data_set = f.read().strip()

# easy_sections = re.split(r'\n\s*\n', easy_data_set)
# print("easy:",len(easy_sections))
# medium_sections = re.split(r'\n\s*\n', medium_data_set)
# print("medium:",len(medium_sections))
# hard_sections = re.split(r'\n\s*\n', hard_data_set)
# print("hard:",len(hard_sections))
# data_set = easy_data_set & medium_data_set
# print(data_set)

# with open(test_data_set_file, 'r', encoding="utf-8") as f:
#     test_data_set = f.read().strip()
data_set = easy_data_set
# data_set =hard_data_set

# data_set = easy_data_set + medium_data_set + hard_data_set

with open(prompt_file1, 'r', encoding="utf-8") as f:
    prompt1 = f.read().strip()
with open(prompt_file2, 'r', encoding="utf-8") as f:
    prompt2 = f.read().strip()

prompt = prompt1+prompt2

sections = re.split(r'\n\s*\n', data_set)
# print("data_set:",len(sections))
count = 0



# llm = LLMERNIE()
llm = LLMGPT3()


def evaluate_responses(sections, feedback_cycles):
    results = {f'GA-{f}F': [] for f in feedback_cycles}
    results.update({f'IA-{f}F': [] for f in feedback_cycles})

    for i, s in enumerate(sections):
        x, y = s.strip().splitlines()
        question = x.strip()
        correct_answer = y.strip().replace("Goal: ", "")

        # 在你的主循环中维护错误黑名单的状态：
        error_black_set = [set(), set(), set()]

        # Initialize tracking for this section
        feedback_results = {}
        for f in feedback_cycles:
            feedback_results[f] = {'grammar_correct': False, 'intent_correct': False}

        for feedback_count in range(max(feedback_cycles) + 1):
            # Generate prompt with appropriate number of examples
            num_examples = min(feedback_count, 5)  # Assuming you provide max 5 examples
            prompt = generate_prompt1(num_examples)

            messages = [{"role": "user", "content": prompt + "\n" + question}]
            answer = llm.request(message=messages)
            print_green(f"answer: {answer}")

            grammar_correct, error_list = format_check(answer)
            if grammar_correct:
                content_correct = evaluate_answer(correct_answer, answer)
                # Record results at each specific feedback level
                for f in feedback_cycles:
                    if feedback_count <= f:
                        feedback_results[f]['grammar_correct'] = True
                        feedback_results[f]['intent_correct'] = content_correct

            else:
                if feedback_count < max(feedback_cycles):
                    # 只有当需要反馈时才调用此函数，并且传递累积的错误黑名单
                    prompt = get_feedback_prompt(prompt, "", question, "", error_list, error_black_set)

        # After all attempts for this section, save results
        for f in feedback_cycles:
            results[f'GA-{f}F'].append(1 if feedback_results[f]['grammar_correct'] else 0)
            results[f'IA-{f}F'].append(1 if feedback_results[f]['intent_correct'] else 0)

    return results

# Define feedback cycles
feedback_cycles = [0, 1, 5]

# Calculate the results
sections = re.split(r'\n\s*\n', data_set)[:1]  # Assuming data_set is defined and loaded
evaluation_results = evaluate_responses(sections, feedback_cycles)

# Calculate percentage results
total_sections = len(sections)
for key in evaluation_results:
    accuracy = np.mean(evaluation_results[key]) * 100
    print(f"{key}: {accuracy:.2f}%")
