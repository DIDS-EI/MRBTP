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
question_list = []
correct_answer_list = []
correct_answer_ls_set = []
outputs_list = [[] for _ in range(len(sections))]

total_num = len(question_list)

error_black_ls = [[set(),set(),set()] for _ in range(total_num)]



max_attempts = 2
# total_GR_ls = np.zeros(5)
total_GR_ls=[]
total_SR_ls = []
total_GCR_ls = []

# for time in range(try_times):
finish_num = 0
SR = 0
GR = 0
GCR = 0
# 统计语法正确的数量
GR_ls=np.zeros(6)



for i, s in enumerate(sections[:1]):
    x, y = s.strip().splitlines()
    question = x.strip()
    correct_answer = y.strip().replace("Goal: ", "")


    attempts = 0
    grammar_attempts = 0
    content_correct = False
    grammar_correct = False
    error_black_set = [set(), set(), set()]

    while attempts < max_attempts:
        messages = []
        messages.append({"role": "user", "content": prompt + "\n" +question})
        answer = llm.request(message=messages)
        print_green(f"answer: {answer}")

        grammar_correct, error_list = format_check(answer)

        if not grammar_correct:
            prompt = get_feedback_prompt(prompt, error_list, error_black_set)
            attempts += 1
            grammar_attempts = attempts
        else:
            content_correct = evaluate_answer(correct_answer, answer)
            if content_correct:
                break
            else:
                prompt = get_feedback_prompt(prompt, error_list, error_black_set)
                attempts += 1
                grammar_attempts = attempts

    print(f"Grammar Correct on Attempt: {grammar_attempts}")
    print(f"Content Correct: {content_correct}")