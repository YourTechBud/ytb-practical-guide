import dotenv from "dotenv";
dotenv.config();

import { b, Message } from "./baml_client";
import * as nope from "./nope";
import { prompt } from "./utils";

async function run(ctx: nope.Context, userMessage: string) {
  const messages: Message[] = [];

  for (let i = 0; i < ctx.retries; i++) {
    const response = await b.ClassifyIntentAdvanced(userMessage, messages);
    messages.push({ role: 'assistant', message: JSON.stringify(response) });

    // Run validations
    if (response.intent === 'listTasks' && !['pending', 'all'].includes(response.filter)) {
      messages.push({ role: 'user', message: '"filter" is required when doing "listTasks". It should be either "pending" or "all"' });
      continue;
    }

    return new nope.AgentResponse(response, i + 1);
  }

  throw new nope.NopeError("Failed to get a valid response from the tool");
}

async function main() {
  const agent = new nope.Agent({ run });

  const message = await prompt("You: ");
  const response = await agent.run(message, { retries: 5 });
  console.log("Iterations:", response.iterations);
  console.log(`Assistant: ${JSON.stringify(response.data, null, 2)}`);
}

main();
