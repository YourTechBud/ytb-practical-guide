import os
from typing import Optional

import lancedb
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def perform_vector_search(query: str, pokemon: Optional[str] = None, top_k: int = 5):
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    tbl = db.open_table("pokemon_moves")

    # Create the embedding for the query
    embedding_client = OpenAIEmbeddings(model=os.getenv("EMBEDDINGS_MODEL", ""))
    embedding = embedding_client.embed_query(query)

    # Perform the vector search
    query_builder = tbl.search(embedding).limit(top_k).select(["content", "metadata"])
    if pokemon is not None:
        query_builder = query_builder.where(f"metadata.filename = '{pokemon}'")

    results = query_builder.to_list()
    return results


def perform_fts_search(query: str, pokemon: Optional[str] = None, top_k: int = 5):
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    tbl = db.open_table("pokemon_moves")

    query_builder = (
        tbl.search(query, query_type="fts").limit(top_k).select(["content", "metadata"])
    )
    if pokemon is not None:
        query_builder = query_builder.where(
            f"metadata.filename = '{pokemon.lower()}'", prefilter=True
        )
    results = query_builder.to_list()
    return results


def build_context_from_results(results):
    return "---\n".join(
        [
            f"Title: {result['metadata']['filename']}\nContent:\n{result['content']}\n"
            for result in results
        ]
    )


def recursive_text_splitter(data, chunk_size, overlap_size):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents(
        [f"{text["filename"]}\n{text["content"]}" for text in data],
        metadatas=[dict({"filename": text["filename"]}) for text in data],
    )
    return texts


def markdown_splitter(data, chunk_size, overlap_size):
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
        strip_headers=True,
    )

    md_splits = [md_splitter.split_text(text["content"]) for text in data]

    # Make sure we add the filename to the metadata
    for i, page in enumerate(md_splits):
        for split in page:
            split.metadata["filename"] = data[i]["filename"]

    # Flatten the list of lists
    md_splits = [split for sublist in md_splits for split in sublist]

    # Don't forget to contraint split size
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_documents(md_splits)


def read_files_as_object_array(directory_path):
    """
    Reads all files in the specified directory and returns their contents as an array of objects.

    Each object contains the filename and the content of the file.

    Args:
        directory_path (str): Path to the directory containing the files.

    Returns:
        list: A list of dictionaries, where each dictionary has 'filename' and 'content' keys.
    """
    object_array = []

    # Iterate through all files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)

        # Skip directories, process only files
        if os.path.isfile(file_path):
            try:
                # Read the content of the file
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Append the file name and content as an object to the array
                object_array.append({"filename": file_name, "content": content})
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    return object_array
