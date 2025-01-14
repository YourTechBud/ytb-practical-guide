import os
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt.tool_node import ToolNode
from typing_extensions import TypedDict

from utils.tasks import read_tasks

load_dotenv()


# Define our state
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

    # Confidential stuff
    userid: str


# Define our tool
@tool
def retrieve_tasks(userid: str) -> str:
    """
    Returns all the tasks for the user.
    """
    return read_tasks(userid)


tools = [retrieve_tasks]

tool_node = ToolNode(tools)


# Define our agent node
def agent(state: State):
    # Create a langchain model
    llm = ChatOpenAI(model=os.getenv("MODEL_SMALL", "")).bind_tools(tools)

    # Define a system message
    system_message = SystemMessage(
        f"You are a helpful AI assistant. The user's id is {state['userid']}"
    )

    # Define the messages
    messages = [system_message] + state["messages"]

    # Invoke the model
    return {"messages": [llm.invoke(messages)]}


# Define our graph
def create_graph():
    graph_builder = StateGraph(State)

    # Add all the nodes
    graph_builder.add_node("agent", agent)
    graph_builder.add_node("executor", tool_node)
    # Add the edges
    graph_builder.add_edge(START, "agent")
    graph_builder.add_edge("agent", "executor")
    graph_builder.add_edge("executor", END)

    return graph_builder.compile()


# Our main function
def main():
    graph = create_graph()

    # Confidential stuff
    userid = "YourTechBud"

    query = input("Your query: ")

    initial_state = {"messages": [HumanMessage(content=query)], "userid": userid}

    for event in graph.stream(initial_state):
        for key in event:
            print("\n*******************************************\n")
            print(key + ":")
            print("---------------------\n")
            print(event[key]["messages"][-1].content)


if __name__ == "__main__":
    main()
