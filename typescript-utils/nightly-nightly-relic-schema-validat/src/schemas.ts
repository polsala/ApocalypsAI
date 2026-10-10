/**
 * Defines the structure for a scavenged log entry.
 */
export interface ScavengedLog {
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR';
  message: string;
  source?: string;
}

/**
 * Defines the structure for a resource manifest.
 */
export interface ResourceManifest {
  resourceId: string;
  quantity: number;
  location: {
    sector: string;
    grid: string;
  };
  scavengerNotes?: string[];
}

/**
 * A recursive type to define the expected structure and types of properties within a schema.
 * 'string' | 'number' | 'boolean' | 'object' | 'array' represent basic types.
 * A nested object will have its own SchemaDefinition.
 */
export type SchemaDefinition = {
  [key: string]: 'string' | 'number' | 'boolean' | 'object' | 'array' | SchemaDefinition;
};

/**
 * A collection of predefined 'relic' schemas for validation.
 * Each key is a schema name, and its value is a SchemaDefinition describing the expected data structure.
 */
export const RELIC_SCHEMAS: { [key: string]: SchemaDefinition } = {
  'ScavengedLog': {
    timestamp: 'string',
    level: 'string', // In a real scenario, this could be an enum check
    message: 'string',
    source: 'string' // Optional fields are handled by not being explicitly required in the validator
  },
  'ResourceManifest': {
    resourceId: 'string',
    quantity: 'number',
    location: {
      sector: 'string',
      grid: 'string'
    },
    scavengerNotes: 'array' // Array type check
  }
};
