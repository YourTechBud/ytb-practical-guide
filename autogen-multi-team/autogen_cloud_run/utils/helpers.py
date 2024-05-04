import subprocess
from os import listdir
from typing import Annotated


def list_files_in_directory(
    directory: Annotated[str, "The directory to list files in"]
) -> str:
    try:
        # Read all the files in the directory and return the output as a string
        files = listdir(directory)

        # Loop over all files and concatenate them into a single string
        output = ""
        for file in files:
            output += file + "\n"

        return "Directory listing:\n" + output
    except FileNotFoundError:
        return "Unable to list files."


def read_file(file_path: Annotated[str, "The path of the file to read"]) -> str:
    try:
        # Read the content of the file and return it as a string
        with open(file_path, "r") as file:
            content = file.read()

        return "File content:\n" + content
    except FileNotFoundError:
        return "Unable to read file."


def write_file(
    file_path: Annotated[str, "The relative path of the file to write"],
    content: Annotated[str, "Content to be written"],
) -> str:
    # Create a file with the provided content. Make sure to overwrite the file if it already exists.
    with open(file_path, "w") as file:
        file.write(content)

    return f"File created successfully at {file_path}."


def execute_command(
    command: Annotated[str, "The command to execute"],
    dir: Annotated[
        str,
        "The relative path of the directory where the command needs to be executed.",
    ],
) -> str:
    # Execute the provided command and return the output as a string
    process = subprocess.Popen(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=dir,
    )

    # Stream the output line by line
    if process.stdout:
        for line in process.stdout:
            print(line, end="")

    exit_code = process.wait()
    if exit_code != 0 and process.stderr:
        # If an error occurred, print the error stream content
        print("An error occurred:", process.stderr.read())

    # Close the streams
    if process.stdout:
        process.stdout.close()

    if process.stderr:
        process.stderr.close()

    return f"Command `{command}` executed successfully."
