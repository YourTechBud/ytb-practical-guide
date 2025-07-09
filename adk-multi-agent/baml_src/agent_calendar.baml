// Defining a data model.
class CalendarActionToolCall {
  action "tool_call" @description("Call a tool to get the calendar events.")
  tool CalendarListEventsTool | CalendarScheduleEventTool
}

class CalendarActionEnd {
  action "end" @description("End and exit the conversation with a summary.")
  answer string @description("Answer to the user's request in a polite and humble manner.")
}

class CalendarActionInputRequired {
  action "input_required" @description("User's input is required to continue.")
  prompt string @description("Prompt to the user to provide the missing information.")
}

class CalendarListEventsTool {
  tool "list_events" @description("Get the calendar events.")
  args CalendarListEventsToolArgs
}

class CalendarScheduleEventTool {
  tool "schedule_event" @description("Schedule a new event.")
  args CalendarScheduleEventToolArgs
}

class CalendarListEventsToolArgs {
  start_time string @description("The start of the time frame (ISO format: YYYY-MM-DDTHH:MM:SS).")
  end_time string @description("The end of the time frame (ISO format: YYYY-MM-DDTHH:MM:SS).")
}

class CalendarScheduleEventToolArgs {
  title string @description("The title of the event.")
  time_start string @description("The start of the event (ISO format: YYYY-MM-DDTHH:MM:SS).")
  time_end string @description("The end of the event (ISO format: YYYY-MM-DDTHH:MM:SS).")
}

function CalendarNextAction(context: string, additional_instructions: string, date_today: string) -> CalendarActionToolCall | CalendarActionEnd | CalendarActionInputRequired {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client Gemini_2_5_Flash
  prompt #"
    Identify the next action to take based on the provided context

    # Instructions
    - We are not allowed to schedule events in the past.
    - Once the user's request is complete, you should end the conversation with an answer. The answer should be in a human readable markdown format.
    - If you do not have enough information to complete the user's request, you should ask the user for the missing information. Be clear about the missing information.
    
    # Effort Mapping
    - very-high: 4 hours or more
    - high: 2 hours or more
    - medium: 1 hour or more
    - low: 30 minutes or more
    - very-low: less than 30 minutes
    
    # Additional instructions
    {{ additional_instructions }}

    # Today's date
    {{ date_today }}
    
    # Context
    {{ context }}

    # Output format
    {{ ctx.output_format }}
    
    Think step by step before outputting the result in JSON format.
  "#
}
