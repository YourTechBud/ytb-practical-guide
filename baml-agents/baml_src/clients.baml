// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> LLAMA3_1_8B {
  provider openai-generic
  options {
    model "llama3.1:8b"
    api_key env.OPENAI_API_KEY
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
  }
}

client<llm> Qwen2_5_32B {
  provider openai-generic
  options {
    model "qwen2.5:32b"
    api_key env.OPENAI_API_KEY
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
  }
}

client<llm> NopeModel {
  provider openai-generic
  options {
    model "llama3.1:8b"
    api_key env.OPENAI_API_KEY
    base_url "https://inferix.yourtechbud.studio/inferix/v1/llm"
  }
}