import os

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

# Configure logfire
logfire.configure()

# Create a PydanticAI instance
modelName = os.getenv("MODEL_MEDIUM", "")
model = OpenAIModel(modelName)
agent = Agent(
    model,
    system_prompt=(
        "You are a helpful ai assistant. Don't call the function if you already have the tasks. Format the task list properly.\n"
    ),
)


# Define the tool that returns the tasks
@agent.tool
def getTasks(ctx: RunContext[None], filter: str) -> str:
    """Get the tasks for the specified day.

    Args:
        filter (str): What tasks to filter. Valid values are 'done', 'pending' and 'all'.
    """

    return (
        f"Here are your {filter} tasks.\n"
        "1. Buy groceries\n"
        "2. Finish the report\n"
        "3. Call mom\n"
    )


# Call the agent
result = agent.run_sync("What's my plan for today?")
print(result.data)
