import dotenv from "dotenv";
dotenv.config();

import { b } from "./baml_client";
import * as nope from "./nope";
import { prompt } from "./utils";

async function run(ctx: nope.Context, query: string) {
  const response = await b.QASimple(query);
  return new nope.AgentResponse(response);
}
const agent = new nope.Agent({ run });

async function main() {
  // Create an agent

  const query = await prompt("You: ");
  const response = await agent.run(query!, {});
  console.log(response.data);
}

main();
