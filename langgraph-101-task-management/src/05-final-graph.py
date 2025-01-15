from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from agents.intent_classifier import (
    ADD_TASK,
    GET_TASKS,
    MARK_TASK_AS_DONE,
    intent_classifier_agent,
)
from agents.task_manager import TaskManagementDeps, task_management_agent
from agents.task_reader import create_task_reader_graph
from agents.title_matcher import TitleMatcherDeps, title_matcher_agent

load_dotenv()


# Define our overall state
class OverallState(TypedDict):
    # Confidential stuff
    userid: str

    # User query
    query: str

    # Intent classifier result
    intent: str

    # Title matcher result
    title: str
    is_title_present: bool

    # Final output
    output: str


# Define our task enrichment state
class TaskEnrichmentState(TypedDict):
    task: str


# Define intent classifier node
def intent_classifier(state: OverallState):
    result = intent_classifier_agent.run_sync(state["query"])
    print("Intent classifier result:")
    print(result.data)
    return {"intent": result.data.action}


# Define title matcher node
def title_matcher(state: OverallState):
    result = title_matcher_agent.run_sync(
        state["query"], deps=TitleMatcherDeps(userid=state["userid"])
    )
    print("Title matcher result:")
    print(result.data)
    return {
        "title": result.data.title,
        "is_title_present": result.data.is_title_present,
    }


# Define task mutator node
def task_adder(state: OverallState):
    result = task_management_agent.run_sync(
        state["query"], deps=TaskManagementDeps(userid=state["userid"])
    )
    print("Task adder result:")
    print(result.data)
    return {"output": result.data}


# Define the task updater node
def task_updater(state: OverallState):
    query = f"Mark task '{state['title']}' as done"
    print("Task updater query:")
    print(query)
    result = task_management_agent.run_sync(
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


# Our main function
def main():
    graph = create_graph()

    # Confidential stuff
    userid = "YourTechBud"

    query = input("Your query: ")

    initial_state = {"query": query, "userid": userid}

    for event in graph.stream(initial_state):
        for key in event:
            print("\n-----------------------------------")
            print("Done with " + key)
            print("\n*******************************************\n")


if __name__ == "__main__":
    main()
