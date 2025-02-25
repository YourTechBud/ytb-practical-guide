import { ClientRegistry } from "@boundaryml/baml";
import { b, Message } from "../baml_client";
import { AgentResponse, Context } from "./types";
import TypeBuilder from "../baml_client/type_builder";
import { Tool, ToolMetadata } from "./tools";


export interface AgentConfig<Request = string, Response = string, DepsT = undefined> {
  run?: (ctx: Context<DepsT>, req: Request) => Promise<AgentResponse<Response>>;
  systemPrompt?: string | ((ctx: Context<DepsT>) => Promise<string>);
  middlewares?: ((ctx: Context<DepsT>, request: Request) => Promise<Request>)[];
  tools?: Tool<any, any, DepsT>[];
  clientRegistry?: ClientRegistry;
}

export type AgentOptions<DepsT> = DepsT extends undefined
  ? { retries?: number }
  : { deps: DepsT; retries?: number };

export class Agent<Request, Response, DepsT> {
  constructor(private readonly config: AgentConfig<Request, Response, DepsT>) {
    this.config;
  }

  async run(request: Request, options: AgentOptions<DepsT>): Promise<AgentResponse<Response>> {
    const ctx = new Context<DepsT>('deps' in options ? options.deps : undefined as DepsT, options.retries);

    // Run middlewares
    for (const middleware of this.config.middlewares || []) {
      request = await middleware(ctx, request);
    }

    if (this.config.run) {
      const response = await this.config.run(ctx, request);
      return response;
    }

    // Set the system prompt
    var systemPrompt = "You are a helpful AI assistant.";
    if (this.config.systemPrompt) {
      if (typeof this.config.systemPrompt === "string") {
        systemPrompt = this.config.systemPrompt;
      } else {
        systemPrompt = await this.config.systemPrompt(ctx);
      }
    }

    if (!this.config.tools || this.config.tools.length === 0) {
      // Request and response will both be strings if we have got to this point
      const result = await b.GenericQuery(systemPrompt, request as string, { clientRegistry: this.config.clientRegistry });
      return new AgentResponse(result as Response);
    }

    const messages: Message[] = [];
    for (let i = 0; i < ctx.retries; i++) {
      const tools: { [key: string]: ToolMetadata } = {};
      const tb = new TypeBuilder();
      for (const tool of this.config.tools) {
        const metadata = tool.getMetadata(tb);
        tools[metadata.name] = metadata;
      }

      const toolTypes = Object.values(tools).map((tool) => tool.fieldType);
      tb.GenericToolResponse.addProperty("tool_call", tb.union(toolTypes));

      const result = await b.GenericToolCall(systemPrompt, request as string, [], { clientRegistry: this.config.clientRegistry, tb });
      messages.push({ role: "assistant", message: JSON.stringify(result) });

      const toolName = result.tool_call.tool_type;
      const tool = this.config.tools.find((tool) => tool.fn.name === toolName);
      if (!tool) {
        messages.push({ role: "user", message: `Tool '${toolName}' not found. Please select one of these tools: ${JSON.stringify(Object.keys(tools))}` });
        continue;
      }

      return await tool.fn(ctx, result.tool_call);
    }

    throw new Error("Max retries exceeded");
  }
}