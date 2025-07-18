# DSPy 101

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

### 4. Run the example scripts

All example scripts are in the `src/` directory.
- `00_baby_steps.py` -> Sample DSPy program to showcase basic syntax.
- `01_intent_classifier.py` -> The intent classifier equivalent in DSPy.
- `02_evaluation.py` -> Simple evaluation dataset for our DSPy program.
- `03_optimization.py` -> Script to optimize few shot examples in our prompt.
- `04_inspect.py` -> Script to inspect the prompt being sent by DSPy.