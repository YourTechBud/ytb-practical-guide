import * as fs from 'fs/promises'
import * as readline from 'readline'

// Path to the JSON file for storing tasks

// Interface for Task
interface Task {
  title: string
  isDone: boolean
}

// Function to get pending tasks
export const getPendingTasks = async (userId: string): Promise<string> => {
  const tasks = await loadTasks(userId)
  return JSON.stringify(tasks.filter((task) => !task.isDone), null, 2)
}

// Function to read all tasks
export const getAllTasks = async (userId: string): Promise<string> => {
  const tasks = await loadTasks(userId)
  return JSON.stringify(tasks, null, 2)
}

// Function to add a new task
export const newTask = async (userId: string, task: string): Promise<string> => {
  const tasks = await loadTasks(userId)

  // Check if the task already exists
  if (tasks.some((t) => t.title === task)) {
    throw new Error(`Task "${task}" already exists.`)
  }

  // Add the new task
  tasks.push({ title: task, isDone: false })
  await saveTasks(userId, tasks)
  return 'Task added successfully.'
}

// Function to mark a task as done
export const markTaskAsDone = async (userId: string, title: string): Promise<string> => {
  const tasks = await loadTasks(userId)
  const task = tasks.find((t) => t.title === title)

  if (!task) {
    throw new Error(`Task "${title}" not found.`)
  }

  task.isDone = true
  await saveTasks(userId, tasks)
  return 'Task marked as done.'
}

// Helper function to read the JSON file
const loadTasks = async (userId: string): Promise<Task[]> => {
  try {
    const filePath = `./tasks/${userId}.json`
    const data = await fs.readFile(filePath, 'utf-8')
    return JSON.parse(data) as Task[]
  } catch (error: any) {
    if (error.code === 'ENOENT') {
      // File doesn't exist, return empty structure
      return []
    }
    throw error
  }
}

// Helper function to write to the JSON file
const saveTasks = async (userId: string, tasks: Task[]): Promise<void> => {
  const filePath = `./tasks/${userId}.json`
  await fs.writeFile(filePath, JSON.stringify(tasks, null, 2))
}

export const prompt = async (message: string): Promise<string> => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  return new Promise((resolve) => {
    rl.question(message, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}
