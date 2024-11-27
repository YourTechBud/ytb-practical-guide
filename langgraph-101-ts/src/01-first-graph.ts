import * as dotenv from 'dotenv'
import { ChatOpenAI } from "@langchain/openai"
import { SystemMessage, HumanMessage, BaseMessage } from "@langchain/core/messages"
import { StateGraph, Annotation } from "@langchain/langgraph"
import { askQuestion, closeInterface, getModelConfig } from './utils'

// Load environment variables
dotenv.config()

// Create our graph state
const StateAnnotation = Annotation.Root({
    messages: Annotation<BaseMessage[]>({
        reducer: (currentValue: BaseMessage[], newValue: BaseMessage[]) => [...currentValue, ...newValue],
        default: () => [],
    })
})

// Create our first langgraph node
const agent = async (state: typeof StateAnnotation.State) => {
    const model = new ChatOpenAI(getModelConfig('Llama-3.1-8B-Instruct'))

    // Create a system message
    const systemMessage = new SystemMessage({
        content: 'You are a helpful AI assitant and a productivity expert. You always respond with motivational and helpful messages.'
    })

    // Prepare list of messages
    const messages = [systemMessage, ...state.messages]

    const response = await model.invoke(messages)
    return { messages: [response] }
}

// Create our first graph
const workflow = new StateGraph(StateAnnotation)
    .addNode("agent", agent)
    .addEdge("__start__", "agent")
    .addEdge("agent", "__end__")
const app = workflow.compile()

// Pop the big question
const question = await askQuestion('Ask your question? ')

// Run the graph
const initialState = { messages: [new HumanMessage({ content: question })] }
const finalState = await app.invoke(initialState)

console.log('\nFinal State:')
console.log(finalState.messages.map((message: BaseMessage) => ({ role: message.getType(), content: message.content })))

// Close the interface
closeInterface()