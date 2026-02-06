import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { Manifest, ManifestItem, MendingSuggestion, MendingSeverity } from './manifestTypes';

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

// Default basic schema for a survival manifest
export const defaultManifestSchema = {
  type: 'object',
  properties: {
    items: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', minLength: 1 },
          quantity: { type: 'number', minimum: 0 },
          category: { type: 'string' },
          tags: { type: 'array', items: { type: 'string' } },
          expiryDate: { type: 'string', format: 'date' }
        },
        required: ['name', 'quantity'],
        additionalProperties: false
      }
    },
    location: { type: 'string' },
    lastUpdated: { type: 'string', format: 'date-time' }
  },
  required: ['items'],
  additionalProperties: false
};

/**
 * Validates a manifest against a given JSON Schema and generates mending suggestions.
 * @param manifest The manifest object to validate.
 * @param schema The JSON Schema object to validate against. Defaults to `defaultManifestSchema`.
 * @returns An object containing validation status, errors, and mending suggestions.
 */
export function validateAndMendManifest(
  manifest: Manifest,
  schema: object = defaultManifestSchema
): { isValid: boolean; errors: any[] | null | undefined; suggestions: MendingSuggestion[] } {
  const validate = ajv.compile(schema);
  const isValid = validate(manifest);
  const errors = validate.errors;

  const suggestions: MendingSuggestion[] = [];

  // --- Apocalyptic Mending Rules ---

  // Rule 1: Hydration Imperative
  const hasWater = manifest.items.some(item =>
    item.name.toLowerCase().includes('water') || item.category?.toLowerCase() === 'hydration'
  );
  if (!hasWater) {
    suggestions.push({
      type: 'add',
      item: 'Water',
      suggestion: 'Critical: Add a reliable water source or purification tablets.',
      rationale: 'Hydration is paramount for survival. The void demands it!',
      severity: 'critical'
    });
  }

  // Rule 2: First Aid Readiness
  const hasFirstAid = manifest.items.some(item =>
    item.name.toLowerCase().includes('first aid') || item.category?.toLowerCase() === 'medical'
  );
  if (!hasFirstAid) {
    suggestions.push({
      type: 'add',
      item: 'First Aid Kit',
      suggestion: 'Warning: Ensure a comprehensive first aid kit is present.',
      rationale: 'Minor scrapes can become major problems in the wasteland. Be prepared!',
      severity: 'warning'
    });
  }

  // Rule 3: Tool Redundancy Protocol
  const sharpTools = manifest.items.filter(item =>
    ['knife', 'blade', 'machete', 'axe', 'saw'].some(tool => item.name.toLowerCase().includes(tool))
  );
  if (sharpTools.length > 2) {
    suggestions.push({
      type: 'consolidate',
      item: 'Sharp Tools',
      suggestion: `Info: You have ${sharpTools.length} sharp tools. Consider consolidating or diversifying your toolkit.`, 
      rationale: 'While sharp, too many of the same tool can be inefficient. Optimize your carry weight!',
      severity: 'info'
    });
  }

  // Rule 4: Luxury Overload Directive
  const luxuryItems = manifest.items.filter(item =>
    ['chocolate', 'coffee', 'gourmet', 'wine', 'spirits'].some(luxury => item.name.toLowerCase().includes(luxury))
  );
  const totalItems = manifest.items.reduce((sum, item) => sum + item.quantity, 0);
  const luxuryQuantity = luxuryItems.reduce((sum, item) => sum + item.quantity, 0);

  if (totalItems > 0 && (luxuryQuantity / totalItems) > 0.2) {
    suggestions.push({
      type: 'adjust',
      item: 'Luxury Items',
      suggestion: 'Warning: Your manifest shows a high proportion of luxury items. Consider balancing with more staples.',
      rationale: 'Comfort is good, but sustenance is better. Prioritize survival rations!',
      severity: 'warning'
    });
  }

  // Rule 5: Expired Goods Alert
  const today = new Date();
  const expiredItems = manifest.items.filter(item => {
    if (item.expiryDate) {
      const expiry = new Date(item.expiryDate);
      return expiry < today;
    }
    return false;
  });
  if (expiredItems.length > 0) {
    suggestions.push({
      type: 'remove',
      item: expiredItems.map(i => i.name).join(', '),
      suggestion: `Warning: ${expiredItems.length} items have expired. Remove them from your manifest.`, 
      rationale: 'The wasteland is unforgiving. Do not rely on spoiled provisions!',
      severity: 'warning'
    });
  }

  return { isValid, errors, suggestions };
}
