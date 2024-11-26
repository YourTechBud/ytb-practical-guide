import * as dotenv from 'dotenv';
import { ChatOpenAI } from "@langchain/openai";

// Load environment variables
dotenv.config()

const model = new ChatOpenAI({
  model: 'Llama-3.1-8B-Instruct',
  configuration: {
    baseURL: process.env.INFERIX_BASE_URL,
  },
  apiKey: process.env.INFERIX_API_KEY
})


model.invoke([{
  role: 'system',
  content: 'You are a helpful AI assitant and a productivity expert. You always respond with motivational and helpful messages.'
}, {
  role: 'user',
  content: 'How are you?'
}]).then((response) => {
  console.log(response.content)
})