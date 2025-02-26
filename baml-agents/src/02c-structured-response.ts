import dotenv from "dotenv";
dotenv.config();

import { b, Message } from "./baml_client";
import * as nope from "./nope";
import { prompt } from "./utils";
import { z } from "zod";
import { ClientRegistry } from "@boundaryml/baml";

/*
 * Create the schemas
 */

const getTasksSchema = z.object({
  intent: z.enum(["listTasks"]).describe("The user wants to list tasks."),
  filter: z.string().describe("The filter can be 'done' or 'pending'"),
}).describe("getTasks");

const addTaskSchema = z.object({
  intent: z.enum(["addTasks"]).describe("The user wants to do something or add a task to the list."),
  taskTitle: z.string().describe("The title of the task to add."),
}).describe("addTask");

const markTaskAsDoneSchema = z.object({
  intent: z.enum(["markTaskAsDone"]).describe("The user has done something or wants to mark a task as done."),
}).describe("markTaskAsDone");

const unknownSchema = z.object({
  intent: z.enum(["unknown"]).describe("User's intent is not clear or invalid."),
}).describe("unknown");

const intentSchema = z.union([getTasksSchema, addTaskSchema, markTaskAsDoneSchema, unknownSchema]);

/*
 * Create the validation function
 */

async function validate(ctx: nope.Context, response: z.infer<typeof intentSchema>) {
  if (response.intent !== "listTasks") return response;

  const listTasksIntent = response as z.infer<typeof getTasksSchema>;
  if (!['pending', 'all'].includes(listTasksIntent.filter!)) {
    throw new nope.NopeRetry(`Invalid filter: '${listTasksIntent.filter}'. Can be 'pending' or 'all'`);
  }
  return response;
}

/*
 * Create agent
 */

const systemPrompt = async (ctx: nope.Context) => {
  return `Identify the user's intent from the provided message. Follow the rules below:
  - Action will be "unknown" for all unknow invalid messages.
  - If the user has done something, mark the task as done.
  - If the user wants to do something, add the task to the list.`;
}

const userPrompt = async (ctx: nope.Context, request: string) => {
  return `User's Message: ${request}`;
}

// Create a structured output object
const structuredOutput = new nope.ResponseSchema(intentSchema, [validate]);

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
const agent = new nope.Agent({ systemPrompt, middlewares: [userPrompt], structuredOutput, clientRegistry });

/*
 * Main function
 */

async function main() {
  const message = await prompt("You: ");
  const response = await agent.run(message, { retries: 5 });
  console.log(`Iterations: ${response.iterations}`);
  console.log(`Assistant: ${JSON.stringify(response.data, null, 2)}`);
}

main();
