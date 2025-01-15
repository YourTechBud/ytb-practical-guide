from typing import Literal

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

from k8s_bot.agents.human_input import get_human_input
from k8s_bot.agents.input_verifier import get_input_verifier
from k8s_bot.state_user_input import UserInputState


def get_graph():
    graph_builder = StateGraph(UserInputState)

    # Add the nodes
    graph_builder.add_node("human_input", get_human_input)
    graph_builder.add_node("input_verifier", get_input_verifier)

    # Add the edges
    graph_builder.add_edge(START, "human_input")
    graph_builder.add_edge("human_input", "input_verifier")
    graph_builder.add_conditional_edges(
        "input_verifier",
        lambda state: END if state["is_valid"] else "human_input",
        {"human_input": "human_input", "__end__": END},
    )

    # Set up memory
    memory = MemorySaver()

    # Build the graph
    return graph_builder.compile(checkpointer=memory, interrupt_before=["human_input"])

def main():
    # Get the graph
    graph = get_graph()
    thread: RunnableConfig = {"configurable": {"thread_id": "default"}}

    while True:
        initial_input = (
            {"question": "", "is_valid": False}
            if graph.get_state(thread).values == {}
            else None
        )
        for event in graph.stream(initial_input, thread):
            # Loop over each key in events and print the messages
            for key in event:
                print("\n*******************************************\n")
                print(key + ":")
                print("---------------------\n")
                print(event[key]["verifier_response"])

        # Check if we need to ask user or not
        next = graph.get_state(thread).next
        if len(next) == 0 or next[0] != "human_input":
            return graph.get_state(thread).values["question"]

        # Get input from the user
        print("\n*******************************************\n")
        print("human_input:")
        print("---------------------\n")
        input_text = input("Enter Request: ")

        # Update the state as if we are the human_input node
        graph.update_state(thread, {"question": input_text}, as_node="human_input")
