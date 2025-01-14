from langchain_core.messages import SystemMessage, HumanMessage

from k8s_bot.helpers import extract_json, get_model
from k8s_bot.state_user_input import UserInputState


def get_input_verifier(state: UserInputState):
    # Create the system message
    system_message = SystemMessage(
        """You are a helpful ai assistant.
Carefully read the user's question and identify what the user is asking for. Describe the nature of the question briefly.
Does the answer to this question require interaction with a K8s cluster? Only questions which require talking to a K8s cluster are valid.
Provide the final answer in a JSON format with a boolean field "requireKubernetesInteraction" and text field "usersQuestion"."""
    )

    # Get the LLM model
    model = get_model("Llama-3.1-8B-Instruct")

    # Return the LLM response
    messages = [system_message, HumanMessage(state["question"])] 

    # Get the json data from the response
    response_content = model.invoke(messages).content
    if isinstance(response_content, str):
        data = extract_json(response_content)
    else:
        raise ValueError("Expected response content to be a string")
    
    return {"is_valid": data["requireKubernetesInteraction"], "question": data["usersQuestion"], "verifier_response": response_content}