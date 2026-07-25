import * as fs from 'fs';
import * as path from 'path';

// --- Type Definitions ---

interface Resource {
  name: string;
  quantity: number;
  unit: string;
  perishable: boolean;
  expiryDate?: string; // ISO 8601 date string if perishable
}

interface Manifest {
  manifestName: string;
  timestamp: string; // ISO 8601 date string
  location: string;
  resources: Resource[];
}

// --- Type Guards for Runtime Validation ---

function isResource(obj: any): obj is Resource {
  if (typeof obj !== 'object' || obj === null) {
    console.error('Validation Error: Resource must be an object.');
    return false;
  }

  if (typeof obj.name !== 'string' || obj.name.trim() === '') {
    console.error('Validation Error: Resource "name" must be a non-empty string.');
    return false;
  }
  if (typeof obj.quantity !== 'number' || obj.quantity < 0 || !Number.isInteger(obj.quantity)) {
    console.error(`Validation Error: Resource "${obj.name}" "quantity" must be a non-negative integer.`);
    return false;
  }
  if (typeof obj.unit !== 'string' || obj.unit.trim() === '') {
    console.error(`Validation Error: Resource "${obj.name}" "unit" must be a non-empty string.`);
    return false;
  }
  if (typeof obj.perishable !== 'boolean') {
    console.error(`Validation Error: Resource "${obj.name}" "perishable" must be a boolean.`);
    return false;
  }

  if (obj.perishable && typeof obj.expiryDate !== 'string') {
    console.error(`Validation Error: Resource "${obj.name}" is perishable but "expiryDate" is missing or not a string.`);
    return false;
  }
  if (obj.expiryDate !== undefined && typeof obj.expiryDate === 'string' && !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$/.test(obj.expiryDate)) {
    console.error(`Validation Error: Resource "${obj.name}" "expiryDate" must be a valid ISO 8601 date string.`);
    return false;
  }

  // Check for unexpected properties (optional, but good for strict validation)
  const allowedResourceKeys = ['name', 'quantity', 'unit', 'perishable', 'expiryDate'];
  for (const key in obj) {
    if (!allowedResourceKeys.includes(key)) {
      console.warn(`Validation Warning: Resource "${obj.name}" has unexpected property "${key}".`);
    }
  }

  return true;
}

function isManifest(obj: any): obj is Manifest {
  if (typeof obj !== 'object' || obj === null) {
    console.error('Validation Error: Manifest must be an object.');
    return false;
  }

  if (typeof obj.manifestName !== 'string' || obj.manifestName.trim() === '') {
    console.error('Validation Error: Manifest "manifestName" must be a non-empty string.');
    return false;
  }
  if (typeof obj.timestamp !== 'string' || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$/.test(obj.timestamp)) {
    console.error('Validation Error: Manifest "timestamp" must be a valid ISO 8601 date string.');
    return false;
  }
  if (typeof obj.location !== 'string' || obj.location.trim() === '') {
    console.error('Validation Error: Manifest "location" must be a non-empty string.');
    return false;
  }
  if (!Array.isArray(obj.resources)) {
    console.error('Validation Error: Manifest "resources" must be an array.');
    return false;
  }

  for (let i = 0; i < obj.resources.length; i++) {
    if (!isResource(obj.resources[i])) {
      console.error(`Validation Error: Invalid resource found at index ${i} in manifest "${obj.manifestName}".`);
      return false;
    }
  }

  // Check for unexpected properties
  const allowedManifestKeys = ['manifestName', 'timestamp', 'location', 'resources'];
  for (const key in obj) {
    if (!allowedManifestKeys.includes(key)) {
      console.warn(`Validation Warning: Manifest "${obj.manifestName}" has unexpected property "${key}".`);
    }
  }

  return true;
}

// --- Main CLI Logic ---

export function validateManifestFile(filePath: string): boolean {
  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const manifestData = JSON.parse(fileContent);

    if (isManifest(manifestData)) {
      console.log(`\n\u001b[32m\u001b[1m✅ Manifest "${manifestData.manifestName}" at "${manifestData.location}" is VALID.\u001b[22m\u001b[39m`);
      console.log(`   Contains ${manifestData.resources.length} unique resource types.`);
      return true;
    } else {
      console.error(`\n\u001b[31m\u001b[1m❌ Manifest validation FAILED for file: ${filePath}\u001b[22m\u001b[39m`);
      // Detailed errors are already logged by isManifest/isResource
      return false;
    }
  } catch (error: any) {
    if (error instanceof SyntaxError) {
      console.error(`\n\u001b[31m\u001b[1m❌ Failed to parse JSON file: ${filePath}. Error: ${error.message}\u001b[22m\u001b[39m`);
    } else if (error.code === 'ENOENT') {
      console.error(`\n\u001b[31m\u001b[1m❌ File not found: ${filePath}\u001b[22m\u001b[39m`);
    } else {
      console.error(`\n\u001b[31m\u001b[1m❌ An unexpected error occurred while processing ${filePath}: ${error.message}\u001b[22m\u001b[39m`);
    }
    return false;
  }
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: ts-node src/index.ts <path-to-manifest.json>');
    process.exit(1);
  }

  const manifestPath = args[0];
  const isValid = validateManifestFile(manifestPath);
  process.exit(isValid ? 0 : 1);
}
