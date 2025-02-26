import { FieldType } from "@boundaryml/baml/native";
import { AgentResponse, Context } from "./types";
import { z } from "zod";
import TypeBuilder from "../baml_client/type_builder";
import zodToJsonSchema from "zod-to-json-schema";
import { SchemaAdder } from "./schema-builder";

interface ToolFn<Args, Response, DepsT> {
  (ctx: Context<DepsT>, args: Args): Promise<AgentResponse<Response>>;
}

export interface ToolMetadata {
  name: string;
  fieldType: FieldType;
}

// Make the Response type more accessible for type inference
export class Tool<Args, Response, DepsT = undefined> {
  private fn: ToolFn<Args, Response, DepsT>;
  private schema: z.AnyZodObject;

  // Add a responseType property to help with type inference
  // This is a phantom property that only exists at compile time
  readonly responseType!: Response;

  constructor(fn: ToolFn<Args, Response, DepsT>, schema: z.AnyZodObject) {
    this.fn = fn;
    this.schema = schema;
  }

  name() {
    return this.fn.name;
  }

  getMetadata(tb: TypeBuilder) {
    // Make sure the tool type is added to the schema
    const name = this.fn.name;
    const finalSchema = this.schema.extend({ "_tool_type": z.enum([name]).describe(this.schema.description!) });

    const titleCasedName = name.charAt(0).toUpperCase() + name.slice(1);
    const jsonSchema = zodToJsonSchema(finalSchema, { name: titleCasedName, nameStrategy: 'title' });
    const fieldType = new SchemaAdder(tb, jsonSchema).parse(jsonSchema);

    const metadata: ToolMetadata = {
      name: name,
      fieldType
    }
    return metadata;
  }

  call(ctx: Context<DepsT>, args: Args) {
    return this.fn(ctx, args);
  }
}
