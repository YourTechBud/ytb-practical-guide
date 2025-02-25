function TaskToolBasic(prompt: string) -> AddTask | GetTasks | MarkTaskAsDone {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client LLAMA3_1_8B
  prompt #"
    Based on the user's message, return the appropriate tool to use.

    {{ _.role("user") }}
    Call the appropriate tool based on the user's message.
    If the user has done something, mark the task as done.

    User message: {{ prompt }}
    
    {{ ctx.output_format }}
    Give step by step reasoning before giving the final answer in JSON format. 
  "#
}

test read_all_tasks {
  functions [TaskToolBasic]
  args {
    prompt "Give me all my tasks"
  }
}

test add_task {
  functions [TaskToolBasic]
  args {
    prompt "Remind me to buy groceries"
  }
}

test mark_task_as_done {
  functions [TaskToolBasic]
  args {
    prompt "I already got my groceries"
  }
}