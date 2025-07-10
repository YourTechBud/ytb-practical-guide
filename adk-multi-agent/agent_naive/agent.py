from google.adk.agents import Agent

from agent_calendar_manager.agent import list_events, schedule_event
from agent_project_manager.agent import get_project_tasks, list_all_projects

root_agent = Agent(
    name="assitant",
    model="gemini-2.5-flash",
    description=(
        "Agent to manage and retrieve information about projects and their tasks and manage the user's calendar"
    ),
    instruction=(
        "You are a helpful agent who can manage the user's calendar and projects and their tasks.\n"
        "Try to break down the tasks into smaller steps if needed.\n\n"
        "Always provide the output in human readable markdown format. Include all the information in the output."
    ),
    tools=[list_all_projects, get_project_tasks, list_events, schedule_event],
)
