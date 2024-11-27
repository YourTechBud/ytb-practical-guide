import * as fs from 'fs/promises'

// Path to the JSON file for storing tasks
const filePath = './tasks.json'

// Interface for Task
interface Task {
  title: string
  isDone: boolean
}

// Function to get pending tasks
export const getPendingTasks = async (): Promise<string> => {
  const tasks = await loadTasks()
  return JSON.stringify(tasks.filter((task) => !task.isDone), null, 2)
}

// Function to read all tasks
export const readTasks = async (): Promise<string> => {
  const tasks = await loadTasks()
  return JSON.stringify(tasks, null, 2)
}

// Function to add a new task
export const newTask = async (task: string): Promise<string> => {
  const tasks = await loadTasks()

  // Check if the task already exists
  if (tasks.some((t) => t.title === task)) {
    throw new Error(`Task "${task}" already exists.`)
  }

  // Add the new task
  tasks.push({ title: task, isDone: false })
  await saveTasks(tasks)
  return 'Task added successfully.'
}

// Function to mark a task as done
export const markTaskAsDone = async (title: string): Promise<string> => {
  const tasks = await loadTasks()
  const task = tasks.find((t) => t.title === title)

  if (!task) {
    throw new Error(`Task "${title}" not found.`)
  }

  task.isDone = true
  await saveTasks(tasks)
  return 'Task marked as done.'
}

// Helper function to read the JSON file
const loadTasks = async (): Promise<Task[]> => {
  try {
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
const saveTasks = async (tasks: Task[]): Promise<void> => {
  await fs.writeFile(filePath, JSON.stringify(tasks, null, 2))
}