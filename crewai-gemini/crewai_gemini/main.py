from crewai import Agent, Task, Crew, Process
from .tools import get_meetings


def main():
    # Create an agent for the calendar tool
    calendar = Agent(
        role="Calendar Tool",
        goal="Get the meetings scheduled for {date}",
        verbose=True,
        backstory=(
            "Identify which day the user wants to know the meetings for. "
            "Convert the identified date to  the RFC3339 date and time format."
        ),
        allow_delegation=False,
        tools=[get_meetings],
    )

    # Create an agent for the writer
    writer = Agent(
        role="Writer",
        goal="Provide notes on the meetings scheduled",
        verbose=True,
        backstory=(
            "Identify the key points from the meetings"
            "Provide pointers to help the user prepare and improve for the meetings."
        ),
        allow_delegation=False,
    )

    # Create the tasks for the agents
    calendar_task = Task(
        description=("Get me all the meetings for today"),
        expected_output="List of meetings. Each meeting should have a title, date, start time, end time, and participants.",
        agent=calendar,
    )

    write_task = Task(
        description=("Help me prepare for my meetings."),
        expected_output="Preparation notes for each meeting to helm the user conduct a great meeting.",
        agent=writer,
    )

    # Create the crew and kickoff the process
    crew = Crew(
        agents=[calendar, writer],
        tasks=[calendar_task, write_task],
        process=Process.sequential,  # Optional: Sequential task execution is default
        max_rpm=100,
        share_crew=True,
    )

    result = crew.kickoff(inputs={"date": "4th May 24"})
    print(result)
