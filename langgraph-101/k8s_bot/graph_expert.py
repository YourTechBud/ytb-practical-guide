from langgraph.graph import StateGraph, START, END

from k8s_bot.agents.engineer import get_k8s_engineer
from k8s_bot.agents.expert import get_k8s_expert
from k8s_bot.agents.k8s_tools import k8s_tool_node
from k8s_bot.state_k8s import K8sState

def get_graph():
    # Make a graph builder
    graph_builder = StateGraph(K8sState)

    # Add the nodes
    graph_builder.add_node("engineer", get_k8s_engineer)
    graph_builder.add_node("k8s_tool_node", k8s_tool_node)
    graph_builder.add_node("expert", get_k8s_expert)

    # Add the edges
    graph_builder.add_edge(START, "expert")
    graph_builder.add_edge("expert", "engineer")
    graph_builder.add_edge("engineer", "k8s_tool_node")
    graph_builder.add_edge("k8s_tool_node", END)

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