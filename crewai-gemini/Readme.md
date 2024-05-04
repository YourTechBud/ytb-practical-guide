# Using CrewAI with Google's Gemini Pro

## Prequisites:

You need to have the following tools installed:
- [Poetry](https://python-poetry.org/docs/)
- [Gemini API Key](https://aistudio.google.com/app/apikey)
## Environment Setup

### 1. Start LiteLLM

```bash
export GEMINI_API_KEY='[YOUR_KEY]'
poetry run litellm --config litellm.yaml
```

This starts an OpenAI compatible API on port 4000 using [litellm](https://docs.litellm.ai/docs/).

### 2. Kickoff your CrewAI Crew

```bash
# First setup environment variables to make sure CrewAI is pointing to LiteLLM
export OPENAI_API_BASE=http://localhost:4000
export OPENAI_MODEL_NAME=gemini-pro
export OPENAI_API_KEY=NA

poetry run app
```