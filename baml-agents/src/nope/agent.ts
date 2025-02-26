import { BamlValidationError, ClientRegistry } from "@boundaryml/baml";
import { b, GenericStructuredResponse, Message } from "../baml_client";
import { AgentResponse, Context } from "./types";
import TypeBuilder from "../baml_client/type_builder";
import { Tool, ToolMetadata } from "./tools";
import { NopeRetry } from "./errors";
import { ResponseSchema } from "./structured-response";

// Helper type to extract the response type from a Tool
type ExtractToolResponseType<T> = T extends Tool<any, infer R, any> ? R : never;

// Helper type to create a union of all tool response types from an array of tools
type ToolsResponseUnion<T extends readonly Tool<any, any, any>[]> = {
  [K in keyof T]: ExtractToolResponseType<T[K]>
}[number];

export interface AgentConfig<Request = string, Response = string, DepsT = undefined, Tools extends readonly Tool<any, any, DepsT>[] = []> {
  run?: (ctx: Context<DepsT>, req: Request) => Promise<AgentResponse<Response>>;
  systemPrompt?: string | ((ctx: Context<DepsT>) => Promise<string>);
  middlewares?: ((ctx: Context<DepsT>, request: Request) => Promise<Request>)[];
  tools?: Tools;
  clientRegistry?: ClientRegistry;
  structuredOutput?: ResponseSchema<Response, DepsT>;
}

export type AgentOptions<DepsT> = DepsT extends undefined
  ? { retries?: number }
  : { deps: DepsT; retries?: number };

// Conditional type for the Agent's Response type
// If tools are provided, use the union of all tool response types
// Otherwise, use the original Response type
export class Agent<
  Request = string,
  Response = string,
  DepsT = undefined,
  Tools extends readonly Tool<any, any, DepsT>[] = []
> {
  constructor(private readonly config: AgentConfig<Request, Response, DepsT, Tools>) { }

  async run(
    request: Request,
    options: AgentOptions<DepsT>
  ): Promise<AgentResponse<
    Tools extends readonly [] ? Response : ToolsResponseUnion<Tools>
  >> {
    const ctx = new Context<DepsT>('deps' in options ? options.deps : undefined as DepsT, options.retries);

    // Run middlewares
    for (const middleware of this.config.middlewares || []) {
      request = await middleware(ctx, request);
    }

    if (this.config.run) {
      const response = await this.config.run(ctx, request);
      return response as any; // Type cast needed due to conditional return type
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

    if (this.isSimpleCall()) {
      // Request and response will both be strings if we have got to this point
      const result = await b.GenericQuery(systemPrompt, request as string, { clientRegistry: this.config.clientRegistry });
      return new AgentResponse(result as Response) as any; // Type cast needed due to conditional return type
    }

    const tb = new TypeBuilder();
    if (this.config.structuredOutput) {
      this.setStructuredResponseField(tb);
    } else if (this.config.tools && this.config.tools.length > 0) {
      this.setToolResponseField(tb);
    }

    const messages: Message[] = [];
    for (let i = 0; i < ctx.retries; i++) {
      var result: GenericStructuredResponse;
      try {
        result = await b.GenericStructuredOutputCall(systemPrompt, request as string, messages, { clientRegistry: this.config.clientRegistry, tb });
      } catch (error) {
        if (error instanceof BamlValidationError) {
          console.log("BAML Validation Error");
          messages.push({ role: "assistant", message: error.raw_output });
          messages.push({ role: "user", message: "Response is of invalid format. Please try again." });
          continue;
        }
        throw error;
      }
      messages.push({ role: "assistant", message: JSON.stringify(result) });

      if (this.isStructuredOutput()) {
        try {
          return new AgentResponse(await this.config.structuredOutput!.validate(ctx, result.response)) as any;
        } catch (error) {
          if (error instanceof NopeRetry) {
            console.log("Retrying structured output:", error.message);
            messages.push({ role: "user", message: error.message });
            continue;
          }
          throw error;
        }
      }

      const toolName = result.tool_call._tool_type;
      const tool = this.config.tools!.find((tool) => tool.name() === toolName);
      if (!tool) {
        const toolNames = this.config.tools!.map((tool) => tool.name());
        messages.push({
          role: "user",
          message: `Tool '${toolName}' not found. Please select one of these tools: ${JSON.stringify(toolNames)}`
        });
        continue;
      }

      try {
        const response = await tool.call(ctx, result.tool_call);
        response.iterations = i + 1; // Set the number of iterations
        return response as any; // Type cast needed due to conditional return type
      } catch (error) {
        if (error instanceof NopeRetry) {
          console.log("Retrying tool call", error.message);
          messages.push({ role: "user", message: error.message });
          continue;
        }
        throw error;
      }
    }

    throw new Error("Max retries exceeded");
  }

  private isSimpleCall() {
    return !this.isToolCall() && !this.isStructuredOutput();
  }

  private isToolCall() {
    return this.config.tools && this.config.tools.length > 0;
  }

  private isStructuredOutput() {
    return this.config.structuredOutput !== undefined;
  }

  private setStructuredResponseField(tb: TypeBuilder) {
    const fieldType = this.config.structuredOutput!.getBamlSchema(tb);
    tb.GenericStructuredResponse.addProperty("response", fieldType);
  }

  private setToolResponseField(tb: TypeBuilder) {
    const tools: { [key: string]: ToolMetadata } = {};
    for (const tool of this.config.tools!) {
      const metadata = tool.getMetadata(tb);
      tools[metadata.name] = metadata;
    }

    const toolTypes = Object.values(tools).map((tool) => tool.fieldType);
    tb.GenericStructuredResponse.addProperty("tool_call", tb.union(toolTypes));
  }
}