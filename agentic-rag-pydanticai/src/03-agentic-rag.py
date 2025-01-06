from time import sleep

import logfire

from agents.extractor import extractor_agent
from agents.finalizer import finalizer_agent
from agents.planner import planner_agent
from agents.retriever import retriever_agent

# Configure logfire
logfire.configure()

# Sleep to let logfire setup
sleep(0.5)


def main():
    query = "Name the pokemons that learn the move thunderbolt or growl?"

    # Get the subquestions
    subquestions = planner_agent.run_sync(query)
    print("Identified Subquestions:")
    print("\n".join(subquestions.data.subquestions))
    print("\n")

    # Get the relevant information for each subquestion
    contexts = []
    for subquestion in subquestions.data.subquestions:
        print(f"Getting relevant information for: {subquestion}")
        retriever_result = retriever_agent.run_sync(subquestion)

        # Extract the relevant information
        prompt_for_extractor = (
            f"{subquestion}\n"
            "Carefully study the following context to answer the users's question:"
            f"{retriever_result.data}"
        )
        extractor_result = extractor_agent.run_sync(prompt_for_extractor)
        print(f"Extracted relevant information:\n{extractor_result.data}")

        # Add the final context to the list
        contexts.append(extractor_result.data)

    # Finalize the answer
    context = "---\n".join(contexts)
    prompt_for_finalizer = (
        f"{query}"
        "Carefully study the folloing context to answer the user's question"
        f"{context}"
    )
    final_answer = finalizer_agent.run_sync(prompt_for_finalizer)
    print(f"Final Answer:\n{final_answer.data}")


if __name__ == "__main__":
    main()
