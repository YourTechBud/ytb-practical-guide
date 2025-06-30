import uuid
from datetime import datetime
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai.types import ModelContent, Part

from baml_client.async_client import b

events = []

events.append(
    {
        "event_id": str(uuid.uuid4()),
        "title": "Team Sync",
        "time_start": "2025-06-23T10:00:00",
        "time_end": "2025-06-23T11:00:00",
    }
)
events.append(
    {
        "event_id": str(uuid.uuid4()),
        "title": "Project X Deep Dive",
        "time_start": "2025-06-24T14:00:00",
        "time_end": "2025-06-24T16:00:00",
    }
)
events.append(
    {
        "event_id": str(uuid.uuid4()),
        "title": "Client Demo",
        "time_start": "2025-06-25T09:30:00",
        "time_end": "2025-06-25T10:30:00",
    }
)
events.append(
    {
        "event_id": str(uuid.uuid4()),
        "title": "Code Review Session",
        "time_start": "2025-06-26T11:00:00",
        "time_end": "2025-06-26T12:00:00",
    }
)
events.append(
    {
        "event_id": str(uuid.uuid4()),
        "title": "Sprint Planning",
        "time_start": "2025-06-27T10:00:00",
        "time_end": "2025-06-27T12:00:00",
    }
)


def list_events(start_time: str, end_time: str) -> dict:
    """Returns a list of events within the given time frame.

    Args:
        start_time (str): The start of the time frame (ISO format: YYYY-MM-DDTHH:MM:SS).
        end_time (str): The end of the time frame (ISO format: YYYY-MM-DDTHH:MM:SS).

    Returns:
        dict: status and a list of events or an error message.
    """
    try:
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
    except ValueError:
        return {
            "status": "error",
            "error_message": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS.",
        }

    if start_dt >= end_dt:
        return {
            "status": "error",
            "error_message": "Start time must be before end time.",
        }

    filtered_events = []
    for event in events:
        event_start_dt = datetime.fromisoformat(event["time_start"])
        event_end_dt = datetime.fromisoformat(event["time_end"])

        # Check for overlap: [start_dt, end_dt] overlaps with [event_start_dt, event_end_dt]
        if not (event_end_dt <= start_dt or event_start_dt >= end_dt):
            filtered_events.append(event)

    return {"status": "success", "events": filtered_events}


def schedule_event(title: str, time_start: str, time_end: str) -> dict:
    """Schedules a new event, checking for conflicts.

    Args:
        title (str): The title of the event.
        time_start (str): The start time of the event (ISO format: YYYY-MM-DDTHH:MM:SS).
        time_end (str): The end time of the event (ISO format: YYYY-MM-DDTHH:MM:SS).

    Returns:
        dict: status and the scheduled event or an error message.
    """
    try:
        start_dt = datetime.fromisoformat(time_start)
        end_dt = datetime.fromisoformat(time_end)
    except ValueError:
        return {
            "status": "error",
            "error_message": "Invalid date format. Use YYYY-MM-DDTHH:MM:SS.",
        }

    if start_dt >= end_dt:
        return {
            "status": "error",
            "error_message": "Start time must be before end time.",
        }

    for event in events:
        event_start_dt = datetime.fromisoformat(event["time_start"])
        event_end_dt = datetime.fromisoformat(event["time_end"])

        # Check for conflict: new event overlaps with an existing event
        if not (end_dt <= event_start_dt or start_dt >= event_end_dt):
            return {
                "status": "error",
                "error_message": "Conflict: New event overlaps with an existing event.",
                "event": event,
            }

    event_id = str(uuid.uuid4())
    new_event = {
        "event_id": event_id,
        "title": title,
        "time_start": time_start,
        "time_end": time_end,
    }
    events.append(new_event)
    return {"status": "success", "event": new_event}


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
    baml_response = await b.CalendarNextAction(
        context=context,
        additional_instructions="Always ask for confirmation before scheduling an event with a very high effort. Only schedule events during weekdays.",
        date_today="Monday, 23rd June 2025",
    )

    if baml_response.action == "tool_call":
        return LlmResponse(
            content=ModelContent(
                parts=[
                    Part.from_function_call(
                        name=baml_response.tool.tool,
                        args=baml_response.tool.args.model_dump(),
                    )
                ]
            )
        )

    if baml_response.action == "end":
        return LlmResponse(
            content=ModelContent(parts=[Part.from_text(text=baml_response.answer)])
        )

    if baml_response.action == "input_required":
        callback_context.state["input_required"] = True
        callback_context.state["input_required_prompt"] = baml_response.prompt
        return LlmResponse(
            content=ModelContent(parts=[Part.from_text(text=baml_response.prompt)])
        )

    return None


root_agent = Agent(
    name="calendar_manager",
    model="gemini-2.5-flash",
    description=(
        "Agent to manage and retrieve information about calendar events. Sample queries:\n"
        "- List all events between 2025-06-23 and 2025-06-27.\n"
        "- Schedule a new event named 'Team Sync' for tomorrow at 10:00 AM.\n"
        "- Schedule all these events: [List of events]\n"
        "- List all events for the next 7 days.\n"
    ),
    instruction="You are a helpful agent who can list and schedule calendar events.",
    tools=[list_events, schedule_event],
    before_model_callback=before_model_callback,
)
