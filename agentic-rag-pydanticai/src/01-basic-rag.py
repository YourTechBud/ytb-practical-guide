import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from utils import build_context_from_results, perform_vector_search

# Load the environment variables
load_dotenv()


def main():
    # Our query
    query = "What are Pikachu's electric type moves?"
    # query = "Between pikachu and charizard who as a more powerful normal type attack?"

    # Get the chunks and form the context
    print("Getting the chunks...")
    results = perform_vector_search(query, top_k=20)
    context = build_context_from_results(results)

    # Create the chat model
    model_name = os.getenv("MODEL_SMALL", "")
    model = ChatOpenAI(model=model_name)

    # Create the response
    print("Creating the response...")
    response = model.invoke(
        [
            SystemMessage(
                content="You are a helpful ai assistant. Carefully study the question and give a descriptive answer to the user's question. Don't use tables in response. Use lists."
            ),
            HumanMessage(
                content=(
                    f"{query}\n"
                    "Carefully study the following context to answer the users's question:\n"
                    f"{context}"
                )
            ),
        ],
    )

    print(response.content)


if __name__ == "__main__":
    main()
