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

export class Tool<Args, Response, DepsT> {
  fn: ToolFn<Args, Response, DepsT>;
  private schema: z.AnyZodObject;

  constructor(fn: ToolFn<Args, Response, DepsT>, schema: z.AnyZodObject) {
    this.fn = fn;
    this.schema = schema;
  }

  getMetadata(tb: TypeBuilder) {
    // Make sure the tool type is added to the schema
    const finalSchema = this.schema.extend({ tool_type: z.enum([this.fn.name]) });

    const titleCasedName = this.fn.name.charAt(0).toUpperCase() + this.fn.name.slice(1);
    const jsonSchema = zodToJsonSchema(finalSchema, { name: titleCasedName, nameStrategy: 'title' });
    const fieldType = new SchemaAdder(tb, jsonSchema).parse(jsonSchema);

    const metadata: ToolMetadata = {
      name: this.fn.name,
      fieldType
    }
    return metadata;
  }
}
