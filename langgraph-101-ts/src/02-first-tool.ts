import * as dotenv from 'dotenv';
import { ChatOpenAI } from "@langchain/openai";
import { SystemMessage, HumanMessage, BaseMessage } from "@langchain/core/messages";
import { StateGraph, Annotation } from "@langchain/langgraph";
import { ToolNode } from "@langchain/langgraph/prebuilt";
import { askQuestion, closeInterface, getModelConfig, toolReadTasks } from './utils';

// Load environment variables
dotenv.config()

// Get our tools
const tools = [toolReadTasks]

// Create our graph state
const StateAnnotation = Annotation.Root({
    messages: Annotation<BaseMessage[]>({
        reducer: (currentValue: BaseMessage[], newValue: BaseMessage[]) => [...currentValue, ...newValue],
        default: () => [],
    })
})

// Create our langgraph nodes
const agent = async (state: typeof StateAnnotation.State) => {
    const model = new ChatOpenAI(getModelConfig('Qwen-2.5-32B-Instruct')).bindTools(tools)

    // Create a system message
    const systemMessage = new SystemMessage({
        content: 'You are a helpful AI assitant and a productivity expert. You always respond with motivational and helpful messages.'
    })

    // Prepare list of messages
    const messages = [systemMessage, ...state.messages]

    const response = await model.invoke(messages)

    return { messages: [response] }
}

// Create our tool node
const toolNode = new ToolNode(tools)

// Create task summarizer node
const taskSummarizer = async (state: typeof StateAnnotation.State) => {
    const model = new ChatOpenAI(getModelConfig('Llama-3.1-8B-Instruct'))

    // Create a system & human message
    const systemMessage = new SystemMessage({
        content: 'You are a helpful AI assitant and a productivity expert. You always respond with motivational and helpful messages.'
    })

    const humanMessage = new HumanMessage({
        content: `Summarize these tasks in a concise and organized manner: ${state.messages[state.messages.length - 1].content}`
    })

    // Prepare list of messages
    const messages = [systemMessage, humanMessage]

    const response = await model.invoke(messages)

    return { messages: [response] }
}

// Create our first graph
const workflow = new StateGraph(StateAnnotation)
    .addNode("agent", agent)
    .addNode("tool", toolNode)
    .addNode("taskSummarizer", taskSummarizer)
    .addEdge("__start__", "agent")
    .addEdge("agent", "tool")
    .addEdge("tool", "taskSummarizer")
    .addEdge("taskSummarizer", "__end__")
const app = workflow.compile()

// Pop the big question
const question = await askQuestion('Ask your question? ')

console.log('---')

// Run the graph
const initialState = { messages: [new HumanMessage({ content: question })] }

for await (
    const chunk of await app.stream(initialState, {
        streamMode: 'updates',
    })
) {
    for (const [node, values] of Object.entries(chunk)) {
        console.log('Receiving update from node:', node)
        const typedValues = values as { messages: BaseMessage[] };
        console.log('Values:', typedValues.messages[0].content)
        console.log('---')
    }
}

// Close the interface
closeInterface()