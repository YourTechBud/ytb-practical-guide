from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai.types import Content


async def run_agent(ctx: InvocationContext, agent: BaseAgent, content: Content):
    runner = Runner(
        app_name=agent.name,
        agent=agent,
        session_service=InMemorySessionService(),
    )

    session = await runner.session_service.create_session(
        app_name=agent.name,
        user_id="tmp_user",
        state=ctx.session.state,
    )

    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=content
    ):
        if event.actions.state_delta:
            ctx.session.state.update(event.actions.state_delta)

        yield event
