export type ResourceUnit = 'kg' | 'g' | 'liter' | 'ml' | 'piece' | 'can' | 'box' | 'meter' | 'foot' | 'unit';

export interface ResourceSchemaItem {
  name: string;
  description?: string;
  units: ResourceUnit[];
  minQuantity?: number;
  maxQuantity?: number;
  tags?: string[];
}

export interface ResourceSchema {
  version: string;
  name: string;
  description?: string;
  resources: ResourceSchemaItem[];
}

export interface ManifestItem {
  resourceName: string;
  quantity: number;
  unit: ResourceUnit;
}

export interface ResourceManifest {
  manifestId: string;
  location: string;
  timestamp: string; // ISO 8601
  items: ManifestItem[];
}

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}
