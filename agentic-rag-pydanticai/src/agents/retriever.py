import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from utils import (
    build_context_from_results,
    perform_fts_search,
    perform_vector_search,
)

# Load the environment variables
load_dotenv()

# Create PydanticAI Agent
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
retriever_agent = Agent(
    model=_model,
    system_prompt=(
        "You are a helpful ai assistant. Help get the right information to answer the user's question. \n",
        "Decide between using the similarity search tool or the keyword search tool based on what's the best way to search for the information.",
        "vector search is best used for finding important which have semantic similarity to the user's question.",
        "keyword search is best used for finding specific keywords in the database.",
    ),
    retries=3,
)


# @retriever_agent.system_prompt
# def dynamic_system_prompt(ctx: RunContext[None]) -> str:
#     files = read_files_as_object_array("./data")

#     return (
#         "Here is a list of pokemons you can search for. Make sure to include the .md extension:\n"
#         + "\n".join([f"- {file['filename']}" for file in files])
#     )


# Define the retrieval tool
@retriever_agent.tool_plain
def perform_similarity_search(query: str) -> str:
    """
    Perform a similarity or vector search on the database.
    This is best used for finding important which have semantic similarity to the user's question.

    Args:
        query (str): A concise question for which you need to get the most relevant information.
    """

    results = perform_vector_search(query, top_k=7)
    return build_context_from_results(results)


@retriever_agent.tool_plain
def perform_keyword_search(keyword: str) -> str:
    """
    Perform a keyword based full text search on the database.
    This is best used for finding specific keywords in the database.

    Args:
        keyword (str): A keyword to search for in the database.
    """
    print("Performing keyword search for:", keyword)
    results = perform_fts_search(keyword, top_k=7)
    return build_context_from_results(results)
