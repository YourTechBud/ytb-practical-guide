from contextlib import AsyncExitStack
from typing import Any, Optional

from mcp import ClientSession
from mcp.client.sse import sse_client
from openai.types.chat import ChatCompletionToolParam


class MCPClient:
    def __init__(self, name: str, server_url: str, api_key: str):
        self.name = name
        self.server_url = server_url
        self.api_key = api_key

        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        self.tools: list[ChatCompletionToolParam] = []

    async def connect_to_sse_server(self):
        """Connect to an MCP server running with SSE transport"""
        # Store the context managers so they stay alive
        self._streams_context = sse_client(
            url=self.server_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        self.session = await self._session_context.__aenter__()

        # Initialize
        await self.session.initialize()

        # List available tools to verify connection
        response = await self.session.list_tools()
        tools = response.tools

        # Store all tools in openai compatible format
        self.tools = [
            ChatCompletionToolParam(
                type="function",
                function={
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema,
                },
            )
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
