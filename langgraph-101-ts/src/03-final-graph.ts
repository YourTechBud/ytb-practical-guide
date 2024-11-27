import * as dotenv from 'dotenv'
import { ChatOpenAI } from "@langchain/openai"
import { SystemMessage, HumanMessage, BaseMessage } from "@langchain/core/messages"
import { StateGraph, Annotation } from "@langchain/langgraph"
import { ToolNode } from "@langchain/langgraph/prebuilt"
import { askQuestion, closeInterface, extractJsonFromString, getModelConfig, getPendingTasks, toolMarkTaskAsDone, toolNewTask, toolReadTasks } from './utils'

// Load environment variables
dotenv.config()

// Get our tools
const tools = [toolReadTasks, toolNewTask, toolMarkTaskAsDone]

// Create our graph state
const StateAnnotation = Annotation.Root({
    messages: Annotation<BaseMessage[]>({
        reducer: (currentValue: BaseMessage[], newValue: BaseMessage[]) => [...currentValue, ...newValue],
        default: () => [],
    }),
    action: Annotation<string>,
    isTitlePresent: Annotation<boolean>(),
})

/******************************************/
// Nodes
/******************************************/

// The node to identify what kind of action does the user wants to perform
const identifyAction = async (state: typeof StateAnnotation.State) => {
    const model = new ChatOpenAI(getModelConfig('Qwen-2.5-32B-Instruct'))

    // Create a system & human message
    const systemMessage = new SystemMessage({
        content: 'You are a helpful AI assitant.'
    })

    const humanMessage = new HumanMessage({
        content: `Identify the action the user wants to perform in the following message: ${state.messages[state.messages.length - 1].content}
        The allowed actions are : readTasks, newTask, markTaskAsDone

        If the user mentions that they have done something, mark the task as done.
        
        Provide the response in the following format: 
        ## Justification
        <Step by step reasoning>

        ## Response
        {"action": "[action]"}`
    })

    // Prepare list of messages
    const messages = [systemMessage, humanMessage]

    const response = await model.invoke(messages)

    const action = extractJsonFromString(response.content as string)
    if (!action || !action.action || !['readTasks', 'newTask', 'markTaskAsDone'].includes(action.action)) {
        return { action: 'unknown' }
    }

    return { action: action.action }
}

// The node to identify the title of the task which matches our database
const findMatchingTitle = async (state: typeof StateAnnotation.State) => {
    const model = new ChatOpenAI(getModelConfig('Qwen-2.5-32B-Instruct'))

    // Create a system & human message
    const systemMessage = new SystemMessage({
        content: 'You are a helpful AI assitant.'
    })
    const humanMessage = new HumanMessage({
        content: `Identify the title in the following message: ${state.messages[state.messages.length - 1].content}

        The title must be present in this list: ${await getPendingTasks()}. Find the title which is the closest match.

        If no title matches, provide an empty string and mark isTitlePresent as false.

        Provide the resonse in the following format:

        ## Justification
        <Step by step reasoning>

        ## Response
        {"title": "[title]", "isTitlePresent": [true/false]}`
    })

    // Prepare list of messages
    const messages = [systemMessage, humanMessage]

    const response = await model.invoke(messages)
    const title = extractJsonFromString(response.content as string)

    return { messages: [new HumanMessage({content: response.content})], isTitlePresent: title && title.isTitlePresent }
}

// Create our langgraph nodes
const agent = async (state: typeof StateAnnotation.State) => {
    const model = new ChatOpenAI(getModelConfig('Qwen-2.5-32B-Instruct')).bindTools(tools)

    // Create a system message
    const systemMessage = new SystemMessage({
        content: 'You are a helpful AI assitant. Follow the entire conversation history carefully to identify the tool to call and arguments to pass to them.'
    })

    // Prepare list of messages
    const messages = [systemMessage, ...state.messages]

    const response = await model.invoke(messages)

    return { messages: [response] }
}

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

// Create our tool node
const toolNode = new ToolNode(tools)

/******************************************/
// Conditional functions
/******************************************/

// Identify the title for marking a task as done
const shouldIdentifyTitle = (state: typeof StateAnnotation.State) => {
    if (state.action === 'unknown') {
        console.log('Unknown action. Exiting...')
        return '__end__'
    }

    if (state.action === 'markTaskAsDone') {
        return 'findMatchingTitle'
    }

    return 'agent'
}

// Exit if title is not present when marking a task as done
const isTitlePresent = (state: typeof StateAnnotation.State) => {
    if (state.isTitlePresent === false) {
        console.log('Title not found. Exiting...')
        return '__end__'
    }

    return 'agent'
}

// We need to summarize responses of readTasks
const isSummarizationNeeded = (state: typeof StateAnnotation.State) => {
    if (state.action === 'readTasks') {
        return 'taskSummarizer'
    }

    return '__end__'
}

/******************************************/
// Create our graph and execute it
/******************************************/

// Create our first graph
const workflow = new StateGraph(StateAnnotation)
    .addNode("identifyAction", identifyAction)
    .addNode("findMatchingTitle", findMatchingTitle)
    .addNode("agent", agent)
    .addNode("tool", toolNode)
    .addNode("taskSummarizer", taskSummarizer)
    .addEdge("__start__", "identifyAction")
    .addConditionalEdges('identifyAction', shouldIdentifyTitle)
    .addConditionalEdges('findMatchingTitle', isTitlePresent)
    .addEdge("agent", "tool")
    .addConditionalEdges("tool", isSummarizationNeeded)
    .addEdge("taskSummarizer", "__end__")
const app = workflow.compile()

// Pop the big question
const question = await askQuestion('Ask your question? ')

console.log('---')

// Run the graph
const initialState = { messages: [new HumanMessage({ content: question })], action: 'unknown' , isTitlePresent: false }

for await (
    const chunk of await app.stream(initialState, {
        streamMode: 'updates',
    })
) {
    for (const [node, values] of Object.entries(chunk)) {
        console.log('Receiving update from node:', node)
        const typedValues = values as { messages: BaseMessage[], action: string, isTitlePresent: boolean }
        switch (node) {
            case 'identifyAction':
                console.log('Action:', typedValues.action)
                break
            default:
                console.log('Content:', typedValues.messages[0].content)
                break
        }
        console.log('---')
    }
}

// Close the interface
closeInterface()