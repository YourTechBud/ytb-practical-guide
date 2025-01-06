import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load the environment variables
load_dotenv()

# Create PydanticAI Agent
_model_name = os.getenv("MODEL_SMALL", "")
_model = OpenAIModel(_model_name)
extractor_agent = Agent(
    model=_model,
    system_prompt=(
        "You are a helpful ai assistant.\n",
        "Give a concise answer to the user's question. Use lists to give a structured answer.",
    ),
)
