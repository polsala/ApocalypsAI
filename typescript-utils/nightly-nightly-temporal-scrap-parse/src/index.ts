import { ScrapedDate, Confidence } from './types';

// Helper to check if a Date object is valid
function isValidDate(date: Date): boolean {
  return !isNaN(date.getTime());
}

// Function to parse a date string with various formats and assign confidence
export function parseScrapedDate(dateString: string): ScrapedDate {
  const trimmedString = dateString.trim();

  // Try ISO 8601 and common formats first (high confidence)
  const highConfidenceFormats = [
    /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z?$/, // ISO 8601 (with or without milliseconds, with or without Z)
    /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/, // YYYY-MM-DD HH:mm:ss
    /^\d{4}\/\d{2}\/\d{2} \d{2}:\d{2}:\d{2}$/, // YYYY/MM/DD HH:mm:ss
    /^\d{4}-\d{2}-\d{2}$/, // YYYY-MM-DD
    /^\d{4}\/\d{2}\/\d{2}$/, // YYYY/MM/DD
    /^[A-Za-z]{3}, \d{2} [A-Za-z]{3} \d{4} \d{2}:\d{2}:\d{2} GMT$/, // RFC 2822 (e.g., "Thu, 01 Jan 1970 00:00:00 GMT")
  ];

  for (const regex of highConfidenceFormats) {
    if (regex.test(trimmedString)) {
      const date = new Date(trimmedString);
      if (isValidDate(date)) {
        return { original: dateString, parsed: date, confidence: 'High' };
      }
    }
  }

  // Try medium confidence formats
  const mediumConfidenceFormats = [
    /^\d{2}\/\d{2}\/\d{4}( \d{2}:\d{2}:\d{2})?$/, // MM/DD/YYYY or MM/DD/YYYY HH:mm:ss
    /^\d{2}-\d{2}-\d{4}( \d{2}:\d{2}:\d{2})?$/, // MM-DD-YYYY or MM-DD-YYYY HH:mm:ss
    /^\d{2}\/\d{2}\/\d{2}( \d{2}:\d{2}:\d{2})?$/, // MM/DD/YY or MM/DD/YY HH:mm:ss (ambiguous year, but common)
    /^\d{2}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$/, // MM-DD-YY or MM-DD-YY HH:mm:ss
    /^[A-Za-z]+ \d{1,2}, \d{4}( \d{1,2}:\d{2}(:\d{2})? (AM|PM))?$/, // "Month DD, YYYY" or "Month DD, YYYY HH:MM:SS AM/PM"
  ];

  for (const regex of mediumConfidenceFormats) {
    if (regex.test(trimmedString)) {
      const date = new Date(trimmedString);
      if (isValidDate(date)) {
        return { original: dateString, parsed: date, confidence: 'Medium' };
      }
    }
  }

  // Try low confidence formats (more ambiguous, less precise)
  // This catches formats that Date.parse might handle but are not explicitly
  // covered by the above regexes, or are inherently ambiguous.
  const date = new Date(trimmedString);
  if (isValidDate(date)) {
    return { original: dateString, parsed: date, confidence: 'Low' };
  }

  // If all else fails
  return { original: dateString, parsed: null, confidence: 'None', error: 'Could not parse date string.' };
}

// CLI entry point
export function runCli(args: string[]): void {
  if (args.length < 1) {
    console.log("Usage: npm start <date_string>");
    console.log("Example: npm start '2023-10-27 14:30:00'");
    console.log("Example: npm start 'Oct 27, 2023'");
    return;
  }

  const dateString = args.join(' ');
  const result = parseScrapedDate(dateString);

  console.log(`Original: "${result.original}"`);
  console.log(`Parsed: ${result.parsed ? result.parsed.toISOString() : 'N/A'}`);
  console.log(`Confidence: ${result.confidence}`);
  if (result.error) {
    console.error(`Error: ${result.error}`);
  }
}

// If this file is run directly (e.g., `node dist/index.js "some date"`), execute CLI.
if (require.main === module) {
  // Slice off 'node' and 'dist/index.js'
  runCli(process.argv.slice(2));
}
