import os

from openai import OpenAI
from utils.structured_responses import extract_json


def classify_intent(query: str) -> str:
    """Classify the intent of the query"""
    client = OpenAI()
    response = client.chat.completions.create(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that classifies the intent of the user's query.",
            },
            {
                "role": "user",
                "content": f"""
        Identify the action the user wants to perform in the following message: ${query}
        The allowed actions are : readTasks, newTask, markTaskAsDone

        If the user mentions that they have done something, mark the task as done.
        
        Provide the response in the following format: 
        ## Justification
        <Step by step reasoning>

        ## Response
        {{"action": "[action]"}}
""",
            },
        ],
    )
    return extract_json(response.choices[0].message.content)["action"]
