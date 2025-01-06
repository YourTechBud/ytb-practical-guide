import os
from time import sleep

import logfire
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from utils import (
    build_context_from_results,
    perform_fts_search,
    perform_vector_search,
    read_files_as_object_array,
)

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


@agent.system_prompt
def dynamic_system_prompt(ctx: RunContext[None]) -> str:
    files = read_files_as_object_array("./data")

    return "Here is a list of pokemons you can search for:\n" + "\n".join(
        [f"- {file['filename']}" for file in files]
    )


# Define the retrieval tool
@agent.tool_plain
def perform_similarity_search(query: str, pokemon: str) -> str:
    """
    Perform a similarity or vector search on the database.
    This is best used for finding important which have semantic similarity to the user's question.

    Args:
        query (str): A concise question for which you need to get the most relevant information.
        pokemon (str): The pokemon to search for.
    """
    print("Similarity search tool was called:", query)
    print("Pokemon:", pokemon)

    results = perform_vector_search(query, pokemon=pokemon, top_k=2)
    return build_context_from_results(results)


@agent.tool_plain
def perform_keyword_search(keyword: str, pokemon: str) -> str:
    """
    Perform a keyword based full text search on the database.
    This is best used for finding specific keywords in the database.

    Args:
        keyword (str): A keyword to search for in the database.
        pokemon (str): The pokemon to search for.
    """
    print("Keyword search tool was called:", keyword)
    print("Pokemon:", pokemon)

    results = perform_fts_search(keyword, top_k=2, pokemon=pokemon)
    return build_context_from_results(results)


def main():
    query = "What are Pikachu's electric type moves?"
    result = agent.run_sync(query)
    print(result.data)


if __name__ == "__main__":
    main()
