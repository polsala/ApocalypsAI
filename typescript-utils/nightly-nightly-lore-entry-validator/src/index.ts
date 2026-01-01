import { LoreEntrySchema, LoreEntry } from './schema';
import { ZodError } from 'zod';
import * as fs from 'fs';
import * as path from 'path';

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  data?: LoreEntry;
}

/**
 * Validates an unknown object against the LoreEntry schema.
 * @param entryData The data to validate.
 * @returns A ValidationResult indicating success or failure and any errors.
 */
export function validateLoreEntry(entryData: unknown): ValidationResult {
  try {
    const parsedEntry = LoreEntrySchema.parse(entryData);
    return { isValid: true, errors: [], data: parsedEntry };
  } catch (error) {
    if (error instanceof ZodError) {
      const errorMessages = error.errors.map(err => {
        const path = err.path.join('.');
        return path ? `${path}: ${err.message}` : err.message; // Handle root-level errors gracefully
      });
      return { isValid: false, errors: errorMessages };
    }
    return { isValid: false, errors: [`An unexpected error occurred: ${(error as Error).message}`] };
  }
}

// Basic CLI functionality
if (require.main === module) {
  const filePath = process.argv[2];

  if (!filePath) {
    console.error("Usage: ts-node src/index.ts <path-to-lore-entry.json>");
    process.exit(1);
  }

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const entry = JSON.parse(fileContent);
    const result = validateLoreEntry(entry);

    if (result.isValid) {
      console.log("\u2705 Lore entry is valid!");
      console.log(JSON.stringify(result.data, null, 2));
    } else {
      console.error("\u274C Lore entry is INVALID:");
      result.errors.forEach(err => console.error(`  - ${err}`));
      process.exit(1);
    }
  } catch (error) {
    if (error instanceof SyntaxError) {
      console.error(`\u274C Failed to parse JSON from ${filePath}: ${error.message}`);
    } else if (error instanceof Error && 'code' in error && error.code === 'ENOENT') {
      console.error(`\u274C File not found: ${filePath}`);
    } else {
      console.error(`\u274C An unexpected error occurred: ${(error as Error).message}`);
    }
    process.exit(1);
  }
}
