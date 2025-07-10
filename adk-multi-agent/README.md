# Multi-Agent system with Google ADK

> Consider giving this repo a ✨! Thanks!!!

Here's a link to the YouTube video explaining this setup in greater detail:

[![Building Agents using MCP](./assets/building-mcp-agents.png)](https://youtu.be/9izHUWherYw)

## Prerequisites

You need to have the following tools installed:

- [uv](https://docs.astral.sh/uv/)
- [Google AI Studio Key](https://aistudio.google.com/apikey)

## Environment Setup

### 1. Setup uv

```bash
# To setup uv
uv sync
```

### 2. Configure your Google AI studio keys

1. Open (Google AI Studio)[https://aistudio.google.com/apikey] and create an API Key.
2. Rename `.env.example` to `.env` and paste you key in there.

### 3. Set the environment variables

- Checkout the example dotenv file at `.env.example`.
- Create a new `.env` using the example one as a template.
- Replace the variables as necessary.

## 5. Run the app

We've got a few scripts in this project. Check them out in the `client` directory.

```bash
# You can run a script using this command
uv run adk web
```

Select `agent_assistant_custom` from the agent dropdown in the top left.

You can run the following queries to try it out:

- `Schedule all tasks for project mewtwo`
- `List all my projects`
