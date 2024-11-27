import * as readline from 'readline'

const rl = readline.createInterface({
  input: process.stdin,
})

// Utility to wrap rl.question in a Promise
export const askQuestion = (question: string): Promise<string> => {
  return new Promise((resolve) => {
    console.log(question)
    rl.question(question, (answer: string) => resolve(answer))
  })
}

// Utility to close the readline interface
export const closeInterface = () => {
  rl.close()
}