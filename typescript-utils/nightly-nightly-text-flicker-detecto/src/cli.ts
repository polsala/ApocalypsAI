import * as fs from 'fs';
import * as path from 'path';
import { detectFlicker, LineFlicker } from './diff';

/**
 * Main function to run the CLI utility.
 */
export function runCli(): void {
  const args = process.argv.slice(2);

  if (args.length !== 2) {
    console.error('Usage: node dist/cli.js <path_to_file_A> <path_to_file_B>');
    process.exit(1);
  }

  const [fileAPath, fileBPath] = args;

  try {
    // Mock rationale: fs.readFileSync is mocked in tests to provide deterministic file content
    // without actual file I/O, ensuring tests are fast and isolated.
    const fileAContent = fs.readFileSync(fileAPath, 'utf8');
    const fileBContent = fs.readFileSync(fileBPath, 'utf8');

    const report = detectFlicker(fileAContent, fileBContent);

    // For the summary, we need the actual number of lines from the files.
    const totalLines = Math.max(fileAContent.split('\n').length, fileBContent.split('\n').length);

    console.log('Temporal Flicker Report:');
    console.log(`Comparing '${fileAPath}' (Temporal Anchor) with '${fileBPath}' (Temporal Echo)\n`);

    if (report.length === 0) {
      console.log('No flicker detected. Files are identical.');
      return;
    }

    for (const lineFlicker of report) {
      console.log(`--- Line ${lineFlicker.lineNumber} ---`);
      console.log(`Original: ${lineFlicker.originalLine}`);
      console.log(`Echo:     ${lineFlicker.echoLine}`);
      console.log(`Flicker:  ${lineFlicker.flickerMarkers}\n`);
    }

    console.log('--- Summary ---');
    console.log(`Total lines compared: ${totalLines}`);
    console.log(`Lines with flicker: ${report.length}`);

  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

// Only run CLI if executed directly
if (require.main === module) {
  runCli();
}
