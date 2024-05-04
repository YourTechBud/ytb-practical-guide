from autogen import ConversableAgent


def get_toolchain_detector_agent(llm_config: dict):
    llm_config = llm_config.copy()
    llm_config["temperature"] = 0.2
    agent = ConversableAgent(
        name="Toolchain_Detector",
        system_message="""Based on the files present in the directory and contents of the file, detect which the tool that was used to build and run the project.

List all the possible tools (like pnpm, npm, yarn, etc) that could be used to build and run the project.
Provide step by step reasoning for not selecting each tool. Reasoning should be based on the files present in the directory and contents of the file.
Select only one single tool and explain the reason for selecting the tool.
Finaly identify the commands that should be used to build and run the project.
Provide the output strictly in the OUTPUT_FORMAT.

OUTPUT_FORMAT:

List of Possible Tools: 
[list of tools goes here]

Step by Step Reasoning for all rejected tool: 
[reasoning goes here]

Step by Step Reasoning for selected tool: 
[reasoning goes here]

Tool Detected: 
[name of the tool/command goes here - example pnpm, npm, yarn, etc]

Build command: 
[command to build the project goes here]

Run command for production: 
[command to run the project goes here]
""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return agent
