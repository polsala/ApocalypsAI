import { ManifestValidator } from '../src/index';
import { ResourceSchema, ResourceManifest, ResourceSchemaItem } from '../src/types';

describe('ManifestValidator', () => {
  const validSchema: ResourceSchema = {
    version: '1.0',
    name: 'ApocalypticEssentials',
    description: 'Schema for critical survival resources.',
    resources: [
      { name: 'Water', units: ['liter', 'ml'], minQuantity: 0.5, maxQuantity: 100 },
      { name: 'Canned Food', units: ['can', 'box'], minQuantity: 1, maxQuantity: 50 },
      { name: 'First Aid Kit', units: ['piece'], minQuantity: 0, maxQuantity: 5 },
      { name: 'Barbed Wire', units: ['meter'], minQuantity: 10, maxQuantity: 500, tags: ['defense'] },
      { name: 'Irradiated Beans', units: ['can'], minQuantity: 1, maxQuantity: 100 }
    ]
  };

  // # Mock rationale: Using predefined schema and manifest objects to ensure deterministic and offline testing.
  // # No external file system access or network calls are made.

  it('should validate a perfectly valid manifest', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-001',
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:37:00Z',
      items: [
        { resourceName: 'Water', quantity: 10, unit: 'liter' },
        { resourceName: 'Canned Food', quantity: 20, unit: 'can' },
        { resourceName: 'First Aid Kit', quantity: 2, unit: 'piece' }
      ]
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('should detect unknown resources', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-002',
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:38:00Z',
      items: [
        { resourceName: 'Water', quantity: 5, unit: 'liter' },
        { resourceName: 'Unknown Gadget', quantity: 1, unit: 'piece' } // Unknown
      ]
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Item 2 ("Unknown Gadget"): Resource "Unknown Gadget" is not defined in the schema.');
  });

  it('should detect invalid units for a resource', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-003',
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:39:00Z',
      items: [
        { resourceName: 'Water', quantity: 5, unit: 'gallon' } // Invalid unit for Water
      ]
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Item 1 ("Water"): Unit "gallon" is not allowed for resource "Water" by the schema. Allowed units: liter, ml.');
  });

  it('should detect quantity below minimum', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-004',
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:40:00Z',
      items: [
        { resourceName: 'Barbed Wire', quantity: 5, unit: 'meter' } // Min is 10
      ]
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Item 1 ("Barbed Wire"): Quantity 5 is below the minimum allowed (10) for resource "Barbed Wire".');
  });

  it('should detect quantity above maximum', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-005',
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:41:00Z',
      items: [
        { resourceName: 'Canned Food', quantity: 51, unit: 'can' } // Max is 50
      ]
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Item 1 ("Canned Food"): Quantity 51 is above the maximum allowed (50) for resource "Canned Food".');
  });

  it('should detect invalid manifest structure (missing manifestId)', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: any = { // Use 'any' to simulate missing property
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:42:00Z',
      items: []
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Invalid manifest structure: missing manifestId, location, timestamp, or items array.');
  });

  it('should detect invalid timestamp format', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-006',
      location: 'Sector 7G',
      timestamp: 'not-a-date', // Invalid timestamp
      items: []
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(false);
    expect(result.errors).toContain('Invalid timestamp format for manifestId "shelter-alpha-006": "not-a-date" is not a valid ISO 8601 date.');
  });

  it('should handle zero quantity if allowed by schema', () => {
    const validator = new ManifestValidator(validSchema);
    const manifest: ResourceManifest = {
      manifestId: 'shelter-alpha-007',
      location: 'Sector 7G',
      timestamp: '2077-10-23T13:43:00Z',
      items: [
        { resourceName: 'First Aid Kit', quantity: 0, unit: 'piece' } // Min is 0
      ]
    };
    const result = validator.validateManifest(manifest);
    expect(result.isValid).toBe(true);
    expect(result.errors).toEqual([]);
  });

  it('should reject schema with invalid unit', () => {
    const invalidSchema: ResourceSchema = {
      version: '1.0',
      name: 'BadSchema',
      resources: [
        { name: 'Broken Item', units: ['furlong'] } as ResourceSchemaItem // Invalid unit
      ]
    };
    expect(() => new ManifestValidator(invalidSchema)).toThrow('Invalid unit "furlong" for resource "Broken Item".');
  });

  it('should reject schema with minQuantity > maxQuantity', () => {
    const invalidSchema: ResourceSchema = {
      version: '1.0',
      name: 'BadSchemaRange',
      resources: [
        { name: 'Confused Item', units: ['piece'], minQuantity: 10, maxQuantity: 5 }
      ]
    };
    expect(() => new ManifestValidator(invalidSchema)).toThrow('Invalid quantity range for resource "Confused Item": minQuantity cannot be greater than maxQuantity.');
  });

  it('should reject schema with missing resource name', () => {
    const invalidSchema: ResourceSchema = {
      version: '1.0',
      name: 'BadSchemaMissingName',
      resources: [
        { units: ['piece'] } as ResourceSchemaItem // Simulate missing name
      ]
    };
    expect(() => new ManifestValidator(invalidSchema)).toThrow('Invalid schema item: missing name or units for resource "unknown".');
  });
});
