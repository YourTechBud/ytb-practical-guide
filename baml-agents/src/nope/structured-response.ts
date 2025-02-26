import { z } from "zod";
import zodToJsonSchema from "zod-to-json-schema";
import { SchemaAdder } from "./schema-builder";
import TypeBuilder from "../baml_client/type_builder";
import { Context } from "./types";

export interface ResponseValidator<Response, DepsT> {
  (ctx: Context<DepsT>, response: Response): Promise<Response>;
}

export class ResponseSchema<Response, DepsT> {
  public schema: z.ZodType;
  public validators: ResponseValidator<Response, DepsT>[];

  constructor(schema: z.ZodType, validators?: ResponseValidator<Response, DepsT>[]) {
    this.schema = schema;
    this.validators = validators || [];
  }

  getBamlSchema(tb: TypeBuilder) {
    const jsonSchema = zodToJsonSchema(this.schema, { name: "Response", nameStrategy: 'title' });
    return new SchemaAdder(tb, jsonSchema).parse(jsonSchema);
  }

  async validate(ctx: Context<DepsT>, response: Response) {
    for (const validator of this.validators) {
      response = await validator(ctx, response);
    }
    return response;
  }
}
