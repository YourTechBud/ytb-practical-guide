"""Define a simple chatbot agent.

This agent returns a predefined response without using an actual LLM.
"""

from langgraph.graph import END, START, StateGraph

from agent.helpers.intent_classifier import (
    ADD_TASK,
    GET_TASKS,
    MARK_TASK_AS_DONE,
    intent_classifier_agent,
)
from agent.helpers.task_manager import TaskManagementDeps, task_management_agent
from agent.helpers.task_reader import create_task_reader_graph
from agent.helpers.title_matcher import TitleMatcherDeps, title_matcher_agent
from agent.state import OverallState


# Define intent classifier node
async def intent_classifier(state: OverallState):
    result = await intent_classifier_agent.run(state["query"])
    print("Intent classifier result:")
    print(result.data)
    return {"intent": result.data.action}


# Define title matcher node
async def title_matcher(state: OverallState):
    result = await title_matcher_agent.run(
        state["query"], deps=TitleMatcherDeps(userid=state["userid"])
    )
    print("Title matcher result:")
    print(result.data)
    return {
        "title": result.data.title,
        "is_title_present": result.data.is_title_present,
    }


# Define task mutator node
async def task_adder(state: OverallState):
    result = await task_management_agent.run(
        state["query"], deps=TaskManagementDeps(userid=state["userid"])
    )
    print("Task adder result:")
    print(result.data)
    return {"output": result.data}


# Define the task updater node
async def task_updater(state: OverallState):
    query = f"Mark task '{state['title']}' as done"
    print("Task updater query:")
    print(query)
    result = await task_management_agent.run(
        query, deps=TaskManagementDeps(userid=state["userid"])
    )
    print("Task updater result:")
    print(result.data)
    return {"output": result.data}


# Define the graph output node
def output(state: OverallState):
    print("Output:")
    print(state["output"])
    return {}


# All our conditional edges
def route_task(state: OverallState):
    if state["intent"] == ADD_TASK:
        return "task_adder"
    elif state["intent"] == MARK_TASK_AS_DONE:
        return "title_matcher"
    elif state["intent"] == GET_TASKS:
        return "task_reader"
    else:
        print("Invalid intent:")
        print(state["intent"])
        return END


def is_title_present(state: OverallState):
    if state["is_title_present"]:
        return "task_updater"
    else:
        print("Title not present")
        return END


# Define our graph
def create_graph():
    graph_builder = StateGraph(OverallState)

    # Get the graph of the task reader
    task_reader_graph = create_task_reader_graph()

    # Add all the nodes
    graph_builder.add_node("intent_classifier", intent_classifier)
    graph_builder.add_node("title_matcher", title_matcher)
    graph_builder.add_node("task_reader", task_reader_graph)
    graph_builder.add_node("task_adder", task_adder)
    graph_builder.add_node("task_updater", task_updater)
    graph_builder.add_node("outputer", output)

    # Add the edges
    graph_builder.add_edge(START, "intent_classifier")
    graph_builder.add_conditional_edges(
        "intent_classifier",
        route_task,
        ["title_matcher", "task_adder", "task_reader", END],
    )
    graph_builder.add_conditional_edges(
        "title_matcher",
        is_title_present,
        ["task_updater", END],
    )
    graph_builder.add_edge("task_adder", "outputer")
    graph_builder.add_edge("task_updater", "outputer")
    graph_builder.add_edge("task_reader", "outputer")
    graph_builder.add_edge("outputer", END)
    return graph_builder.compile()


# async def my_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
#     """Each node does work."""
#     configuration = Configuration.from_runnable_config(config)
#     # configuration = Configuration.from_runnable_config(config)
#     # You can use runtime configuration to alter the behavior of your
#     # graph.
#     return {
#         "changeme": "output from my_node. "
#         f"Configured with {configuration.my_configurable_param}"
#     }


# # Define a new graph
# workflow = StateGraph(State, config_schema=Configuration)

# # Add the node to the graph
# workflow.add_node("my_node", my_node)

# # Set the entrypoint as `call_model`
# workflow.add_edge("__start__", "my_node")

# # Compile the workflow into an executable graph
# graph = workflow.compile()
graph = create_graph()
graph.name = "Task Management"  # This defines the custom name in LangSmith
