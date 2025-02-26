import os


from openai import OpenAI
import openai
from enum import Enum
from typing import Union

from pydantic import BaseModel


class Action(str, Enum):
    # Walk_self_toy = "Walk(self,toy)"
    # RightGrab_self_toy = "RightGrab(self,toy)"
    actions_name_str_ls = []


class AgentSubtreeList(BaseModel):
    """
    `subtree_dict` contains multiple combined action pairs, i.e., includes multiple key-value pairs, typically 2-4 key-value pairs
    """
    subtree_dict: dict[str,list[Action]]


class Query(BaseModel):
    """
    `multi_subtree_list` contains n dictionaries, where n is the number of agents, which equals the number of action lists in `action_space`
    """
    multi_subtree_list: list[AgentSubtreeList]



class LLMGPT3():
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.dwyu.top/v1", api_key="sk-CSHOawi329bdxl4nkaHWJDVfp8bj6pDFzM2vfjLFva0F7Msy"
        )

    def tool_request(self, messages, tools):
        completion = self.client.chat.completions.create(
            # model="gpt-3.5-turbo-0125",
            # model="gpt-3.5-turbo-1106",
            model="gpt-3.5-turbo",
            # messages=[
            #   {"role": "system", "content": ""},#You are a helpful assistant.
            #   {"role": "user", "content": question}
            # ]
            messages=messages,
            tools=tools
        )

        return completion.choices[0].message.tool_calls[0].function.arguments

    # def request(self,message): # question
    #     completion = self.client.chat.completions.create(
    #       model="gemini-1.5-pro-002",
    #       # messages=[
    #       #   {"role": "system", "content": ""},#You are a helpful assistant.
    #       #   {"role": "user", "content": question}
    #       # ]
    #         messages=message
    #     )
    #
    #     return completion.choices[0].message.content

    # def embedding(self,question):
    #     embeddings = self.client.embeddings.create(
    #       model="text-embedding-3-small",
    #       # model="text-embedding-ada-002",
    #       input=question
    #     )
    #
    #     return embeddings
    # def list_models(self):
    #     response = self.client.models.list()
    #     return response.data
    # def list_embedding_models(self):
    #     models = self.list_models()
    #     embedding_models = [model.id for model in models if "embedding" in model.id]
    #     return embedding_models


if __name__ == '__main__':

    example = """
        {
        "goal": [
            "IsIn(milk,fridge)"
        ],
        "init_state": [
            "IsClose(fridge)"
        ],
        "objects": [
            "milk",
            "fridge"
        ],
        "action_space": [
            [
                "Walk",
                "RightGrab",
                "RightPutIn",
                "Open",
                "SwitchOn"
            ],
            [
                "Walk",
                "RightGrab",
                "RightPutIn",
                "SwitchOn"
            ]
        ],
        "multi_subtree_list": [
            {
                "WalkToOpenFridge": ["Walk(self,fridge)", "Open(self,fridge)"],
                "WalkToPutInMilkFridge": ["Walk(self,milk)","RightGrab(self,milk)","Walk(self,fridge)","RightPutIn(self,milk,fridge)"]
            },
            {
                "WalkToPutInMilkFridge": ["Walk(self,milk)","RightGrab(self,milk)","Walk(self,fridge)","RightPutIn(self,milk,fridge)"]
            }
        ]
    }"""

    task_info = """
            "goal": [
            "IsOn(toy,bookshelf)",
            "IsIn(book,bookshelf)",
            "IsOpen(closet)",
            "IsSwitchedOn(microwave)"
        ],
        "init_state": [ "IsClose(closet)", "IsSwitchedOff(microwave)","IsClose(microwave)"
        ],
        "objects": [
            "toy",
            "book",
            "bookshelf"
        ],
        "action_space": [
            [
                "Walk",
                "RightGrab",
                "RightPut",
                 "SwitchOn",
                "SwitchOff"
            ],
            [
                "Walk",
                "Open",
                "RightGrab",
                "RightPutIn"
            ]
        ],"""

    tools = [openai.pydantic_function_tool(Query)]

    llm = LLMGPT3()
    messages = [{"role": "system", "content": "You are a helpful assistant. Please provide some combined actions for each agent based on the task by calling the query function."}]

    prompt = f"""
    subtree_name is the name of the combined action, and action_list specifies which actions are to be combined.

    [example]
    {example}

    [task info]
    {task_info}

    The number of agents in this task is 2. That is, `multi_subtree_list` has 2 dictionaries. Each dictionary has 4 key-values.
"""

    messages.append({"role": "user", "content": prompt})
    res_msg = llm.tool_request(messages,tools=tools)
    print(res_msg)

    multi_subtree_list = eval(res_msg)["multi_subtree_list"]

    print(multi_subtree_list)


    # multi_subtree_list=[]
    # for llm_subtree_list in llm_multi_subtree_list:
    #     subtree_dic = {}
    #     for llm_subtree in llm_subtree_list:
    #         subtree_dic[llm_subtree['subtree_name']] = llm_subtree['action_list']
    #     multi_subtree_list.append(subtree_dic)


