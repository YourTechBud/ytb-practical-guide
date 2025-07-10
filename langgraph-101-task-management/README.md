# LangGraph + Pydantic AI

> Consider giving this repo a ✨! Thanks!!!

Here's a link to the YouTube video explaining this setup in greater detail:

[![PydanticAI + Langgraph: The Ultimate Match for Smarter AI Agents!](./assets/thumbnail.png)](https://youtu.be/P3qH5GVIxD0)

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

1. `uv run src/01_first_graph.py` - Our first graph using LangGraph.
2. `uv run src/02-basic-read.py` - Simple tool use in LangGraph (using LangChain).
3. `uv run src/03-basic-read-pydantic.py` - Simple tool use in LangGraph (using Pydantic AI).
4. `uv run src/04-mixing-it-up.py` - Mixing up LangChain and Pydantic AI within LangGraph.
5. `uv run src/05-final-graph.py` - A complete agentic workflow made using Pydantic AI & LangGraph.
