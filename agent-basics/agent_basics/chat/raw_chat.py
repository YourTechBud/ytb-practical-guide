import os
from openai import OpenAI

def main():
    prev_result = """Events:
    [
        {
            "event": "Write code for the AI Agent presentation",
            "time": "7:00 PM",
            "location": "Home",
            "type": "personal"
        }
    ]"""

    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_URL"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a helpful AI assistant. You help the user prepare for her events.
    The user will provide you with a list of events. Provide suggested actions to help the user prepare for each event.
    - Add a field called 'suggestedActions' to each event in the list. Preserve the original event information.
    - Ouput stictly in YAML format.""",
            },
            {
                "role": "user",
                "content": "What's my leisure calendar look like today?",
            },
            {"role": "assistant", "content": prev_result},
        ],
        model="Qwen1.5-32B-Chat",
    )

    print(chat_completion.choices[0].message.content)
