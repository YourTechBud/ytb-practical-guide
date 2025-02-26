import dotenv from "dotenv";
dotenv.config();

import { b, Message } from "./baml_client";
import * as nope from "./nope";
import { prompt } from "./utils";

async function run(ctx: nope.Context, messages: Message[]) {
  const response = await b.QAChat(messages);
  return new nope.AgentResponse(response);
}


async function main() {
  // Create an agent
  const agent = new nope.Agent({ run });

  const messages: Message[] = []

  while (true) {
    const message = await prompt("You: ");
    messages.push({ role: "user", message: message! });

    const response = await agent.run(messages, {});
    console.log(`Assistant: ${response.data}`);
    messages.push({ role: "assistant", message: response.data });
  }
}

main();
