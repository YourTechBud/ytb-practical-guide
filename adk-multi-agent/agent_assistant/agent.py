from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from agent_calendar_manager.agent import root_agent as calendar_manager_agent
from agent_project_manager.agent import root_agent as project_manager_agent

calendar_agent = AgentTool(agent=calendar_manager_agent)
project_agent = AgentTool(agent=project_manager_agent)

root_agent = Agent(
    name="assistant",
    model="gemini-2.5-flash",
    description="I can help you with your tasks and projects.",
    # tools=[project_agent, calendar_agent],
    sub_agents=[project_manager_agent, calendar_manager_agent],
)
