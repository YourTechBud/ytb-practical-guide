# Building Agents Using Langgraph JS

> Consider giving this repo a ✨! Thanks!!!

## Prerequisites

You need to have the following tools installed:

- [NodeJS](https://nodejs.org/en/download/package-manager)
- [PNPM](https://pnpm.io/installation)
- [Inferix](https://github.com/YourTechBud/inferix) or any OpenAI compatible API.

## Environment Setup

### 1. Setup the project

```bash
# To install all dependencies
pnpm install
```

### 2. Install Inferix (OpenAI compatible API)

- Feel free to use OpenAI or any OpenAI compatible server. 
- Use this [guide to setup inferix](https://github.com/YourTechBud/inferix) to host a OpenAI compatible API capable of function calling.

### 3. Set the environment variables

- `INFERIX_BASE_URL`
- `INFERIX_API_KEY`

> You can change these by updating the `./src/utils/models.ts` file.

## Run The App

We got 4 scripts in this project:
1. `pnpm run 00` - Making a simple inference call using langchain js.
2. `pnpm run 01` - Running an langgraph equivalent of the above step.
3. `pnpm run 02` - Add support for function/tool calling in langgraph
3. `pnpm run 03` - A full feldged langgraph app.

You can try running the final script with the following inputs:
- `Get me all my tasks` - It will list and summarize all your tasks.
- `I got my groceries` - It marks the "Buy groceries task as done."
- `I finished watching all episodes from Naruto` - It doesn't do anything cause such a task doesn't exist.