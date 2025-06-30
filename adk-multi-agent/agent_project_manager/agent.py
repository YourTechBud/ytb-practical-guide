from google.adk.agents import Agent


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
    tools=[list_all_projects, get_project_tasks],
)
