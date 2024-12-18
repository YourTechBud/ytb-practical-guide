import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()


# Define a Pydantic model for the intent
class Intent(BaseModel):
    action: str


# Create a PydanticAI instance
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
intent_classifier_agent = Agent(
    _model,
    system_prompt=(
        "You are a helpful ai assistant\n"
        "Identify the user's intent from the provided message\n"
        "Choose from these options: `getTasks`, `markTaskAsDone`, `addTask` and `unknown`\n"
        "If the user mentions that they have done something, mark the task as done."
        "Action will be invalid for all invalid messages"
    ),
    result_type=Intent,
    result_tool_name="user_intent",
    result_tool_description="Log the user's intended action and whether it is valid",
    result_retries=3,
)


@intent_classifier_agent.result_validator
def validate_result(ctx: RunContext[None], result: Intent) -> Intent:
    if result.action not in ["getTasks", "markTaskAsDone", "addTask", "unknown"]:
        raise ModelRetry(
            "Invalid action. Please choose from `getTasks`, `markTaskAsDone`, `addTask` and `unknown`"
        )

    return result
