from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events.event import Event
from google.adk.tools.agent_tool import AgentTool
from google.genai.types import ModelContent, Part, UserContent

from agent_assistant_custom.helpers import run_agent
from agent_calendar_manager.agent import root_agent as calendar_manager_agent
from agent_project_manager.agent import root_agent as project_manager_agent
from baml_client.async_client import b
from baml_client.type_builder import TypeBuilder

calendar_agent = AgentTool(agent=calendar_manager_agent)
project_agent = AgentTool(agent=project_manager_agent)


class AssistantAgent(BaseAgent):
    children: list[BaseAgent] = []

    def __init__(self, name: str, children: list[BaseAgent]):
        super().__init__(
            name=name,
        )
        self.children = children

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        print(f"[{self.name}] Starting assistant agent workflow.")

        while True:
            messages: list[Event] = [
                event
                for event in ctx.session.events
                if event.author == self.name or event.author == "user"
            ]

            context = ""

            for event in messages:
                content = event.content
                if not content or not content.parts:
                    continue

                for part in content.parts:
                    if part.text:
                        context += f"{content.role}: {part.text}\n\n"
                        continue

                    if (
                        part.function_response
                        and part.function_response.response
                        and part.function_response.response.get("agent")
                    ):
                        context += f"{part.function_response.response['agent']}: {part.function_response.response['response']}\n\n"

            tb = TypeBuilder()
            for agent in self.children:
                tb.AgentName.add_value(agent.name).description(agent.description)

            baml_response = await b.AssistantNextAction(context, {"tb": tb})

            if baml_response.action == "end":
                yield Event(
                    id=Event.new_id(),
                    invocation_id=ctx.invocation_id,
                    author=ctx.agent.name,
                    branch=ctx.branch,
                    content=ModelContent(
                        parts=[Part.from_text(text=baml_response.answer)]
                    ),
                )
                return

            if baml_response.action == "transfer_to_agent":
                agent = next(
                    (
                        agent
                        for agent in self.children
                        if agent.name == baml_response.agent
                    ),
                    None,
                )
                if agent is None:
                    raise ValueError(f"Agent {baml_response.agent} not found")

                content = UserContent(
                    parts=[
                        Part.from_text(
                            text=f"Tasks: {baml_response.tasks}\n\nContext: {baml_response.context}"
                        )
                    ],
                )

                yield Event(
                    id=Event.new_id(),
                    invocation_id=ctx.invocation_id,
                    author=ctx.agent.name,
                    branch=ctx.branch,
                    content=ModelContent(
                        parts=[
                            Part.from_function_call(
                                name="transfer_to_agent",
                                args={
                                    "agent": agent.name,
                                    "tasks": baml_response.tasks,
                                    "context": baml_response.context,
                                },
                            )
                        ]
                    ),
                )

                last_event = None
                async for event in run_agent(ctx, agent, content):
                    last_event = event
                    yield event

                if last_event:
                    if last_event.content and last_event.content.parts:
                        event_text = last_event.content.parts[0].text

                    yield Event(
                        id=Event.new_id(),
                        invocation_id=ctx.invocation_id,
                        author=ctx.agent.name,
                        branch=ctx.branch,
                        content=ModelContent(
                            parts=[
                                Part.from_function_response(
                                    name="transfer_to_agent",
                                    response={
                                        "status": "success",
                                        "agent": agent.name,
                                        "response": (
                                            event_text
                                            if event_text
                                            else "No response from agent."
                                        ),
                                    },
                                )
                            ]
                        ),
                    )

                continue

            if baml_response.action == "input_required":
                yield Event(
                    id=Event.new_id(),
                    invocation_id=ctx.invocation_id,
                    author=ctx.agent.name,
                    branch=ctx.branch,
                    content=ModelContent(
                        parts=[Part.from_text(text=baml_response.prompt)]
                    ),
                )

                return


root_agent = AssistantAgent(
    name="assistant",
    children=[
        calendar_manager_agent,
        project_manager_agent,
    ],
)
