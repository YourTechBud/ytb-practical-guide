from __future__ import annotations

import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from agents import intent_classifier
from agents.intent_classifier import intent_classifier_agent
from agents.task_manager import task_manager_agent
from agents.task_summarizer import task_summarizer_agent
from agents.title_matcher import title_matcher_agent
from utils.model import GraphDeps, GraphState

# Load environment variables
load_dotenv()


@dataclass
class ClassifierNode(BaseNode[GraphState, GraphDeps, str]):
    async def run(
        self, ctx: GraphRunContext[GraphState, GraphDeps]
    ) -> TaskManagerNode | TitleMatcherNode | End[str]:
        print("---\nInside the classifier node\n---\n")

        result = await intent_classifier_agent.run(ctx.deps.query)

        # Store the intent for future nodes
        ctx.state.intent = result.data.action

        print("Intent: ", ctx.state.intent)

        # Decide which node to run next
        match ctx.state.intent:
            case intent_classifier.GET_TASKS:
                return TaskManagerNode(query="Get my tasks")
            case intent_classifier.ADD_TASK:
                return TaskManagerNode(query=f"Add the task: '{ctx.deps.query}'")
            case intent_classifier.MARK_TASK_AS_DONE:
                return TitleMatcherNode()
            case _:
                return End("unknown")


@dataclass
class TitleMatcherNode(BaseNode[GraphState, GraphDeps, str]):
    async def run(
        self, ctx: GraphRunContext[GraphState, GraphDeps]
    ) -> TaskManagerNode | End[str]:
        print("---\nInside the title matcher node\n---\n")
        result = await title_matcher_agent.run(ctx.deps.query, deps=ctx.deps)

        print("Result: ", result.data)

        if not result.data.is_title_present:
            # You could loop back and ask the user for an input.
            return End("Unknown task provided")

        return TaskManagerNode(query=f"Mark the task '{result.data.title}' as done")


@dataclass
class TaskManagerNode(BaseNode[GraphState, GraphDeps, str]):
    query: str

    async def run(
        self, ctx: GraphRunContext[GraphState, GraphDeps]
    ) -> TaskSummarizerNode | End[str]:
        print("---\nInside the task manager node\n---\n")
        result = await task_manager_agent.run(self.query, deps=ctx.deps)

        print("Result: ", result.data)

        if ctx.state.intent == intent_classifier.GET_TASKS:
            return TaskSummarizerNode(data=result.data)

        return End(result.data)


@dataclass
class TaskSummarizerNode(BaseNode[GraphState, GraphDeps, str]):
    data: str

    async def run(self, ctx: GraphRunContext[GraphState, GraphDeps]) -> End[str]:
        print("---\nInside the task summarizer node\n---\n")

        query = f"Summarize these tasks in a concise and organized way:\n{self.data}"
        result = await task_summarizer_agent.run(query)
        return End(result.data)


async def main():
    query = input("Enter your query: ")

    # Create a graph
    graph = Graph(
        nodes=[ClassifierNode, TitleMatcherNode, TaskManagerNode, TaskSummarizerNode]
    )

    # Run the graph
    result, history = await graph.run(
        start_node=ClassifierNode(),
        state=GraphState(intent=""),
        deps=GraphDeps(id="YourTechBud", query=query),
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
