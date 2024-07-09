import os
from openai import OpenAI


def main():
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_URL"),
    )

    question = "What's my leisure calendar look like today?"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Call the right function to get the user's calendar events.",
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_calendar_events",
                    "description": 'Get the "work" or "personal" events from the user\'s calendar.',
                    "parameters": {
                        "calendar_type": {
                            "type": "string",
                            "description": 'The type of calendar to get events from. Can either be "work" or "personal" and nothing else.',
                        }
                    },
                },
            }
        ],
        model="Qwen1.5-32B-Chat",
        # model="Llama-3-8B-Instruct"
    )

    print("Function call: \n")
    print(chat_completion.choices[0].message.tool_calls)
