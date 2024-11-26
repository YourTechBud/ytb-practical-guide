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