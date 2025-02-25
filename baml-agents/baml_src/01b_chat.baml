function QAChat(messages: Message[]) -> string {
  client LLAMA3_1_8B
  prompt #"
    You are a helpful assistant.

    {{ PrintMessages(messages) }}
  "#
}

test qa_chat_test {
  functions [QAChat]
  args {
    messages [
      {
        role "user"
        message "What is the capital of France?"
      },
      {
        role "assistant"
        message "The capital of France is Paris."
      },
      {
        role "user"
        message "Tell me something about it?"
      }
    ]
    
  }
}
