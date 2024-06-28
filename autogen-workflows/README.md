# Building Custom Workflows with AutoGen

> Consider giving this repo a ✨! Thanks!!!

## Prerequisites

You need to have the following tools installed:

- [Poetry](https://python-poetry.org/docs/)
- [Inferix](https://github.com/YourTechBud/inferix) or any OpenAI compatible API.

## Environment Setup

### 1. Setup poetry & K8s Environment

```bash
# To setup poetry
poetry install
```

### 2. Install Inferix (OpenAI compatible API)

- Feel free to use any OpenAI compatible API.
- Make sure you have [Ollama](https://ollama.ai/) installed.
- Make sure you have pulled a model. I recommend [OpenHermes 2.5](https://ollama.ai/library/openhermes:7b-mistral-v2.5-q5_K_M).
- Use this [guide to setup inferix](https://github.com/YourTechBud/inferix) to host a OpenAI compatible API capable of function calling.

### 3. Run the AutoGen App

```bash
# Basic program (Summarization with optional title generation)
poetry run basic -g -f note.md

# Advance program (Note paraphrazing with task identification)
poetry run advanced -f note.md
```