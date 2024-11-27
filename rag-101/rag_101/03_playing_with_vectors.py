import os
import numpy as np
from openai import OpenAI

from rag_101.utils import compute_cosine_similarity

# Let's start by creating an openai client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE_URL"),
)


def main():
    # Generate some sample data
    data = [
        "Pikachu is the best pokemon",
        "Fire type moves are absolutely badass and amazing!",
        "Subscribe to my YouTube channel",
    ]

    # Generate embeddings for all of them
    print("Generating embeddings...")
    embeddings = client.embeddings.create(input=data, model="gte-large-en-v1.5")
    print("Embeddings generated!")

    # Input prompt
    prompt = "Name a nice poket monster"

    # Generate the prompt's embedding
    print("Generating prompt embedding...", prompt)
    prompt_embedding = client.embeddings.create(input=prompt, model="gte-large-en-v1.5")
    print("Prompt embedding generated!")

    # Convert the np arrays
    embeddings = np.array([item.embedding for item in embeddings.data])
    prompt_embedding = np.array(prompt_embedding.data[0].embedding)

    # Compute cosine similarity
    similarities = compute_cosine_similarity(embeddings, prompt_embedding)
    
    # Print the results
    print("Similarities:")
    for i, sim in enumerate(similarities):
        print(f"[{i}]: {sim}")