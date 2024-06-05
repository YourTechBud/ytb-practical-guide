import argparse
from email import message

from tf_plan_explainer.agent_tf_summarizer import get_tf_summarizer
from tf_plan_explainer.agent_user import get_user


def main(planPath: str):
    # First lets load the plan file
    f = open(planPath, "r")
    plan = f.read()

    print(plan)

    # build the gpt_configuration object
    base_llm_config = {
        "config_list": [
            {
                "model": "mistal-openorca",
                "api_key": "dont-copy-this",
                "base_url": "http://localhost:8000/api/v1",
            }
        ],
        "temperature": 0,
    }

    tf_summarizer = get_tf_summarizer(base_llm_config)
    user = get_user()

    user.initiate_chat(tf_summarizer, clear_history=True, message=plan)


if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Program to talk with Kubernetes.")

    # Add all server arguments
    parser.add_argument("-p", "--plan", type=str, help="Path of the plan.")

    # Parse the arguments
    args = parser.parse_args()
    main(args.plan)
