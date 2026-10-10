import { Command } from 'commander';
import * as fs from 'fs';
import { validateData } from './validator';
import { RELIC_SCHEMAS } from './schemas';

const program = new Command();

program
  .name('relic-validate')
  .description('A type-safe CLI tool to validate scavenged data files against predefined "relic" schemas.')
  .version('0.1.0');

program
  .argument('<schema-name>', 'The name of the relic schema to validate against (e.g., ScavengedLog, ResourceManifest)')
  .argument('<data-file>', 'Path to the JSON data file to validate')
  .action((schemaName: string, dataFile: string) => {
    if (!RELIC_SCHEMAS[schemaName]) {
      console.error(`Error: Unknown schema '${schemaName}'. Available schemas: ${Object.keys(RELIC_SCHEMAS).join(', ')}`);
      process.exit(1);
    }

    let rawData: string;
    try {
      rawData = fs.readFileSync(dataFile, 'utf8');
    } catch (error: any) {
      console.error(`Error reading data file '${dataFile}': ${error.message}`);
      process.exit(1);
    }

    let data: any;
    try {
      data = JSON.parse(rawData);
    } catch (error: any) {
      console.error(`Error parsing data file '${dataFile}' as JSON: ${error.message}`);
      process.exit(1);
    }

    const validationResult = validateData(schemaName, data);

    if (validationResult.isValid) {
      console.log(`\n✅ Data in '${dataFile}' successfully validated against schema '${schemaName}'.`);
    } else {
      console.error(`\n❌ Data in '${dataFile}' failed validation against schema '${schemaName}':`);
      validationResult.errors.forEach(error => console.error(`  - ${error}`));
      process.exit(1);
    }
  });

program.parse(process.argv);
