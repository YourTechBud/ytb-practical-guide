# Agentic RAG with Pydantic AI

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

1. `uv run src/00_humble_call.py` - Runs the ingestion script to create the embeddings and full text search index.
2. `uv run src/01-basic-rag.py` - Demonstrates a basic RAG workflow.
3. `uv run src/02a-rag-as-tool.py` - Demonstrates how you can agents can perform RAG by means of a tool call.
4. `uv run src/02b-rag-as-system-prompt.py` - Demonstrates how you can use Pydantic AI's system prompt hook to perform RAG.
5. `uv run src/02c-rag-combined.py` - Demonstrates how you can combine the two approaches to perform RAG.
6. `uv run src/03-agentic-rag.py` - Demonstrates how you can use Pydantic AI's agentic workflow to perform RAG.
