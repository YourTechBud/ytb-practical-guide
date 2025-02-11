from client import get_task_status, submit_crawl


def main():
    response = submit_crawl(
        urls=["https://pokemondb.net/pokedex/pikachu/moves/3"],
        priority=1,
        css_selector="div.sv-tabs-panel.active .grid-row > .grid-col:first-of-type",
    )
    status = get_task_status(response.task_id)

    if status and status.results:
        print(status.results[0].markdown)
    else:
        print(status.error)


if __name__ == "__main__":
    main()
