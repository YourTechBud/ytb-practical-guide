import os
from pydoc import text
from re import M
import numpy as np
import tiktoken
from sklearn.metrics.pairwise import cosine_similarity
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter


def compute_cosine_similarity(embeddings, prompt_embedding):
    """
    Computes the cosine similarity between a prompt embedding and an array of embeddings.

    Args:
        embeddings (np.ndarray): A 2D array where each row is an embedding (shape: [N, D]).
        prompt_embedding (np.ndarray): A 1D array representing the prompt embedding (shape: [D]).

    Returns:
        np.ndarray: A 1D array of cosine similarity scores (shape: [N]).
    """
    # Ensure prompt_embedding is reshaped for pairwise comparison
    prompt_embedding = np.array(prompt_embedding).reshape(1, -1)

    # Compute cosine similarities between the prompt and each embedding in the array
    similarities = cosine_similarity(embeddings, prompt_embedding).flatten()

    return similarities


def read_files_as_string_array(directory_path):
    """
    Reads all files in the specified directory and returns their contents as a string array.

    Args:
        directory_path (str): Path to the directory containing the files.

    Returns:
        list: A list of tuples, where each tuple is the file name and the content of a file.
    """
    string_array = []

    # Iterate through all files in the directory
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)

        # Skip directories, process only files
        if os.path.isfile(file_path):
            try:
                # Read the content of the file
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Append the file content to the string array
                string_array.append(content)
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    return string_array


def recursive_text_splitter(data, chunk_size, overlap_size):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents(data)
    return [text.page_content for text in texts]

def markdown_splitter(data, chunk_size, overlap_size):
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "h1"), ("##", "h2"), ("###", "h3")],
        strip_headers=True,
    )
    
    md_splits = [md_splitter.split_text(text) for text in data]
    md_splits = [split for sublist in md_splits for split in sublist]

    # Don't forget to contraint split size
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
        length_function=len,
        is_separator_regex=False,
    )

    return prepend_metadata_to_content(text_splitter.split_documents(md_splits))

def prepend_metadata_to_content(elements):
    """
    Takes an array of elements and constructs a string for each element 
    by prepending metadata values (h1, h2, h3) to page_content.

    Args:
        elements (list of dict): Array of elements with 'page_content' and 'metadata'.

    Returns:
        list of str: An array of strings with metadata prepended to the page content.
    """
    result = []

    for element in elements:
        # Extract metadata and page content
        metadata = element.metadata
        page_content = element.page_content

        # Prepend h1, h2, and h3 if they exist
        parts = [
            metadata.get('h1', ''), 
            metadata.get('h2', ''), 
            metadata.get('h3', ''),
            page_content
        ]

        # Join non-empty parts with a space
        combined_content = "\n".join(part for part in parts if part)
        result.append(combined_content)

    return result

def find_top_k(strings, numbers, top_k):
    """
    Finds the top N numbers and their corresponding strings.

    Args:
        strings (list of str): Array of string values.
        numbers (list of float or int): Array of numerical values.
        top_n (int): Number of top entries to find.

    Returns:
        list of tuple: A list of (number, string) pairs sorted by the top numbers in descending order.
    """
    if len(strings) != len(numbers):
        raise ValueError("The arrays 'strings' and 'numbers' must have the same length.")
    
    # Combine strings and numbers into a list of tuples
    combined = list(zip(numbers, strings))

    # Sort the combined list by numbers in descending order
    sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # Get the top N entries
    top_entries = sorted_combined[:top_k]

    return top_entries