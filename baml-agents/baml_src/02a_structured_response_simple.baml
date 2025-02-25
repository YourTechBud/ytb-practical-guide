class Intent {
  intent "addTasks" | "listTasks" | "markTaskAsDone" | "unknown"
}

function ClassifyIntentSimple(user_message: string) -> Intent {
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
  "#
}

test add_task {
  functions [ClassifyIntentSimple]
  args {
    user_message "I need to study how to use BAML to build a Graph based Knowledge Base"
  }
}

test list_tasks {
  functions [ClassifyIntentSimple]
  args {
    user_message "List my tasks"
  }
}

test mark_task_as_done {
  functions [ClassifyIntentSimple]
  args {
    user_message "I got my groceries"
  }
}
