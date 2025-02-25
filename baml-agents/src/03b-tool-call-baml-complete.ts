import dotenv from "dotenv";
dotenv.config();

import { AddTask, b, GetTasks, MarkTaskAsDone, Message } from "./baml_client";
import * as nope from "./nope";
import { getPendingTasks, getAllTasks } from "./utils";

async function run(ctx: nope.Context<string>, request: string) {
  var tool: AddTask | GetTasks | MarkTaskAsDone | null = null;

  const messages: Message[] = [];
  for (let i = 0; i < ctx.retries; i++) {
    // Call
    console.log("Calling TaskToolComplete");
    tool = await b.TaskToolComplete(request, messages);

    // First append the response to the message list. We might need it for retrying
    messages.push({role: 'assistant', message: JSON.stringify(tool)});

    // Perform checks
    if (tool.tool === 'getTasks' && !['pending', 'all'].includes(tool.filter)) {
      console.log('filter:', tool.filter);
      messages.push({role: 'user', message: '"filter" is required when tool is "getTasks". It should be either "pending" or "all"'});
      continue;
    }

    if (tool.tool === 'addTask' && !tool.title) {
      messages.push({role: 'user', message: 'addTaskArgs is required when tool is "addTask"'});
      continue;
    }

    break;
  }

  // Throw an error if we didn't get a valid response
  if (!tool) {
    throw new nope.Nope("Failed to get a valid response from the tool");
  }
  
  // Call the tool
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
agent.run('Give me completed tasks', {deps: "YourTechBud"}).then((response) => {
  console.log(response.data);
});
