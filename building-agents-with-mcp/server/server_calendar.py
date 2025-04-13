import yaml
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from utils.starlette import create_starlette_app

load_dotenv()


mcp = FastMCP("Calendar")


@mcp.tool()
def get_events() -> str:
    """Get all calendar events for today"""
    return yaml.dump(
        [
            {
                "title": "MCP Stream",
                "start": "2025-04-02T10:00:00",
                "end": "2025-04-02T11:00:00",
            },
            {
                "title": "Hate on Python",
                "start": "2025-04-02T11:00:00",
                "end": "2025-04-02T12:00:00",
            },
        ]
    )


if __name__ == "__main__":
    import uvicorn

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(
        mcp._mcp_server, api_key="secret-key2", debug=True
    )

    uvicorn.run(starlette_app, host="localhost", port=8020)
