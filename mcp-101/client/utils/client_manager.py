import json

import yaml
from openai.types.chat import ChatCompletionMessageToolCall, ChatCompletionToolParam
from utils.client import MCPClient


class ClientManager:
    """Manage multiple MCP clients"""

    def __init__(self):
        self.clients: list[MCPClient] = []
        self.tools: list[ChatCompletionToolParam] = []
        self.tool_map: dict[str, MCPClient] = {}

    def load_servers(self, servers_file: str):
        """Load servers from a file"""
        with open(servers_file, "r") as f:
            servers = yaml.safe_load(f)

        for server in servers["servers"]:
            self._add_server(server["name"], server["url"], server["api_key"])

    async def connect_to_server(self):
        """Connect to an MCP server running with SSE transport"""
        for client in self.clients:
            await client.connect_to_sse_server()

        # Store all tools in openai compatible format
        for client in self.clients:
            self.tools.extend(client.tools)

            for tool in client.tools:
                self.tool_map[tool.get("function").get("name")] = client

    def get_tools(self):
        """Get all tools in openai compatible format"""
        return self.tools

    async def process_tool_call(self, tool_calls: list[ChatCompletionMessageToolCall]):
        """Process a tool call"""
        results = []
        for tool_call in tool_calls:
            print("Processing tool call", tool_call.function.name)
            obj = json.loads(tool_call.function.arguments)
            client = self.tool_map[tool_call.function.name]
            result = await client.call_tool(tool_call.function.name, obj)
            results.append(result.content[0].text)

        return results

    async def cleanup(self):
        """Cleanup all clients"""
        for client in self.clients:
            await client.cleanup()

    def _add_server(self, name: str, server_url: str, api_key: str):
        """Add a client to the manager"""
        client = MCPClient(name, server_url, api_key)
        self.clients.append(client)
