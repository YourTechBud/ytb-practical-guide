import dotenv from "dotenv";
dotenv.config();

import * as nope from "./nope";
import { ClientRegistry } from "@boundaryml/baml";
import { z } from "zod";
import { getAllTasks, getPendingTasks, newTask } from "./utils";
import { get } from "http";

/*
 * Define the prompts
 */

const systemPrompt = async (ctx: nope.Context<string>) => {
  return `Based on the user's message, return the appropriate tool to use.
  If the user has done something, mark the task as done.`;
}

const userPrompt = async (ctx: nope.Context<string>, request: string) => {
  return `Based on the user's message, return the appropriate tool to use.
  If the user has done something, mark the task as done.
  
  User's message: ${request}`;
}

/*
 * Define the tools
 */

// Get task tool
const getTasksSchema = z.object({ filter: z.union([z.literal("all"), z.literal("pending")]) })
  .describe("Get tasks from the database");

const getTasksFromDB = async (ctx: nope.Context<string>, args: z.infer<typeof getTasksSchema>) => {
  if (args.filter === "all") {
    return new nope.AgentResponse(await getAllTasks(ctx.deps));
  } else {
    return new nope.AgentResponse(await getPendingTasks(ctx.deps));
  }
}
const getTasksTool = new nope.Tool(getTasksFromDB, getTasksSchema)

// Add task tool
const addTaskSchema = z.object({ title: z.string() })
  .describe("Add a new task to the database");

const addTaskToDB = async (ctx: nope.Context<string>, args: z.infer<typeof addTaskSchema>) => {
  await newTask(ctx.deps, args.title);
  return new nope.AgentResponse('Task added');
}
const addTaskTool = new nope.Tool(addTaskToDB, addTaskSchema)


/*
 * Define and run the agent
 */

// Create a client registry
const clientRegistry = new ClientRegistry();
const clientOptions = {
  model: process.env.MODEL_SMALL,
  api_key: process.env.OPENAI_API_KEY,
  base_url: process.env.OPENAI_BASE_URL,
}
clientRegistry.addLlmClient("NopeModel", "openai-generic", clientOptions)
clientRegistry.setPrimary("NopeModel");

// Create an agent
const agent = new nope.Agent({ systemPrompt, middlewares: [userPrompt], clientRegistry, tools: [getTasksTool, addTaskTool] });
agent.run('Give me all my tasks', { deps: "YourTechBud", retries: 5 }).then((response) => {
  console.log(response.data);
});
