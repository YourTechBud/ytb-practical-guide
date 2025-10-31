class IntentAddTask {
  action "AddTask"
  task string
}

class IntentGetTasks {
  action "GetTasks"
  filter "ALL" | "PENDING" | "DONE" @description(#"
    Filter for the tasks to retrieve. Defaults to "ALL".
  "#)
}

class IntentDeleteTask {
  action "DeleteTask"
  task string 
}

class IntentMarkTaskAsDone {
  action "MarkTaskAsDone"
  task string 
}

class IntentUnknown {
  action "Unknown"
  reason string
}

function ClassifyIntent(query: string, instructions: string?) -> IntentAddTask | IntentGetTasks | IntentDeleteTask | IntentMarkTaskAsDone | IntentUnknown {
  client Gemini_2_0_Flash_Lite
  prompt #"
    {% if instructions %}
      {{ instructions }}
    {% endif %}

    {{ctx.output_format}}

    {{ _.role("user") }}
    # Query:
    {{query}}
  "#
}

test ClassifyIntent_markTaskAsDone1 {
  functions [ClassifyIntent]
  args {
    query "I bought my groceries"
    instructions "Identify the intended action from the user's query."
  }
}

test ClassifyIntent_deleteTask {
  functions [ClassifyIntent]
  args {
    query "I don't need groceries"
    instructions "Identify the intended action from the user's query."
  }
}