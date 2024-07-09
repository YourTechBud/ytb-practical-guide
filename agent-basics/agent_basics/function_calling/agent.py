import json
import os
from numpy import rec
from typing_extensions import Annotated
from autogen import ConversableAgent, register_function


def get_calendar_events(
    calendar_type: Annotated[
        str,
        "The type of calendar to get events from. Can either be 'work' or 'personal' and nothing else.",
    ]
) -> Annotated[str, "The events from the user's calendar."]:
    arr = [
        {
            "event": "Talk about why Pikachu is the best Pokemon",
            "time": "10:00 AM",
            "location": "Office",
            "type": "work",
        },
        {
            "event": "Binge watch the last season of Demon Slayer",
            "time": "1:00 PM",
            "location": "Cafe",
            "type": "work",
        },
        {
            "event": "Write code for the AI Agent presentation",
            "time": "7:00 PM",
            "location": "Home",
            "type": "personal",
        },
    ]

    # Filter out the events based on calendar_type
    filtered_arr = [event for event in arr if event["type"] == calendar_type]

    # Pretty print to Json
    return "Events:\n" + json.dumps(filtered_arr, indent=4)


config_list = [
    {
        "model": "Qwen1.5-32B-Chat",
        # "model": "Llama-3-8B-Instruct",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "base_url": os.environ.get("OPENAI_API_URL"),
        "cache_seed": None,
    }
]

# Let's create the agents
user = ConversableAgent(
    "user",
    llm_config=False,
    human_input_mode="NEVER",  # Never ask for human input.
)

calander_bro = ConversableAgent(
    name="calander_bro",
    system_message="Call the right function to get the user's calendar events.",
    llm_config={
        "config_list": config_list,
    },
    code_execution_config=False,
    is_termination_msg=lambda msg: "events" in msg["content"].lower(),
    human_input_mode="NEVER",
)

executor = ConversableAgent(
    name="executor",
    llm_config=False,
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: "events" in msg["content"].lower(),
)


# Register the functions to the agents
register_function(
    get_calendar_events,
    caller=calander_bro,
    executor=executor,
    name="get_calendar_events",
    description='Get the "work" or "personal" events from the user\'s calendar.',
)

calander_bro.register_nested_chats(
    trigger=lambda sender: sender is not executor,
    chat_queue=[
        {
            "sender": executor,
            "recipient": calander_bro,
            "summary_msg": "last_msg",
        }
    ],
)

def main():
    user.initiate_chat(
        calander_bro, message="What's my leisure calendar look like today?", max_turns=1
    )


