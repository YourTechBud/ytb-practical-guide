import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load the environment variables
load_dotenv()

# Create PydanticAI Agent
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
finalizer_agent = Agent(
    model=_model,
    system_prompt=(
        "You are a helpful ai assistant.\n"
        "Give a descriptive & detailed answer to the user's question."
    ),
)
