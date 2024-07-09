from autogen import ConversableAgent

from autogen_multi_team.utils.config_list import get_config_list


def get_cloud_run_deploy_agent(llm_config: dict):
    llm_config = llm_config.copy()
    llm_config["config_list"] = get_config_list()
    llm_config["temperature"] = 0.2
    agent = ConversableAgent(
        name="Cloud_Run_Deploy",
        system_message="""Write a command to deploy the image to google cloud run. Use the SAMPLE_COMMAND for reference. Make sure to also include the directory the command needs to be run from.
Make sure you generate the output in the provided OUTPUT_FORMAT.

SAMPLE_COMMAND:
 ```
# This command will deploy the image to google cloud run
gcloud run deploy [APP_NAME] --allow-unauthenticated --region us-east1 --image [IMAGE_NAME]
```
APP_NAME is the name of the app that you want to deploy.
IMAGE_NAME is the name of the image that you pushed to the container registry.

OUTPUT_FORMAT:

Command:
[gcloud run deploy command goes here]

Directory:
[relative project root path goes here]""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return agent
