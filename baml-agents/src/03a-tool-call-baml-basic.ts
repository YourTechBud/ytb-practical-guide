import dotenv from "dotenv";
dotenv.config();

import { AddTask, b, GetTasks, MarkTaskAsDone } from "./baml_client";
import * as nope from "./nope";
import { getPendingTasks, getAllTasks, prompt } from "./utils";

async function run(ctx: nope.Context<string>, request: string) {
  const tool = await b.TaskToolBasic(request);
  switch (tool.tool) {
    case "getTasks":
      const getTasks = tool as GetTasks;
      console.log("Getting tasks: filter -", getTasks.filter);

      // Call the tools yourself
      if (getTasks.filter === "pending") {
        const result = await getPendingTasks(ctx.deps);
        return new nope.AgentResponse(result);
      } else {
        const allTasks = await getAllTasks(ctx.deps);
        return new nope.AgentResponse(allTasks);
      }
    case "addTask":
      const addTask = tool as AddTask;
      console.log("Adding task:", addTask.title);

      // Call the new task function
      return new nope.AgentResponse('Task added');
    case "markTaskAsDone":
      const markTaskAsDone = tool as MarkTaskAsDone;
      console.log("MarkTaskAsDone");

      // Call the mark task as done function
      return new nope.AgentResponse("Task marked as done");
  }

}

const agent = new nope.Agent({ run });

async function main() {
  const message = await prompt("You: ");
  const response = await agent.run(message!, { deps: "YourTechBud" });
  console.log(response.data);
}

main();
