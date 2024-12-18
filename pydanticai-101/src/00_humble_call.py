import os

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

# Configure logfire
logfire.configure()

# Create a PydanticAI instance
model_name = os.getenv("MODEL_SMALL", "")
model = OpenAIModel(model_name)
agent = Agent(model)

# Run the agent
result = agent.run_sync("What's my plan for today?")
print(result.data)
