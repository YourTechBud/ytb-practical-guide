# Pydantic AI 101

> Consider giving this repo a ✨! Thanks!!!

## Prerequisites

You need to have the following tools installed:

- [uv](https://docs.astral.sh/uv/)
- [Inferix](https://github.com/YourTechBud/inferix) or any OpenAI compatible API.

## Environment Setup

### 1. Setup uv

```bash
# To setup uv
uv sync
```

### 2. Install Inferix (OpenAI compatible API)

> Note: You can use any OpenAI compatible backend or simply use OpenAI itself.

- Feel free to use any OpenAI compatible API.
- Make sure you have [Ollama](https://ollama.ai/) installed.
- Make sure you have pulled a model. I recommend [Qwen 2.5 32B](https://ollama.com/library/qwen2.5:32b).
- Use this [guide to setup inferix](https://github.com/YourTechBud/inferix) to host a OpenAI compatible API capable of function calling.

### 3. Set the environment variables

- Checkout the example dotenv file at `.env.example`.
- Create a new `.env` using the example one as a template.
- Replace the variables as necessary.

## Run the app

We've got a few scripts in this project:

1. `uv run src/00_humble_call.py` - Making a simple LLM call using the `pydantic-ai` sdk.
2. `uv run src/02_structured_responses.py` - Demonstration of how structured responses work.
3. `uv run src/03_tool_call.py` - Demonstration of how to use tools with pydantic ai.
4. `uv run src/04_the_real_deal.py` - A complete agentic workflow made using pydantic ai.