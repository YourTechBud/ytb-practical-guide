import os

import lancedb
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from utils import read_files_as_object_array, recursive_text_splitter

# Load environment variables
load_dotenv()

# Create an openai client
embeddings_model = os.getenv("EMBEDDINGS_MODEL", "")
embeddings_client = OpenAIEmbeddings(model=embeddings_model)


def main():
    # Read the files
    print("Reading files...")
    object_array = read_files_as_object_array("./data")

    # Split the markdown files into chunks
    splits = recursive_text_splitter(object_array, 3000, 100)

    # Prepare an array of string from the documents
    splits_as_string = [
        f"{doc.metadata.get('filename', '')}\n{doc.page_content}\n" for doc in splits
    ]

    # Compute the embeddings
    print("Computing embeddings...")
    embeddings = embeddings_client.embed_documents(splits_as_string, chunk_size=512)

    # Save the embeddings to libsql
    print("Saving embeddings to database...")
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    db.drop_table("pokemon_moves")  # Drop the table if it exists

    # Insert the embeddings into the database
    data = []
    for i, embedding in enumerate(embeddings):
        data.append(
            {
                "vector": embedding,
                "content": splits[i].page_content,
                "metadata": splits[i].metadata,
            }
        )

    # Create the table and full text search index
    tbl = db.create_table("pokemon_moves", data=data)
    tbl.create_fts_index("content", use_tantivy=False)


if __name__ == "__main__":
    main()
