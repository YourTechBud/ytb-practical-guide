from mcp.server.fastmcp import FastMCP
from utils.starlette import create_starlette_app
from utils.tasks import add_task as add_task_to_file
from utils.tasks import mark_task_as_done as mark_task_as_done_in_file
from utils.tasks import read_tasks

mcp = FastMCP("Task Manager")


@mcp.tool()
def get_tasks() -> str:
    """Get all tasks"""
    return read_tasks("YourTechBud")


@mcp.tool()
def add_task(task: str) -> str:
    """Add a task"""
    return add_task_to_file("YourTechBud", task)


@mcp.tool()
def mark_task_as_done(task: str) -> str:
    """Mark a task as done"""
    return mark_task_as_done_in_file("YourTechBud", task)


if __name__ == "__main__":
    import uvicorn

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(
        mcp._mcp_server, api_key="secret-key1", debug=True
    )

    uvicorn.run(starlette_app, host="localhost", port=8010)
