import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

# Create a PydanticAI instance
model_name = os.getenv("MODEL_SMALL", "")
model = OpenAIModel(model_name)
task_summarizer_agent = Agent(
    model,
    system_prompt="You are a helpful AI assitant and a productivity expert. You always respond with motivational and helpful messages.",
)
