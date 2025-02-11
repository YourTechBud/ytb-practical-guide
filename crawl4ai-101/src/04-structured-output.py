import json
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from client import get_task_status, submit_crawl
from client.models import ExtractionConfig, ExtraParams

load_dotenv()


def main():
    # Define the schema for the structured output
    schema = {
        "name": "Moves",
        "fields": [
            {
                "name": "move",
                "selector": "h3:first-of-type",
                "type": "text",
            }
        ],
    }
    extra_params = ExtraParams(
        extraction_config=ExtractionConfig(type="json_css", params={"schema": schema})
    )
    response = submit_crawl(
        urls=["https://pokemondb.net/pokedex/pikachu/moves/3"],
        priority=1,
        extra=extra_params,
        css_selector="div.sv-tabs-panel.active .grid-row > .grid-col:first-of-type",
    )
    status = get_task_status(response.task_id)

    if status and status.results:
        # Initialize BeautifulSoup with your HTML. You can use "html.parser" or "lxml" if installed.
        soup = BeautifulSoup(str(status.results[0].cleaned_html), "lxml")

        # Extract Pokémon name and game from the first section's paragraph.
        level_up_h3 = soup.find("h3", string="Moves learnt by level up")
        if not level_up_h3:
            print("No level up moves found")
            return
        level_up_p = level_up_h3.find_next("p")
        if not level_up_p:
            print("No level up paragraph found")
            return
        pokemon_name = level_up_p.find("em").text.strip()  # type: ignore

        # Use a regular expression to capture the game name from the paragraph text.
        game_match = re.search(r"in (.*?) at the", level_up_p.get_text())
        game_name = game_match.group(1) if game_match else ""

        # Initialize the output data structure.
        data = {
            "pokemon": pokemon_name,
            "game": game_name,
            "sections": {},
            "egg_moves_navigation": [],
        }
        # --- Parse "Moves learnt by level up" ---
        level_up_table = level_up_h3.find_next("div").find("table")
        level_up_moves = extract_moves(
            level_up_table, ["level", "move", "type", "category", "power", "accuracy"]
        )
        data["sections"]["level_up"] = {
            "title": level_up_h3.get_text(strip=True),
            "description": level_up_p.get_text(strip=True),
            "moves": level_up_moves,
        }

        # --- Parse "Egg moves" ---
        egg_moves_h3 = soup.find("h3", string="Egg moves")
        egg_moves_p = egg_moves_h3.find_next("p")  # type: ignore
        egg_moves_table = egg_moves_h3.find_next("div").find("table")  # type: ignore
        egg_moves = extract_moves(
            egg_moves_table, ["move", "type", "category", "power", "accuracy"]
        )
        data["sections"]["egg_moves"] = {
            "title": egg_moves_h3.get_text(strip=True),
            "description": egg_moves_p.get_text(strip=True),
            "moves": egg_moves,
        }

        # --- Parse "Pre-evolution moves" ---
        pre_evo_h3 = soup.find("h3", string="Pre-evolution moves")
        pre_evo_p = pre_evo_h3.find_next("p")  # type: ignore
        pre_evo_table = pre_evo_h3.find_next("div").find("table")
        pre_evo_moves = extract_moves(
            pre_evo_table, ["move", "type", "category", "power", "accuracy", "method"]
        )
        data["sections"]["pre_evolution"] = {
            "title": pre_evo_h3.get_text(strip=True),
            "description": pre_evo_p.get_text(strip=True),
            "moves": pre_evo_moves,
        }

        # --- Parse Egg moves navigation ---
        nav = soup.find("nav")
        if nav:
            for li in nav.find("ul").find_all("li"):
                a = li.find("a")
                data["egg_moves_navigation"].append({"name": a.get_text(strip=True)})

        print(json.dumps(data, indent=2))
    else:
        print(status.error)


# --- Helper function to extract moves from a table ---
def extract_moves(table, columns):
    moves = []
    tbody = table.find("tbody")
    for tr in tbody.find_all("tr"):
        cells = tr.find_all("td")
        move_data = {}
        for idx, col in enumerate(columns):
            cell = cells[idx]
            # Process based on column name.
            if col == "level":
                move_data["level"] = int(cell.get_text(strip=True))
            elif col == "move":
                a = cell.find("a")
                move_data["move"] = {
                    "name": a.get_text(strip=True),
                    "title": a.get("title", ""),
                }
            elif col == "type":
                a = cell.find("a")
                move_data["type"] = {"name": a.get_text(strip=True)}
            elif col == "category":
                img = cell.find("img")
                move_data["category"] = (
                    img["alt"] if img and img.has_attr("alt") else ""
                )
            elif col in ("power", "accuracy", "method"):
                move_data[col] = cell.get_text(strip=True)
        moves.append(move_data)
    return moves


if __name__ == "__main__":
    main()
