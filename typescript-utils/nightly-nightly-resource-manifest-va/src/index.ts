import { ResourceSchema, ResourceManifest, ValidationResult, ResourceUnit, ResourceSchemaItem } from './types';

export class ManifestValidator {
  private schema: ResourceSchema;

  constructor(schema: ResourceSchema) {
    this.schema = schema;
    this.validateSchema(schema); // Basic self-validation of the schema
  }

  private validateSchema(schema: ResourceSchema): void {
    if (!schema || !schema.version || !schema.name || !Array.isArray(schema.resources)) {
      throw new Error("Invalid schema structure: missing version, name, or resources array.");
    }
    schema.resources.forEach(item => {
      if (!item.name || !Array.isArray(item.units) || item.units.length === 0) {
        throw new Error(`Invalid schema item: missing name or units for resource "${item.name || 'unknown'}".`);
      }
      item.units.forEach(unit => {
        if (!this.isValidResourceUnit(unit)) {
          throw new Error(`Invalid unit "${unit}" for resource "${item.name}".`);
        }
      });
      if (item.minQuantity !== undefined && item.maxQuantity !== undefined && item.minQuantity > item.maxQuantity) {
        throw new Error(`Invalid quantity range for resource "${item.name}": minQuantity cannot be greater than maxQuantity.`);
      }
    });
  }

  private isValidResourceUnit(unit: string): unit is ResourceUnit {
    const validUnits: ResourceUnit[] = ['kg', 'g', 'liter', 'ml', 'piece', 'can', 'box', 'meter', 'foot', 'unit'];
    return (validUnits as string[]).includes(unit);
  }

  validateManifest(manifest: ResourceManifest): ValidationResult {
    const errors: string[] = [];

    if (!manifest || !manifest.manifestId || !manifest.location || !manifest.timestamp || !Array.isArray(manifest.items)) {
      errors.push("Invalid manifest structure: missing manifestId, location, timestamp, or items array.");
      return { isValid: false, errors };
    }

    // Validate timestamp format (basic ISO 8601 check)
    if (isNaN(new Date(manifest.timestamp).getTime())) {
        errors.push(`Invalid timestamp format for manifestId "${manifest.manifestId}": "${manifest.timestamp}" is not a valid ISO 8601 date.`);
    }

    const schemaResourceMap = new Map<string, ResourceSchemaItem>();
    this.schema.resources.forEach(res => schemaResourceMap.set(res.name, res));

    manifest.items.forEach((item, index) => {
      const prefix = `Item ${index + 1} ("${item.resourceName}"):`;
      const schemaItem = schemaResourceMap.get(item.resourceName);

      if (!schemaItem) {
        errors.push(`${prefix} Resource "${item.resourceName}" is not defined in the schema.`);
        return; // Skip further validation for this item if not in schema
      }

      if (item.quantity === undefined || typeof item.quantity !== 'number' || item.quantity < 0) {
        errors.push(`${prefix} Quantity must be a non-negative number.`);
      }

      if (!item.unit || !this.isValidResourceUnit(item.unit)) {
        errors.push(`${prefix} Invalid or unsupported unit "${item.unit}".`);
      } else if (!schemaItem.units.includes(item.unit)) {
        errors.push(`${prefix} Unit "${item.unit}" is not allowed for resource "${item.resourceName}" by the schema. Allowed units: ${schemaItem.units.join(', ')}.`);
      }

      if (item.quantity !== undefined && typeof item.quantity === 'number') {
        if (schemaItem.minQuantity !== undefined && item.quantity < schemaItem.minQuantity) {
          errors.push(`${prefix} Quantity ${item.quantity} is below the minimum allowed (${schemaItem.minQuantity}) for resource "${item.resourceName}".`);
        }
        if (schemaItem.maxQuantity !== undefined && item.quantity > schemaItem.maxQuantity) {
          errors.push(`${prefix} Quantity ${item.quantity} is above the maximum allowed (${schemaItem.maxQuantity}) for resource "${item.resourceName}".`);
        }
      }
    });

    return {
      isValid: errors.length === 0,
      errors: errors,
    };
  }
}
