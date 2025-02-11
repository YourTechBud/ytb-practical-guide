from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

# Load environment variables
load_dotenv()


@dataclass
class FirstNode(BaseNode[None, None, str]):
    userid: str

    async def run(self, ctx: GraphRunContext[None, None]) -> End[str]:
        print("Inside the first node\n---\n")

        # Create a langchain model
        llm = ChatOpenAI(model=os.getenv("MODEL_SMALL", ""))

        # Define a system message
        system_message = SystemMessage(
            "You are a helpful AI assistant.\n"
            "Always use the user's name in the response: " + self.userid
        )

        # Define the messages
        messages = [system_message, HumanMessage(content="what's up?")]
        result = await llm.ainvoke(messages)

        # We just validated type safety here
        return End(result.content)  # type: ignore


async def main():
    userid = "YourTechBud"

    # Create a graph with the FirstNode
    graph = Graph(nodes=[FirstNode])

    # Run the graph
    result, history = await graph.run(start_node=FirstNode(userid=userid))
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
