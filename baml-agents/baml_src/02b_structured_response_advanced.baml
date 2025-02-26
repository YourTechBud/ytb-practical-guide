class IntentAddTask {
  intent "addTasks" @description("The user wants to do something add a task to the list.")
  taskTitle string 
}

class IntentListTasks {
  intent "listTasks" @description("The user wants to list tasks.")
  filter string @description("The filter can be 'done' or 'pending'")
}

class IntentMarkTaskAsDone {
  intent "markTaskAsDone" @description("The user has done something or wants to mark a task as done.")
}

class IntentUnknown {
  intent "unknown" @description("The user's message is not clear or invalid.")
}

function ClassifyIntentAdvanced(user_message: string, messages: Message[]) -> IntentAddTask | IntentListTasks | IntentMarkTaskAsDone | IntentUnknown {
  client LLAMA3_1_8B

  prompt #"
    Identify the user's intent from the provided message. Follow the rules below:
    - Action will be "unknown" for all unknow invalid messages.
    - If the user has done something, mark the task as done.
    - If the user wants to do something, add the task to the list.

    {{ ctx.output_format }}
    Give step by step reasoning before giving the final answer in JSON format.
    Select only a single action from the list of actions.

    {{ _.role("user") }}
    User's Message: {{ user_message }}

    {{ PrintMessages(messages) }}
  "#
}
