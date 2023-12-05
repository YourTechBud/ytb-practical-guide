import autogen
from agent_utils import is_termination_message
from k8s_adaptor import KubernetesAdaptor


def get_k8s_engineer(base_llm_config: dict, k8s_adaptor: KubernetesAdaptor):
    # Add the function signature to our llm config
    llm_config = base_llm_config.copy()
    llm_config["functions"] = [
        {
            "name": "get_k8s_resource_list",
            "description": "Get the list of resources from the provided api version and kind",
            "parameters": {
                "type": "object",
                "properties": {
                    "api_version": {
                        "type": "string",
                        "description": "The api version is the group along with version that defines the resource",
                    },
                    "kind": {
                        "type": "string",
                        "description": "The name of the resource that identifies the object",
                    },
                },
                "required": ["api_version", "kind"],
            },
        }
    ]

    # A system message to define the role and job of our agent
    system_message = "A Kubernetes Engineer. You fetch kubernetes resources based on the API Version and Kind Provided."

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Kubernetes_Engineer",
        llm_config=llm_config,
        system_message=system_message,
        function_map={
            "get_k8s_resource_list": k8s_adaptor.get_resources,
        },
        is_termination_msg=is_termination_message,
    )
