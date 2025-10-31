from dataclasses import dataclass

from constants import MODEL_NAME
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, PromptedOutput, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from tasks import read_tasks

# Load environment variables
load_dotenv()


# Define a model for the dependencies
@dataclass
class TitleMatcherDeps:
    userid: str


# Define a Pydantic model for the result
class ResultType(BaseModel):
    title: str
    is_title_present: bool


# Create a PydanticAI instance
_model = OpenAIChatModel(MODEL_NAME)
title_matcher_agent = Agent(
    model=_model,
    instructions=("You are a helpful ai assistant\n"),
    deps_type=TitleMatcherDeps,
    output_type=PromptedOutput(
        outputs=[ResultType],
        name="title_matcher",
        description="Identify the right title",
    ),
)


@title_matcher_agent.system_prompt
def system_prompt(ctx: RunContext[TitleMatcherDeps]) -> str:
    # First, we read the tasks for the user
    titles = read_tasks(ctx.deps.userid)

    # Craft the system prompt
    return (
        "Identify the title provided by the user\n"
        f"The title must be present in this list: {titles}\n\n"
        "Find the title which is the closest match to the user's input\n"
        "If no title is present, provide an empty string and mark is_title_present as False"
    )
