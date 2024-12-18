import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from utils.model import UserState
from utils.tasks import read_tasks

# Load environment variables
load_dotenv()


# Define a Pydantic model for the result
class Match(BaseModel):
    title: str
    is_title_present: bool


# Create a PydanticAI instance
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
title_matcher_agent = Agent(
    _model,
    system_prompt=("You are a helpful ai assistant\n"),
    deps_type=UserState,
    result_type=Match,
    result_tool_name="title_matcher",
    result_tool_description="Identify the right title",
    result_retries=3,
)


@title_matcher_agent.system_prompt
def system_prompt(ctx: RunContext[UserState]) -> str:
    # First, we read the tasks for the user
    titles = read_tasks(ctx.deps.id)

    # Craft the system prompt
    return (
        "Identify the title provided by the user\n"
        f"The title must be present in this list: {titles}\n\n"
        "Find the title which is the closest match to the user's input\n"
        "If no title is present, provide an empty string and mark is_title_present as False"
    )
