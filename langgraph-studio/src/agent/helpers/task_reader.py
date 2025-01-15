import operator
import os
from typing import Annotated

import yaml
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from typing_extensions import TypedDict

from agent.helpers.task_manager import TaskManagementDeps, task_management_agent

load_dotenv()


# Define our overall state
class OverallState(TypedDict):
    # Confidential stuff
    userid: str

    # Other stuff
    query: str
    tasks: list[str]
    enriched_tasks: Annotated[list, operator.add]
    output: str


# Define our task enrichment state
class TaskEnrichmentState(TypedDict):
    task: str


# Define our agent node
async def task_manager(state: OverallState):
    result = await task_management_agent.run(
        state["query"], deps=TaskManagementDeps(userid=state["userid"])
    )

    tasks_raw = yaml.safe_load(result.data)
    tasks = [task["title"] for task in tasks_raw if not task["isDone"]]

    print("Tasks:")
    print(tasks)

    return {"tasks": tasks}


# Define our task enrichment node
async def task_enricher(state: TaskEnrichmentState):
    # Create a langchain model
    llm = ChatOpenAI(model=os.getenv("MODEL_SMALL", ""))

    # Define a system message
    system_message = SystemMessage(
        "You are a helpful AI assistant. You are given a task and you need to enrich it with helpful quotes to motivate the user to complete it. Keep it short and concise."
    )

    # Define the messages
    messages = [
        system_message,
        HumanMessage(content=(f"Here's the task: {state['task']}")),
    ]

    # Invoke the model
    result = await llm.ainvoke(messages)
    print("---\nEnriched task:")
    print(result.content)
    return {"enriched_tasks": [result.content]}


# Define our task formatter node
async def task_formatter(state: OverallState):
    llm = ChatOpenAI(model=os.getenv("MODEL_SMALL", ""))

    # Define a system message
    system_message = SystemMessage(
        "You are a helpful AI assistant. You are given a list of tasks and you need to return a well formatted list."
    )

    # Create a string of the tasks
    tasks_str = "---\n".join(state["enriched_tasks"])

    # Define the messages
    messages = [
        system_message,
        HumanMessage(content=f"Here's the list of tasks:\n{tasks_str}"),
    ]

    result = await llm.ainvoke(messages)
    print("---\nFormatted tasks:")
    print(result.content)
    return {"output": result.content}


# Here we define the logic to map out each task to an enricher
# This will be an edge in the graph
def map_tasks_to_enricher(state: OverallState):
    # We will return a list of `Send` objects
    # Each `Send` object will have a `node` and `state`
    # The `node` will be the node to send the message to
    # The `state` will be the state to send to the node
    return [
        Send(node="task_enricher", arg=TaskEnrichmentState(task=task))
        for task in state["tasks"]
    ]


# Define our graph
def create_task_reader_graph():
    graph_builder = StateGraph(OverallState)

    # Add all the nodes
    graph_builder.add_node("task_manager", task_manager)
    graph_builder.add_node("task_enricher", task_enricher)
    graph_builder.add_node("task_formatter", task_formatter)

    # Add the edges
    graph_builder.add_edge(START, "task_manager")
    graph_builder.add_conditional_edges(
        "task_manager", map_tasks_to_enricher, ["task_enricher"]
    )
    graph_builder.add_edge("task_enricher", "task_formatter")
    graph_builder.add_edge("task_formatter", END)

    return graph_builder.compile()
