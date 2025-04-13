import asyncio

import yaml
from agents.intent_classifier import classify_intent
from agents.task_manager import get_tasks
from dotenv import load_dotenv
from utils.client_manager import ClientManager

# Load environment variables
load_dotenv()


async def main():
    client_manager = ClientManager()
    client_manager.load_servers("servers.yaml")

    await client_manager.connect_to_server()

    query = input("Enter a query: ")
    intent = classify_intent(query)

    print(f"Intent: {intent}")

    match intent:
        case "readTasks":
            print("Reading tasks")
            tasks = await get_tasks(query, client_manager)
            print(yaml.dump(tasks))
        case "newTask":
            print("Creating a new task")
        case "markTaskAsDone":
            print("Marking task as done")

    await client_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
