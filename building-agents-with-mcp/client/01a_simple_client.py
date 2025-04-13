import asyncio
from contextlib import AsyncExitStack
from typing import Any, Optional

import yaml
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client

load_dotenv()  # load environment variables from .env


class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url

        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_sse_server(self):
        """Connect to an MCP server running with SSE transport"""
        # Store the context managers so they stay alive
        self._streams_context = sse_client(url=self.server_url)
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        self.session = await self._session_context.__aenter__()

        # Initialize
        await self.session.initialize()

        # List available tools to verify connection
        response = await self.session.list_tools()
        tools = response.tools
        for tool in tools:
            print("Name:", tool.name)
            print("Description:", tool.description)
            print("---")
            print(yaml.dump(tool.inputSchema))

        # Store all tools in openai compatible format
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools
        ]

    async def call_tool(self, tool_name: str, tool_input: dict[str, Any] | None):
        """Call a tool with the given name and input"""

        if self.session is None:
            raise ValueError("Session not initialized")

        response = await self.session.call_tool(tool_name, tool_input)
        return response

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)


async def main():
    client = MCPClient(server_url="http://localhost:8010/sse")
    try:
        await client.connect_to_sse_server()

        print("Calling tool...")
        response = await client.call_tool(tool_name="get_tasks", tool_input=None)
        if response.content[0].type == "text":
            print(response.content[0].text)
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
