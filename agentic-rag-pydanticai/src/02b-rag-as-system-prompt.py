import os
from time import sleep

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from utils import build_context_from_results, perform_vector_search

# Load the environment variables
load_dotenv()

# Configure logfire
logfire.configure()

# Sleep to let logfire setup
sleep(0.5)

# Create PydanticAI Agent
model_name = os.getenv("MODEL_SMALL", "")
model = OpenAIModel(model_name)
agent = Agent(
    model=model,
    system_prompt=(
        "You are a helpful ai assistant.\n"
        "Give a short and descriptive answer to the user's question. Use lists to structure response."
    ),
)


# Dynamic system prompt
@agent.system_prompt
def dynamic_system_prompt(ctx: RunContext[None]) -> str:
    print("System prompt was called:", ctx.prompt)
    results = perform_vector_search(ctx.prompt, top_k=5)
    context = build_context_from_results(results)

    return (
        "Carefully study the following context to answer the users's question:\n"
        f"{context}\n"
    )


def main():
    query = "What are Pikachu's electric type moves?"
    result = agent.run_sync(query)
    print(result.data)


if __name__ == "__main__":
    main()
