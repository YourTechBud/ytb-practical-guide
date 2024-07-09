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

    prompt = f"""You are a helpful AI assistant. You help the user prepare for her events.
    The user will provide you with a list of EVENTS. Provide suggested actions to help the user prepare for each event.
    - Add a field called 'suggestedActions' to each event in the list. Preserve the original event information.
    - Ouput stictly in YAML format. 

    EVENTS:
    {prev_result}
    """


    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="Qwen1.5-32B-Chat",
    )

    print(chat_completion.choices[0].message.content)