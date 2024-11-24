import { tool } from '@langchain/core/tools';
import { z } from 'zod';
import { markTaskAsDone, newTask, readTasks } from './tasks';

export const toolReadTasks = tool((_input: any) => {
  return readTasks();
}, {
  name: 'readTasks',
  description: 'Read all tasks',
  schema: z.object({
    noOp: z.string().optional().describe('No-op parameter which is always an empty string.'),
  }),
})

export const toolNewTask = tool((input: any) => {
  return newTask(input.task);
}, {
  name: 'newTask',
  description: 'Add a new task',
  schema: z.object({
    task: z.string().describe('The task to add'),
  }),
})

export const toolMarkTaskAsDone = tool((input: any) => {
  return markTaskAsDone(input.title);
}, {
  name: 'markTaskAsDone',
  description: 'Mark a task as done',
  schema: z.object({
    title: z.string().describe('The task to mark as done'),
  }),
})