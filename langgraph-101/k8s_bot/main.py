from langgraph.graph import StateGraph, START, END

from k8s_bot.k8s_tools import k8s_tool_node
from k8s_bot.agent_engineer import get_k8s_engineer

from .agent_expert import get_k8s_expert
from .state import State


def main():
    graph_builder = StateGraph(State)

    # Add the nodes
    graph_builder.add_node("k8s_expert", get_k8s_expert)
    graph_builder.add_node("k8s_engineer", get_k8s_engineer)
    graph_builder.add_node("k8s_tool_node", k8s_tool_node)

    # Add the edges
    graph_builder.add_edge(START, "k8s_expert")
    graph_builder.add_edge("k8s_expert", "k8s_engineer")
    graph_builder.add_edge("k8s_engineer", "k8s_tool_node")
    graph_builder.add_edge("k8s_tool_node", END)

    # Build the graph
    graph = graph_builder.compile()

    # Get input from the user
    input_text = input("Enter Request: ")
    for event in graph.stream({"messages": [input_text]}):
        # Loop over each key in events and print the messages
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key])
            print(event[key]["messages"][-1].content)