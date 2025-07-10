from typing import Optional, Union, Any

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai.types import ModelContent, Part

from baml_client.async_client import b
from baml_client.types import ProjectManagerGetProjectTasksTool, ProjectManagerListProjectsTool, AgentActionEnd, AgentActionInputRequired, ProjectManagerActionToolCall

def list_all_projects() -> dict:
    """Returns a list of all available projects.

    Returns:
        dict: status and a list of projects or an error message.
    """
    projects = [
        {
            "project_id": "proj-001",
            "title": "Website Redesign",
            "description": "Redesigning the company website for better user experience.",
        },
        {
            "project_id": "proj-002",
            "title": "Mobile App Development",
            "description": "Developing a new mobile application for iOS and Android.",
        },
        {
            "project_id": "proj-003",
            "title": "Catch Wild Mewtwo",
            "description": "Embark on an epic quest to locate and capture the legendary Mewtwo.",
        },
    ]
    return {"status": "success", "projects": projects}


def get_project_tasks(project_id: str) -> dict:
    """Returns a list of tasks for a given project ID.

    Args:
        project_id (str): The ID of the project to retrieve tasks for.

    Returns:
        dict: status and a list of tasks or an error message.
    """
    tasks = {
        "proj-001": [
            {
                "task_id": "task-001",
                "title": "Design mockups",
                "description": "Create wireframes and mockups for the new website.",
                "effort": "high",
            },
            {
                "task_id": "task-002",
                "title": "Develop front-end",
                "description": "Implement the user interface using React.",
                "effort": "medium",
            },
        ],
        "proj-002": [
            {
                "task_id": "task-003",
                "title": "Backend API development",
                "description": "Develop RESTful APIs for the mobile application.",
                "effort": "high",
            },
            {
                "task_id": "task-004",
                "title": "iOS app development",
                "description": "Develop the iOS version of the mobile application.",
                "effort": "high",
            },
            {
                "task_id": "task-005",
                "title": "Android app development",
                "description": "Develop the Android version of the mobile application.",
                "effort": "medium",
            },
        ],
        "proj-003": [
            {
                "task_id": "task-006",
                "title": "Research Mewtwo's Location",
                "description": "Gather intelligence on Mewtwo's last known whereabouts and potential hiding spots.",
                "effort": "high",
            },
            {
                "task_id": "task-007",
                "title": "Assemble Elite Team",
                "description": "Recruit and train a specialized team of trainers and Pokémon for the capture mission.",
                "effort": "high",
            },
            {
                "task_id": "task-008",
                "title": "Prepare Capture Equipment",
                "description": "Acquire and prepare necessary items like Master Balls, recovery items, and battle gear.",
                "effort": "medium",
            },
            {
                "task_id": "task-009",
                "title": "Execute Capture Mission",
                "description": "Track, engage, and capture Mewtwo using strategic battle plans.",
                "effort": "very-high",
            },
        ],
    }

    if project_id in tasks:
        return {"status": "success", "tasks": tasks[project_id]}
    else:
        return {
            "status": "error",
            "error_message": f"Tasks for project '{project_id}' not found.",
        }

async def before_model_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    context = ""

    for content in llm_request.contents:
        if not content.parts:
            continue

        for part in content.parts:
            if part.text:
                context += f"{content.role}: {part.text}\n\n"
                continue

            if (
                part.function_response
                and part.function_response.name != "transfer_to_agent"
            ):
                context += f"{content.role}: {part.function_response.response}\n\n"

    # Fire BAML request
    baml_response = await b.ProjectManagerNextAction(
        context=context,
    )

    if isinstance(baml_response, ProjectManagerActionToolCall):
        print(f"Tool call: {baml_response.tool}")
        tool_args: dict[str, Any] = {}
        if isinstance(baml_response.tool, ProjectManagerGetProjectTasksTool):
            tool_args = baml_response.tool.args.model_dump()
        
        function_call_parts = []
        function_call_parts.append(Part.from_function_call(
            name=baml_response.tool.name,
            args=tool_args,
        ))

        return LlmResponse(
            content=ModelContent(
                parts=function_call_parts
            )
        )

    if isinstance(baml_response, AgentActionEnd):
        return LlmResponse(
            content=ModelContent(parts=[Part.from_text(text=baml_response.result)])
        )

    if isinstance(baml_response, AgentActionInputRequired):
        callback_context.state["input_required"] = True
        callback_context.state["input_required_prompt"] = baml_response.prompt
        return LlmResponse(
            content=ModelContent(parts=[Part.from_text(text=baml_response.prompt)])
        )

    return None


root_agent = Agent(
    name="project_manager",
    model="gemini-2.5-flash",
    description=(
        "Agent to manage and retrieve information about projects and their tasks. Sample queries:\n"
        "- List all projects.\n"
        "- List all tasks for project (project id, name or description)\n"
    ),
    instruction=(
        "You are a helpful agent who can list projects and their tasks.\n"
        "Try to break down the tasks into smaller steps if needed.\n\n"
        "Always provide the output in human readable markdown format. Include all the information in the output."
    ),
    before_model_callback=before_model_callback,
    tools=[list_all_projects, get_project_tasks],
)
