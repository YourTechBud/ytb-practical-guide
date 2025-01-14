from langgraph.graph import StateGraph, START, END

from k8s_bot.agents.bot import get_bot
from k8s_bot.state_k8s import K8sState


def get_graph():
    # Make a graph builder
    graph_builder = StateGraph(K8sState)

    # Add the nodes
    graph_builder.add_node("bot", get_bot)

    # Add the edges
    graph_builder.add_edge(START, "bot")
    graph_builder.add_edge("bot", END)

    # Return the graph
    return graph_builder.compile()

def main():
    # Get the graph
    graph = get_graph()

    # Get user request
    user_request = input("Enter your request: ")

    # Make the initial state
    initial_state = K8sState({"messages": [user_request]})

    # Run the graph
    for event in graph.stream(initial_state):
        # Loop over each key in events and print the messages
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)
        