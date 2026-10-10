export type VoidEchoSchemaDefinition = {
  type: 'string';
  pattern: string; // regex string
} | {
  type: 'json';
  properties: Record<string, { type: 'string' | 'number' | 'boolean' | 'array' | 'object', required?: boolean, enum?: any[] }>;
  // Simplified JSON schema for demonstration purposes
};

export interface ValidationResult {
  isValid: boolean;
  errors?: string[];
}
