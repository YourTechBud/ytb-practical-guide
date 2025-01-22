import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()


# Define the dependencies
@dataclass
class MyDeps:
    name: str


# Create a PydanticAI instance
modelName = os.getenv("MODEL_SMALL", "")
model = OpenAIModel(modelName)
agent = Agent(
    model,
    deps_type=MyDeps,
    system_prompt=("You are a helpful ai assistant\n"),
)


# Define a system prompt that uses the user's name
@agent.system_prompt
def system_prompt(ctx: RunContext[MyDeps]) -> str:
    return "Always use the user's name in the response: " + ctx.deps.name


# Run the agent
result = agent.run_sync("What's up?", deps=MyDeps("YourTechBud"))
print(result.data)
