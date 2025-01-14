import os
from dataclasses import dataclass
from typing import Annotated

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
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


# Define our PydanticAI agent
@dataclass
class MyDeps:
    userid: str


pydantic_agent = Agent(
    model=OpenAIModel(os.getenv("MODEL_MEDIUM", "")),
    system_prompt="You are a helpful AI assistant",
    deps_type=MyDeps,
)


@pydantic_agent.tool
def get_tasks(ctx: RunContext[MyDeps]) -> str:
    """
    Get the user's tasks
    """
    return read_tasks(ctx.deps.userid)


# Define our agent node
def agent(state: State):
    query = state["messages"][-1].content

    # Invoke the model
    result = pydantic_agent.run_sync(query, deps=MyDeps(userid=state["userid"]))
    return {"messages": [AIMessage(content=result.data)]}


# Define our graph
def create_graph():
    graph_builder = StateGraph(State)

    # Add all the nodes
    graph_builder.add_node("agent", agent)
    # Add the edges
    graph_builder.add_edge(START, "agent")
    graph_builder.add_edge("agent", END)

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
