import dotenv from "dotenv";
dotenv.config();

import { b, Message } from "./baml_client";
import * as nope from "./nope";
import { prompt } from "./utils";

async function run(ctx: nope.Context, userMessage: string) {
  const response = await b.ClassifyIntentSimple(userMessage);
  return new nope.AgentResponse(response);
}

async function main() {
  const agent = new nope.Agent({ run });

  const message = await prompt("You: ");
  const response = await agent.run(message, {});
  console.log(`Assistant: ${JSON.stringify(response.data, null, 2)}`);
}

main();
