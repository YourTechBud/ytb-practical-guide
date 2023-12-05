import json
from kubernetes import config, dynamic
from kubernetes.client import api_client


class KubernetesAdaptor:
    def __init__(self) -> None:
        # Creating a dynamic kubernetes client
        self.client = dynamic.DynamicClient(
            api_client.ApiClient(configuration=config.load_kube_config())
        )

    def get_resources(self, api_version: str, kind: str) -> str:
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
