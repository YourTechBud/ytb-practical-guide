import asyncio

import yaml
from utils.client_manager import ClientManager


async def main():
    client_manager = ClientManager()
    client_manager.load_servers("servers.yaml")

    await client_manager.connect_to_server()

    print(yaml.dump(client_manager.tools))
    await client_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
