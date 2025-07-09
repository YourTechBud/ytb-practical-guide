from operator import call
import uuid
from datetime import datetime
from typing import Optional

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai.types import Content

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


async def before_agent_callback(
    callback_context: CallbackContext
) -> Optional[Content]:
    # TODO: Get this from user preferences db
    user_preferences = "Always ask for confirmation before scheduling an event with a very high effort. Only schedule events during weekdays. All meeetings should be during first 4 hours of the day."

    # TODO: Set the real date here
    date_today = "2025-06-23 Monday, 12 AM"

    # Update the state object
    callback_context.state["user_preferences"] = user_preferences
    callback_context.state["date_today"] = date_today

    print(f"State: {callback_context.state}")

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
    instruction="""You are a helpful agent who can list and schedule calendar events.
    # Instructions
    - We are not allowed to schedule events in the past.
    - Once the user's request is complete, you should end the conversation with an answer. The answer should be in a human readable markdown format.
    - Suggest time to schedule events based on the user's preferences if not specified.
    - Pay special attention to the user's preferences. User may provide additional instructions in the User preferences section.
    - Always list events for the next few days before to make sure we avoid duplicates and conflicts.

    # Effort Mapping
    - very-high: 4 hours or more
    - high: 2 hours or more
    - medium: 1 hour or more
    - low: 30 minutes or more
    - very-low: less than 30 minutes

    # Today's date
    {date_today}
    
    # User preferences
    {user_preferences}\
    
    # Output format
    - Make sure the output is in a human readable markdown format.
    - Make sure all dates are properly formatted in human readable format.
    """,
    before_agent_callback=before_agent_callback,
    tools=[list_events, schedule_event],
)
