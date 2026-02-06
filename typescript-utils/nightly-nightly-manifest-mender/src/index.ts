import { Command } from 'commander';
import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { validateAndMendManifest, defaultManifestSchema } from './mender';
import { Manifest, MendingSuggestion } from './manifestTypes';

const program = new Command();

program
  .name('nightly-manifest-mender')
  .description('A type-safe CLI tool to validate and suggest \'mends\' for apocalyptic inventory manifests.')
  .version('1.0.0');

program
  .argument('<manifestPath>', 'Path to the inventory manifest file (JSON or YAML)')
  .option('-s, --schema <path>', 'Path to a custom JSON Schema file for validation')
  .action(async (manifestPath, options) => {
    try {
      const manifestContent = fs.readFileSync(manifestPath, 'utf8');
      let manifest: Manifest;

      if (manifestPath.endsWith('.json')) {
        manifest = JSON.parse(manifestContent);
      } else if (manifestPath.endsWith('.yaml') || manifestPath.endsWith('.yml')) {
        manifest = yaml.load(manifestContent) as Manifest;
      } else {
        console.error('Error: Manifest file must be .json or .yaml/.yml');
        process.exit(1);
      }

      let schema: object = defaultManifestSchema;
      if (options.schema) {
        const schemaContent = fs.readFileSync(options.schema, 'utf8');
        schema = JSON.parse(schemaContent);
      }

      const { isValid, errors, suggestions } = validateAndMendManifest(manifest, schema);

      console.log(`\n--- Manifest Mending Report for '${manifestPath}' ---\n`);

      if (isValid) {
        console.log('✅ Manifest is structurally sound according to schema.');
      } else {
        console.log('❌ Manifest has schema validation errors:');
        errors?.forEach(err => {
          console.log(`  - ${err.instancePath}: ${err.message}`);
        });
      }

      if (suggestions.length > 0) {
        console.log('\n--- ApocalypsAI Mending Suggestions ---');
        suggestions.sort((a, b) => {
          const severityOrder = { 'critical': 0, 'warning': 1, 'info': 2 };
          return severityOrder[a.severity] - severityOrder[b.severity];
        }).forEach(s => {
          const prefix = s.severity === 'critical' ? '🚨 CRITICAL:' : s.severity === 'warning' ? '⚠️ WARNING:' : '💡 INFO:';
          console.log(`\n${prefix} ${s.suggestion}`);
          if (s.item) console.log(`  Item(s) affected: ${s.item}`);
          console.log(`  Rationale: ${s.rationale}`);
        });
      } else {
        console.log('\n✨ No mending suggestions from ApocalypsAI. Your manifest is optimally grim!');
      }

      console.log('\n-------------------------------------------\n');

      if (!isValid || suggestions.some(s => s.severity === 'critical')) {
        process.exit(1); // Exit with error code if validation fails or critical suggestions exist
      }

    } catch (error: any) {
      console.error(`Error processing manifest: ${error.message}`);
      process.exit(1);
    }
  });

program.parse(process.argv);
