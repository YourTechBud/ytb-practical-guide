import os

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext
from pydantic_ai.models.openai import OpenAIModel

# Load the environment variables
load_dotenv()


# Define the result type
class Result(BaseModel):
    subquestions: list[str]


# Create PydanticAI Agent
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
planner_agent = Agent(
    model=_model,
    system_prompt=(
        "You are a helpful ai assistant.\n",
        "You need to break the user's question down into smaller groups of questions.\n"
        "Each question should be a standalone question that does not depend on the answer of any other question.\n",
        "Try to group related questions together to keep the number of questions to a minimum. Power and the moves can be asked in a single question.\n",
    ),
    result_type=Result,
    result_retries=3,
    result_tool_name="subquestions",
    result_tool_description="A list of subquestions to ask the user to retreive all the relavant information required to answer the main question",
)


@planner_agent.result_validator
def validate_result(ctx: RunContext[None], result: Result) -> Result:
    if not result.subquestions:
        raise ModelRetry("No subquestions found. Please try again.")

    return result
