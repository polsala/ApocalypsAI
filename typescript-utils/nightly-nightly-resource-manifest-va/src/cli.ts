#!/usr/bin/env node
import { readFileSync } from 'fs';
import { ManifestValidator } from './index';
import { ResourceSchema, ResourceManifest } from './types';

function runCli() {
  const args = process.argv.slice(2);

  if (args.length < 2 || args[0] !== 'validate') {
    console.log('Usage: nrmv validate <schema-file.json> <manifest-file.json>');
    process.exit(1);
  }

  const schemaFilePath = args[1];
  const manifestFilePath = args[2];

  try {
    const schemaContent = readFileSync(schemaFilePath, 'utf8');
    const manifestContent = readFileSync(manifestFilePath, 'utf8');

    const schema: ResourceSchema = JSON.parse(schemaContent);
    const manifest: ResourceManifest = JSON.parse(manifestContent);

    const validator = new ManifestValidator(schema);
    const result = validator.validateManifest(manifest);

    if (result.isValid) {
      console.log(`✅ Manifest "${manifest.manifestId}" at "${manifest.location}" is valid according to schema "${schema.name}".`);
      process.exit(0);
    } else {
      console.error(`❌ Manifest "${manifest.manifestId}" at "${manifest.location}" is INVALID.`);
      result.errors.forEach(error => console.error(`  - ${error}`));
      process.exit(1);
    }
  } catch (error: any) {
    console.error(`An error occurred: ${error.message}`);
    process.exit(1);
  }
}

runCli();
