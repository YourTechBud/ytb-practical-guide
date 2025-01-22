from __future__ import annotations

import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from agents import intent_classifier
from agents.intent_classifier import intent_classifier_agent

# Load environment variables
load_dotenv()


@dataclass
class GraphState:
    intent: str


@dataclass
class ClassifierNode(BaseNode[GraphState, None, str]):
    query: str

    async def run(
        self, ctx: GraphRunContext[GraphState, None]
    ) -> GetTasksNode | MarkTaskAsDoneNode | End[str]:
        print("Inside the classifier node\n---\n")

        result = await intent_classifier_agent.run(self.query)

        # Store the intent for future nodes
        ctx.state.intent = result.data.action

        # Decide which node to run next
        match ctx.state.intent:
            case intent_classifier.GET_TASKS:
                return GetTasksNode()
            case intent_classifier.MARK_TASK_AS_DONE:
                return MarkTaskAsDoneNode()
            case _:
                return End("unknown")


@dataclass
class GetTasksNode(BaseNode[GraphState, None, str]):
    async def run(self, ctx: GraphRunContext[GraphState, None]) -> End[str]:
        print("Inside the get tasks node\n---\n")
        return End("get tasks")


@dataclass
class MarkTaskAsDoneNode(BaseNode[GraphState, None, str]):
    async def run(self, ctx: GraphRunContext[GraphState, None]) -> End[str]:
        print("Inside the mark task as done node\n---\n")
        return End("mark task as done")


async def main():
    # Create a graph
    graph = Graph(nodes=[ClassifierNode, GetTasksNode, MarkTaskAsDoneNode])

    # Run the graph
    result, history = await graph.run(
        start_node=ClassifierNode(query="Get me my tasks"),
        state=GraphState(""),
    )
    print(result)
    print("---")
    print([item.data_snapshot() for item in history])


if __name__ == "__main__":
    asyncio.run(main())
