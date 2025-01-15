from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from k8s_bot import graph_k8s, graph_user_input


class MainState(TypedDict):
    messages: Annotated[list, add_messages]


def get_human_input(state: MainState):
    print("\n###########################################")
    print("RUNNING HUMAN INPUT SUBGRAPH")
    question = graph_user_input.main()
    print("END")
    print("###########################################\n")
    return {"messages": [HumanMessage(content=question)]}


def get_k8s_response(state: MainState):
    print("\n###########################################")
    print("RUNNING K8S SUBGRAPH")
    response = graph_k8s.run(state["messages"][-1].content)
    print("END")
    print("###########################################\n")
    return {"messages": [AIMessage(content=response)]}


def get_graph():
    graph_builder = StateGraph(MainState)

    # Add the nodes
    graph_builder.add_node("input", get_human_input)
    graph_builder.add_node("k8s", get_k8s_response)

    # Add the edges
    graph_builder.add_edge(START, "input")
    graph_builder.add_edge("input", "k8s")
    graph_builder.add_edge("k8s", END)

    # Build the graph
    return graph_builder.compile()


def main():
    graph = get_graph()

    initial_input = {"messages": []}
    for event in graph.stream(initial_input):
        # Loop over each key in events and print the messages
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)
