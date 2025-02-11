import os

from dotenv import load_dotenv
from openai import OpenAI

from client import get_task_status, submit_crawl

load_dotenv()

# Create an openai client
openai = OpenAI()


def main():
    response = submit_crawl(
        urls=["https://pokemondb.net/pokedex/pikachu/moves/3"],
        priority=1,
        css_selector="div.sv-tabs-panel.active .grid-row > .grid-col:first-of-type",
    )
    status = get_task_status(response.task_id)

    if status and status.results:
        print("Original markdown:")
        print(status.results[0].markdown)
        print("--------------------------------")
        result = openai.chat.completions.create(
            model=os.getenv("MODEL_MEDIUM", "gpt-4o-mini"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": (
                        "Replace all the tables with bullet list. Also remove all links and styling(bold, italic, underline, etc). Retain the headers.\n"
                        + "Don't loose any important information:\n\n"
                        + str(status.results[0].markdown)
                    ),
                },
            ],
        )
        print("Summarized markdown:")
        print(result.choices[0].message.content)
    else:
        print(status.error)


if __name__ == "__main__":
    main()
