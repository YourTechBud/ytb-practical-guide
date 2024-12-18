import os

import logfire
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

# Configure logfire
logfire.configure()


# Define a Pydantic model for the intent
class Intent(BaseModel):
    intent: str


# Create a PydanticAI instance
model_name = os.getenv("MODEL_MEDIUM", "")
model = OpenAIModel(model_name)
agent = Agent(
    model,
    system_prompt=(
        "You are a helpful ai assistant\n"
        "Identify the user's intent from the provided options\n"
        "Choose from these options: `getTasks`, `markTaskAsDone`, `addTask`\n"
    ),
    result_type=Intent,
    result_retries=3,
)


@agent.result_validator
def validate_intent(ctx: RunContext[None], result: Intent) -> Intent:
    if result.intent not in ["getTasks", "markTaskAsDone", "addTask"]:
        raise ModelRetry("Invalid intent provided")
    return result


result = agent.run_sync("I just got done with my groceries.")
print(result.data)
