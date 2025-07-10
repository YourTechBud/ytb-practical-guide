// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> Gemini_2_5_Flash {
  provider google-ai
  options {
    model "gemini-2.5-flash"
    api_key env.GOOGLE_API_KEY
  }
}
