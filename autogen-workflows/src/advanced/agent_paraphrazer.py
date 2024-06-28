import autogen


def get_paraphrazer(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """You are a helpful AI content editor. 
The user will provide you a note along with a summary.
Rewrite that note and make sure you cover everything in the note. Do not include the title. The output must obey the following "RULES":

"RULES":
- Output must be in markdown.
- Make sure you use each points provided in summary as headers.
- Each header must start with `##`.
- Headers are not bullet points.
- Each header can optionally have a list of bullet points. Don't put bullet points if the header has no content.
- Strictly use "-" to start bullet points.
- Optionally make an additional header named "Addional Info" to cover points not included in the summary. Use "Addional Info" header for unclassified points.
- Identify and correct spelling & grammatical mistakes."""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Paraphrazer",
        llm_config=base_llm_config,
        system_message=system_message,
    )

# def get_paraphrazer(base_llm_config: dict):
#     # A system message to define the role and job of our agent
#     system_message = """You are a helpful AI assistant. 
#     The user will provide you a note. Proof read that note. The output must obey the following "RULES":

#     "RULES":
#     - Output must be in markdown.
#     - The output must be grammatically correct.
#     - Reformat the note into releavant sections.
#     """

#     # Create and return our assistant agent
#     return autogen.AssistantAgent(
#         name="Paraphrazer",
#         llm_config=base_llm_config,
#         system_message=system_message,
#     )

