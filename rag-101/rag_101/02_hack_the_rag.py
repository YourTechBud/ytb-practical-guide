import os
from openai import OpenAI

# Let's start by creating an openai client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE_URL"),
)

def main():
    # Example prompt
    prompt = "Gimme a list of Pikachu's electric attacks."

    # Get pikachu's information
    context = get_more_info(prompt)
    
    # Generate a new prompt
    prompt = f"""{prompt}

    Answer the user's question with the following information:
    {context}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    # Print the response
    print(response.choices[0].message.content)

def get_more_info(prompt: str):
    # Get the data from somewhere
    info = """
    ### Moves learnt by level up

_Pikachu_ learns the following moves in Pokémon Emerald at the levels specified.

| Lv. | Move | Type | Cat. | Power | Acc. |
| --- | --- | --- | --- | --- | --- |
| 1   | [Growl](/move/growl "View details for Growl") | [Normal](/type/normal) | ![Status](https://img.pokemondb.net/images/icons/move-status.png "Status") | —   | 100 |
| 1   | [ThunderShock](/move/thunder-shock "View details for ThunderShock") | [Electric](/type/electric) | ![Special](https://img.pokemondb.net/images/icons/move-special.png "Special") | 40  | 100 |
| 6   | [Tail Whip](/move/tail-whip "View details for Tail Whip") | [Normal](/type/normal) | ![Status](https://img.pokemondb.net/images/icons/move-status.png "Status") | —   | 100 |
| 8   | [Thunder Wave](/move/thunder-wave "View details for Thunder Wave") | [Electric](/type/electric) | ![Status](https://img.pokemondb.net/images/icons/move-status.png "Status") | —   | 100 |
| 11  | [Quick Attack](/move/quick-attack "View details for Quick Attack") | [Normal](/type/normal) | ![Physical](https://img.pokemondb.net/images/icons/move-physical.png "Physical") | 40  | 100 |
| 15  | [Double Team](/move/double-team "View details for Double Team") | [Normal](/type/normal) | ![Status](https://img.pokemondb.net/images/icons/move-status.png "Status") | —   | —   |
| 20  | [Slam](/move/slam "View details for Slam") | [Normal](/type/normal) | ![Physical](https://img.pokemondb.net/images/icons/move-physical.png "Physical") | 80  | 75  |
| 26  | [Thunderbolt](/move/thunderbolt "View details for Thunderbolt") | [Electric](/type/electric) | ![Special](https://img.pokemondb.net/images/icons/move-special.png "Special") | 95  | 100 |
| 33  | [Agility](/move/agility "View details for Agility") | [Psychic](/type/psychic) | ![Status](https://img.pokemondb.net/images/icons/move-status.png "Status") | —   | —   |
| 41  | [Thunder](/move/thunder "View details for Thunder") | [Electric](/type/electric) | ![Special](https://img.pokemondb.net/images/icons/move-special.png "Special") | 120 | 70  |
| 50  | [Light Screen](/move/light-screen "View details for Light Screen") | [Psychic](/type/psychic) | ![Status](https://img.pokemondb.net/images/icons/move-status.png "Status") | —   | —   |
"""
    return info