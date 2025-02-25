import { FieldType } from "@boundaryml/baml/native";
import TypeBuilder from "../baml_client/type_builder";

interface Schema {
    [key: string]: any;
}

export class SchemaAdder {
    private tb: TypeBuilder;
    private schema: Schema;
    private _refCache: { [key: string]: FieldType };

    constructor(tb: TypeBuilder, schema: Schema) {
        this.tb = tb;
        this.schema = schema;
        this._refCache = {};
    }

    private _parseObject(jsonSchema: Schema): FieldType {
        if (jsonSchema.type !== "object") {
            throw new Error("Expected type to be 'object'");
        }

        const name = jsonSchema.title;
        if (!name) {
            throw new Error("Title is required in JSON schema for object type");
        }

        const requiredFields = jsonSchema.required || [];
        if (!Array.isArray(requiredFields)) {
            throw new Error("'required' field must be an array");
        }

        const newClass = this.tb.addClass(name);

        const properties = jsonSchema.properties;
        if (properties) {
            if (typeof properties !== 'object') {
                throw new Error("'properties' field must be an object");
            }

            for (const fieldName in properties) {
                if (properties.hasOwnProperty(fieldName)) {
                    const fieldSchema = properties[fieldName];
                    if (typeof fieldSchema !== 'object' || !fieldSchema) {
                        throw new Error(`Invalid schema for property '${fieldName}'`);
                    }

                    const defaultValue = fieldSchema.default;

                    let fieldType: FieldType;
                    if (!fieldSchema.properties && fieldSchema.type === 'object') {
                        console.warn(`Field '${fieldName}' uses generic dict type which defaults to Dict<string, string>. If a more specific type is needed, please provide a specific Pydantic model instead.`);
                        fieldType = this.tb.map(this.tb.string(), this.tb.string());
                    } else {
                        fieldType = this.parse(fieldSchema);
                    }

                    if (!requiredFields.includes(fieldName)) {
                        if (defaultValue === undefined) {
                            fieldType = fieldType.optional();
                        }
                    }

                    const property = newClass.addProperty(fieldName, fieldType);

                    const description = fieldSchema.description;
                    if (description) {
                        if (typeof description !== 'string') {
                            throw new Error(`Invalid description for property '${fieldName}'`);
                        }
                        if (defaultValue !== undefined) {
                            property.description(`${description.trim()}\nDefault: ${defaultValue}`.trim());
                        } else {
                            property.description(description.trim());
                        }
                    }
                }
            }
        }

        return newClass.type();
    }

    private _parseString(jsonSchema: Schema): FieldType {
        if (jsonSchema.type !== "string") {
            throw new Error("Expected type to be 'string'");
        }

        const title = jsonSchema.title;

        const enumValues = jsonSchema.enum;
        if (Array.isArray(enumValues)) {
            if (title) {
                const enumType = this.tb.addEnum(title);
                enumValues.forEach(value => enumType.addValue(value));
                return enumType.type();
            }

            return this.tb.union(enumValues.map(value => this.tb.literalString(value)));
        }

        return this.tb.string();
    }

    private _loadRef(ref: string): FieldType {
        if (!ref.startsWith("#/")) {
            throw new Error(`Only local references are supported: ${ref}`);
        }

        const [_, left, right] = ref.split("/", 3);

        if (!this._refCache[ref]) {
            const refs = this.schema[left];
            if (refs && typeof refs === 'object') {
                const subSchema = refs[right];
                if (!subSchema) {
                    throw new Error(`Reference ${ref} not found in schema`);
                }
                this._refCache[ref] = this.parse(subSchema);
            }
        }

        return this._refCache[ref];
    }

    public parse(jsonSchema: Schema): FieldType {
        if (jsonSchema.anyOf) {
            return this.tb.union(jsonSchema.anyOf.map((subSchema: any) => this.parse(subSchema)));
        }

        const additionalProperties = jsonSchema.additionalProperties;
        if (additionalProperties && typeof additionalProperties === 'object') {
            const anyOfAdditionalProps = additionalProperties.anyOf;
            if (Array.isArray(anyOfAdditionalProps)) {
                return this.tb.map(this.tb.string(), this.tb.union(anyOfAdditionalProps.map(subSchema => this.parse(subSchema))));
            }
        }

        const ref = jsonSchema.$ref;
        if (typeof ref === 'string') {
            return this._loadRef(ref);
        }

        const type = jsonSchema.type;
        if (!type) {
            console.warn("Empty type field in JSON schema, defaulting to string");
            return this.tb.string();
        }

        const parseType: { [key: string]: () => FieldType } = {
            "string": () => this._parseString(jsonSchema),
            "number": () => this.tb.float(),
            "integer": () => this.tb.int(),
            "object": () => this._parseObject(jsonSchema),
            "array": () => this.parse(jsonSchema.items).list(),
            "boolean": () => this.tb.bool(),
            "null": () => this.tb.null(),
        };

        if (!parseType[type]) {
            throw new Error(`Unsupported type: ${type}`);
        }

        return parseType[type]();
    }
}

function parseJsonSchema(jsonSchema: Schema, tb: TypeBuilder): FieldType {
    const parser = new SchemaAdder(tb, jsonSchema);
    return parser.parse(jsonSchema);
}
