import os
from time import sleep

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from utils import build_context_from_results, perform_fts_search, perform_vector_search

# Load the environment variables
load_dotenv()

# Configure logfire
logfire.configure()

# Sleep to let logfire setup
sleep(0.5)

# Create PydanticAI Agent
model_name = os.getenv("MODEL_MEDIUM", "")
model = OpenAIModel(model_name)
agent = Agent(
    model=model,
    system_prompt=(
        "You are a helpful ai assistant. Help get the right information to answer the user's question. \n",
        "Decide between using the similarity search tool or the keyword search tool based on what's the best way to search for the information.",
        "vector search is best used for finding important which have semantic similarity to the user's question.",
        "keyword search is best used for finding specific keywords in the database.",
    ),
)


# Define the retrieval tool
@agent.tool_plain
def perform_similarity_search(query: str) -> str:
    """
    Perform a similarity or vector search on the database.
    This is best used for finding important which have semantic similarity to the user's question.

    Args:
        query (str): A concise question for which you need to get the most relevant information.
    """
    print("Similarity search tool was called:", query)

    results = perform_vector_search(query, top_k=10)
    return build_context_from_results(results)


# Define the keyword search tool
@agent.tool_plain
def perform_keyword_search(keyword: str) -> str:
    """
    Perform a keyword based full text search on the database.
    This is best used for finding specific keywords in the database.

    Args:
        keyword (str): A keyword to search for in the database.
    """
    print("Keyword search tool was called:", keyword)

    results = perform_fts_search(keyword, top_k=10)
    return build_context_from_results(results)


def main():
    query = "What are Pikachu's electric type moves?"
    result = agent.run_sync(query)
    print(result.data)


if __name__ == "__main__":
    main()
