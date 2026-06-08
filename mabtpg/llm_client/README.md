# LLM Client

Thin OpenAI-compatible client used by MABTPG experiments to query large
language models for behaviour-tree planning, sub-tree generation, etc.

## Layout

```
mabtpg/llm_client/
├── base.py          # BaseLLMClient (request / tool_request / embedding / list_models)
├── llms/            # Concrete model clients
│   ├── gpt3.py      # LLMGPT3   -> gpt-3.5-turbo
│   ├── gpt4.py      # LLMGPT4   -> gpt-4o-mini-2024-07-18
│   └── gpt4o.py     # LLMGPT4o  -> gpt-4o-2024-08-06
└── schemas/         # Pydantic schemas used as OpenAI tools
    └── subtree.py   # Action / AgentSubtreeList / Query
```

## Configuration

Credentials are read with the following precedence:

1. constructor arguments: `LLMGPT3(model=..., base_url=..., api_key=...)`
2. environment variables: `OPENAI_BASE_URL`, `OPENAI_API_KEY`
3. placeholder values (`YOUR_URL` / `YOUR_KEY`) — the request will fail
   with a clear OpenAI auth error so you know to configure something.

```bash
export OPENAI_BASE_URL=https://api.openai.com/v1
export OPENAI_API_KEY=sk-...
```

## Quick start

### Plain chat

```python
from mabtpg.llm_client import LLMGPT3

llm = LLMGPT3()
print(llm.request([
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user",   "content": "Hello!"},
]))
```

### Structured tool calling

```python
import openai
from mabtpg.llm_client import LLMGPT4o, Query

llm = LLMGPT4o()
tools = [openai.pydantic_function_tool(Query)]

messages = [
    {"role": "system", "content": "You decompose tasks into sub-trees."},
    {"role": "user",   "content": "..."},
]
arguments_json = llm.tool_request(messages, tools=tools)
multi_subtree_list = eval(arguments_json)["multi_subtree_list"]
```

`tool_request` returns the JSON arguments string of the first tool call,
matching how the existing experiments under `test_experiment/` consume it.

## Adding a new model

```python
# mabtpg/llm_client/llms/my_model.py
from mabtpg.llm_client.base import BaseLLMClient

class MyModel(BaseLLMClient):
    DEFAULT_MODEL = "my-model-id"
```

Then re-export it from `mabtpg/llm_client/llms/__init__.py` and (optionally)
from `mabtpg/llm_client/__init__.py`.
