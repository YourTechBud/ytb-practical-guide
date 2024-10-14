import json
from typing import Literal, Union

from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from k8s_bot.agents.k8s_tools import k8s_tool_node
from k8s_bot.agents.engineer import get_k8s_engineer
from k8s_bot.agents.expert import get_k8s_expert
from k8s_bot.agents.ns_identifier import get_ns_identifier
from k8s_bot.helpers import extract_json
from k8s_bot.state_k8s import K8sState


def route_ns_identifier(
    state: K8sState,
) -> Literal["k8s_ns_identifier", "k8s_engineer"]:
    # Try to load the json text
    try:
        data = extract_json(state["messages"][-1].content)

        # If the value for the field "namespace" is "all", then return the ns_identifier node
        if data["namespace"] != "all":
            return "k8s_ns_identifier"
    except json.JSONDecodeError:
        return "k8s_engineer"

    # Return the engineer node by default
    return "k8s_engineer"


def get_graph():
    graph_builder = StateGraph(K8sState)

    # Add the nodes
    graph_builder.add_node("k8s_expert", get_k8s_expert)
    graph_builder.add_node("k8s_engineer", get_k8s_engineer)
    graph_builder.add_node("k8s_ns_identifier", get_ns_identifier)
    graph_builder.add_node("k8s_tool_node", k8s_tool_node)

    # Add the edges
    graph_builder.add_edge(START, "k8s_expert")
    # We only want to run the k8s_ns_identifier node if the user specifies a namespace.
    graph_builder.add_conditional_edges(
        "k8s_expert",
        route_ns_identifier,
        {"k8s_ns_identifier": "k8s_ns_identifier", "k8s_engineer": "k8s_engineer"},
    )
    graph_builder.add_edge("k8s_ns_identifier", "k8s_engineer")
    graph_builder.add_edge("k8s_engineer", "k8s_tool_node")
    graph_builder.add_edge("k8s_tool_node", END)

    # Set up memory
    memory = MemorySaver()

    # Build the graph
    return graph_builder.compile(checkpointer=memory)


def run(question: Union[str, None]):
    graph = get_graph()
    thread: RunnableConfig = {"configurable": {"thread_id": "default"}}

    # Get input from the user
    if question == None:
        question = input("Enter Request: ")

    for event in graph.stream({"messages": [question]}, thread):
        # Loop over each key in events and print the messages
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)
        pass

    return graph.get_state(thread).values["messages"][-1].content


def main():
    run(None)
