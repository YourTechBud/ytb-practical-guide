from sys import api_version
from kubernetes import config, dynamic
from kubernetes.client import api_client
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


class GetResourcesInput(BaseModel):
    api_version: str = Field(description="The api version is the group along with version that defines the resource")
    kind: str = Field(description="The kind is the type of resource that you want to get")


class KubernetesAdaptor:
    def __init__(self) -> None:
        # Creating a dynamic kubernetes client
        self.client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_kube_config())
        )

    @tool("get_k8s_resource_list")
    def get_resources(self, api_version: str, kind: str) -> str:
        """Get the list of resources from the provided api version and kind"""
        # Get an API object for the provide resource
        api = self.client.resources.get(api_version=api_version, kind=kind)

        # Query kubernetes
        list = api.get()

        # Print the response
        print("===")
        print("Response from K8s:")
        for r in map(
            lambda r: {
                "kind": r.kind,
                "namespace": r.metadata.namespace,
                "name": r.metadata.name,
            },
            list.items,
        ):
            print(r)
        print("===")

        # Return termination message
        return "Done"

