import asyncio
import os

from dotenv import load_dotenv
from openai import OpenAI
from utils.client_manager import ClientManager

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

model = os.getenv("MODEL", "gpt-4o-mini")


async def main():
    client_manager = ClientManager()
    client_manager.load_servers("servers.yaml")

    await client_manager.connect_to_server()

    # Create a chat completion
    # Assuming ChatCompletionToolParam is a class
    query = input("Enter a query: ")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": f"User's query: {query}"}],
        tools=client_manager.tools,
        tool_choice="auto",
        temperature=0.0,
    )

    results = await client_manager.process_tool_call(
        response.choices[0].message.tool_calls
    )

    print(results[0])

    await client_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
