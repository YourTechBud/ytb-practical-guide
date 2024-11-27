import os
import numpy as np
from openai import OpenAI

from rag_101.utils import compute_cosine_similarity, find_top_k, read_files_as_string_array, recursive_text_splitter

# Let's start by creating an openai client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE_URL"),
)


def main():
    # Read all markdown files in the ./data directory
    data = read_files_as_string_array("./data")

    # Split the data into smaller chunks
    print("Splitting data...")
    data = recursive_text_splitter(data, 2048, 200)
    print("Data splitted!")

    # Generate embeddings for all of them
    print("Generating embeddings...")
    embeddings = client.embeddings.create(input=data, model="gte-large-en-v1.5")
    print("Embeddings generated!")

    # Input prompt
    prompt = "Gimme a list of Pikachu's electric attacks."
    # prompt = "Which pokemons can learn growl?"

    # Generate the prompt's embedding
    print("Generating prompt embedding...", prompt)
    prompt_embedding = client.embeddings.create(input=prompt, model="gte-large-en-v1.5")
    print("Prompt embedding generated!")

    # Convert the np arrays
    embeddings = np.array([item.embedding for item in embeddings.data])
    prompt_embedding = np.array(prompt_embedding.data[0].embedding)

    # Compute cosine similarity
    similarities = compute_cosine_similarity(embeddings, prompt_embedding)

    # Pick out the top 5 most similar chunks
    results = find_top_k(data, similarities, 5)
    
    # Print the results
    print("Retrieval results:")
    for item in results:
        print("")
        print("----------------------------------------")
        print("")
        print(item[0], item[1])
        print("")
        print("----------------------------------------")
        print("")

    print("Time to call the model")
    context = "\n\n".join([item[1] for item in results]) 
    prompt = f"""{prompt}

    Answer the user's question with the following information:
    {context}
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="Qwen-2.5-32B-Instruct",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Give a descriptive answer to the user's question. Don't use tables in response."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    # Print the response
    print(response.choices[0].message.content)