import dotenv from "dotenv";
dotenv.config();

import { b } from "./baml_client";
import * as nope from "./nope";

async function run(ctx: nope.Context, query: string) {
  const response = await b.Summarize(query);
  return new nope.AgentResponse(response);
}

// Create an agent
const agent = new nope.Agent({ run });

const paragraph = `
  Pokemon is a Japanese media franchise managed by The Pokemon Company,
  which was formed by Nintendo, Game Freak, and Creatures.
  The franchise was created by Satoshi Tajiri in 1996, and is centered on a series of video games,
  card games, and trading card games, as well as animated television series.
`;
agent.run(paragraph, {}).then((response) => {
  console.log(response.data);
});
