import os

from openai import OpenAI
from utils.client_manager import ClientManager


async def get_tasks(query: str, client_manager: ClientManager) -> str:
    """Get the tasks from the user"""
    client = OpenAI()

    information = []
    while True:
        messages = [
            {
                "role": "system",
                "content": "Carefully read the user's query. Check which tool to call based on the user's query. Call only one tool.",
            },
            {
                "role": "user",
                "content": f"""
    We need to answer the user's query. Gather all the information you need to answer the query. You can call only one tool at a time to gather information.

    Here's the information you have gathered so far:
    {information}

    Once all information has been gathered, summarize the information and return the answer to the user's query.
    
    ## User's query
    {query}

    """,
            },
        ]
        print("--------------------------------")
        print("Firing request")
        print("---")
        for message in messages:
            print(message["role"], ":", message["content"])
            print("-")
        print("---")
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            messages=messages,
            temperature=0.0,
            tools=list(client_manager.tools),
            # + [
            #     ChatCompletionToolParam(
            #         type="function",
            #         function={
            #             "name": "summarize_tasks",
            #             "description": "This should be the last tool to call. Only call this tool once all required information has been gathered.",
            #             "parameters": {
            #                 "type": "object",
            #                 "properties": {
            #                     "is_information_sufficient": {
            #                         "type": "boolean",
            #                     },
            #                 },
            #                 "required": ["is_information_sufficient"],
            #             },
            #         },
            #     ),
            # ],
        )
        print("Got a response")
        print("---")
        if (
            response.choices[0].message.tool_calls is None
            or len(response.choices[0].message.tool_calls) == 0
        ):
            return response.choices[0].message.content

        # Call the tool
        print(
            f"Calling tool: {response.choices[0].message.tool_calls[0].function.name}"
        )
        result = await client_manager.process_tool_call(
            response.choices[0].message.tool_calls
        )

        information.append(
            f"{response.choices[0].message.tool_calls[0].function.name} result: {result[0]}"
        )


def summarize(tasks: list[str]) -> str:
    """Summarize the tasks"""
    client = OpenAI()

    print("Summarizing tasks")
    print(f"Tasks: {tasks.join('\n---')}")
    response = client.chat.completions.create(
        model=os.getenv("MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant to summarize tasks. Summarize the tasks in a concise manner.",
            },
            {
                "role": "user",
                "content": f"Summarize the following tasks: {tasks.join('\n---')}",
            },
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
