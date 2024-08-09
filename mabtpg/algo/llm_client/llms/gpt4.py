import os
# os.environ["OPENAI_API_KEY"]="sk-4vD6bVtv67XcfoVS8802AdF75888473296D604D707FbC9Bf"
# os.environ["OPENAI_BASE_URL"]= "https://gtapi.xiaoerchaoren.com:8932"

from openai import OpenAI
import openai
from enum import Enum
from typing import Union

from pydantic import BaseModel

class Table(str, Enum):
    orders = "orders"
    customers = "customers"
    products = "products"


class Column(str, Enum):
    id = "id"
    status = "status"
    expected_delivery_date = "expected_delivery_date"
    delivered_at = "delivered_at"
    shipped_at = "shipped_at"
    ordered_at = "ordered_at"
    canceled_at = "canceled_at"


class Operator(str, Enum):
    eq = "="
    gt = ">"
    lt = "<"
    le = "<="
    ge = ">="
    ne = "!="


class OrderBy(str, Enum):
    asc = "asc"
    desc = "desc"


class DynamicValue(BaseModel):
    column_name: str


class Condition(BaseModel):
    column: str
    operator: Operator
    value: Union[str, int, DynamicValue]


class Query(BaseModel):
    table_name: Table
    columns: list[Column]
    conditions: list[Condition]
    order_by: OrderBy


class LLMGPT4():
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.xty.app/v1", api_key="sk-0aT67hZ747Jy9XDR2cB6F051A11d41Dc8955633bF5008327"
            # base_url="https://gtapi.xiaoerchaoren.com:8932/v1",            api_key="sk-OO5BXh9SUMrnWR6q6fC035142aC94352A59f78E8655fE62b"
        )

    def tool_request(self, message, tools):
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            # messages=[
            #   {"role": "system", "content": ""},#You are a helpful assistant.
            #   {"role": "user", "content": question}
            # ]
            messages=message,
            tools=tools
        )

        return completion.choices[0].message.tool_calls[0].function

    def request(self,message): # question
        completion = self.client.chat.completions.create(
          model="gpt-4o-mini-2024-07-18",
          # messages=[
          #   {"role": "system", "content": ""},#You are a helpful assistant.
          #   {"role": "user", "content": question}
          # ]
            messages=message
        )

        return completion.choices[0].message.content

    def embedding(self,question):
        embeddings = self.client.embeddings.create(
          model="text-embedding-3-small",
          # model="text-embedding-ada-002",
          input=question
        )

        return embeddings
    def list_models(self):
        response = self.client.models.list()
        return response.data
    def list_embedding_models(self):
        models = self.list_models()
        embedding_models = [model.id for model in models if "embedding" in model.id]
        return embedding_models


if __name__ == '__main__':

    tools = [openai.pydantic_function_tool(Query) ]

    llm = LLMGPT4()
    messages = [{"role": "system", "content": "You are a helpful assistant. The current date is August 6, 2024. You help users query for the data they are looking for by calling the query function."}]

    prompt = "look up all my orders in may of last year that were fulfilled but not delivered on time"

    messages.append({"role": "user", "content": prompt})
    res_msg = llm.tool_request(messages,tools=tools)
    print(res_msg)