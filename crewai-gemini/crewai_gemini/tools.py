from crewai_tools import tool
from yaml import dump


@tool("Get Meetings")
def get_meetings(date: str) -> str:
    """Get all the meetings scheduled for the provided date."""
    meetings = [
        {
            "title": "Give a talk on AI",
            "date": date,
            "start_time": "10:00 AM",
            "end_time": "11:00 AM",
            "participants": ["GDG Vancouver", "Noorain", "A wonderful audience"],
        },
        {
            "title": "Seminar: How to make friends",
            "date": date,
            "start_time": "2:00 PM",
            "end_time": "3:00 PM",
            "participants": ["Lonely people"],
        },
    ]
    # Tool logic here
    return "meetings:\n" + dump(meetings)
