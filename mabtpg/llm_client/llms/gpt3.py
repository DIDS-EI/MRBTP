"""GPT-3.5-turbo client."""

from mabtpg.llm_client.base import BaseLLMClient


class LLMGPT3(BaseLLMClient):
    DEFAULT_MODEL = "gpt-3.5-turbo"


if __name__ == "__main__":
    llm = LLMGPT3()
    messages = [{"role": "system", "content": ""}]
    while True:
        prompt = input("Please enter your question: ")
        messages.append({"role": "user", "content": prompt})
        res_msg = llm.request(messages)
        messages.append({"role": "assistant", "content": res_msg})
        print(res_msg)
