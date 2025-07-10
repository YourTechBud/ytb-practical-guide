// Defining a data model.
class ProjectManagerActionToolCall {
  action "tool_call" @description("Call a tool to get the calendar events.")
  tool ProjectManagerListProjectsTool | ProjectManagerGetProjectTasksTool
}

class ProjectManagerListProjectsTool {
  name "list_all_projects" @description("Get the list of projects.")
}

class ProjectManagerGetProjectTasksTool {
  name "get_project_tasks" @description("Get the list of tasks for a given project.")
  args ProjectManagerGetProjectTasksToolArgs
}

class ProjectManagerGetProjectTasksToolArgs {
  project_id string @description("The id of the project to get the tasks for.")
}

function ProjectManagerNextAction(context: string) -> ProjectManagerActionToolCall | AgentActionEnd | AgentActionInputRequired {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client Gemini_2_5_Flash
  prompt #"
    Identify the next action to take based on the provided context

    # Instructions
    - Break down the user's request into smaller steps if needed.
    - Project ids are not human readable. You need to list all projects to get the project id.
    - Once the user's request is complete, you should end the conversation with an answer. The answer should be in a human readable markdown format.
    - If you do not have enough information to complete the user's request, you should ask the user for the missing information. Be clear about the missing information.
    
    # Context
    {{ context }}

    # Output format
    {{ ctx.output_format }}
    
    Print step by step reasoningbefore outputting the result in JSON format.
  "#
}

test pm_agent_GetProjectTasks {
  functions [ProjectManagerNextAction]
  args {
    context #"
      List all tasks for project mewto
    "#
  }
}