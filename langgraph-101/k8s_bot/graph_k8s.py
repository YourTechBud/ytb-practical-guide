import json
from typing import Literal
from langgraph.graph import StateGraph, START, END

from k8s_bot.agents.k8s_tools import k8s_tool_node
from k8s_bot.agents.engineer import get_k8s_engineer
from k8s_bot.agents.expert import get_k8s_expert
from k8s_bot.agents.ns_identifier import get_ns_identifier
from k8s_bot.helpers import extract_json
from k8s_bot.state_k8s import K8sState


def route_ns_identifier(state: K8sState) -> Literal["k8s_ns_identifier", "k8s_engineer"]:
    # Try to load the json text
    try:
        data = extract_json(state["k8s_internal_messages"][-1].content)

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
    graph_builder.add_conditional_edges(
        "k8s_expert",
        route_ns_identifier,
        {"k8s_ns_identifier": "k8s_ns_identifier", "k8s_engineer": "k8s_engineer"},
    )
    graph_builder.add_edge("k8s_ns_identifier", "k8s_engineer")
    graph_builder.add_edge("k8s_engineer", "k8s_tool_node")
    graph_builder.add_edge("k8s_tool_node", END)

    # Build the graph
    return graph_builder.compile()


def main():
    graph = get_graph()

    # Get input from the user
    input_text = input("Enter Request: ")
    for event in graph.stream({"messages": [input_text], "k8s_internal_messages": []}):
        # Loop over each key in events and print the messages
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["k8s_internal_messages"][-1].content)
