class TaskMatcherResult {
  is_task_present bool
  identified_task string?
}

function MatchTask(task: string, tasks: string[], instructions: string?) -> TaskMatcherResult {
  client OpenRouter_Gemma3_12B
  prompt #"
    {% if instructions %}
      {{ instructions }}
    {% endif %}

    {{ctx.output_format}}

    {{ _.role("user") }}
    # TASK
    {{task}}

    # TASK_LIST
    {% for t in tasks %}
    - {{t}}
    {% endfor %}
  "#
}

test MatchTask_taskPresent {
  functions [MatchTask]
  args {
    task "Remind me to buy groceries"
    tasks ["walk the dog", "buy groceries", "clean the house"]
    instructions "Determine if the specified TASK is present in the TASK_LIST."
  }
}

test MatchTask_taskAbsent {
  functions [MatchTask]
  args {
    task "Finish the report"
    tasks ["walk the dog", "buy groceries", "clean the house"]
    instructions "Determine if the specified TASK is present in the TASK_LIST."
  }
}