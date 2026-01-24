export interface LineFlicker {
  lineNumber: number;
  originalLine: string;
  echoLine: string;
  flickerMarkers: string; // e.g., "      ^^^^^" where ^ indicates a difference
}

export type FlickerReport = LineFlicker[];

/**
 * Compares two lines character by character and generates a flicker marker string.
 * @param lineA The original line.
 * @param lineB The echo line.
 * @returns A string with spaces for identical characters and '^' for differences.
 */
function generateFlickerMarkers(lineA: string, lineB: string): string {
  const maxLength = Math.max(lineA.length, lineB.length);
  let markers = '';
  for (let i = 0; i < maxLength; i++) {
    const charA = lineA[i] || ' '; // Pad shorter line with space for comparison
    const charB = lineB[i] || ' '; // Pad shorter line with space for comparison
    markers += (charA === charB) ? ' ' : '^';
  }
  return markers;
}

/**
 * Detects character-level "flicker" differences between two text contents.
 * @param fileAContent The content of the original file (Temporal Anchor).
 * @param fileBContent The content of the echo file (Temporal Echo).
 * @returns A FlickerReport detailing all detected differences.
 */
export function detectFlicker(fileAContent: string, fileBContent: string): FlickerReport {
  const linesA = fileAContent.split('\n');
  const linesB = fileBContent.split('\n');
  const maxLength = Math.max(linesA.length, linesB.length);

  const report: FlickerReport = [];

  for (let i = 0; i < maxLength; i++) {
    const lineA = linesA[i] !== undefined ? linesA[i] : '';
    const lineB = linesB[i] !== undefined ? linesB[i] : '';

    if (lineA !== lineB) {
      report.push({
        lineNumber: i + 1,
        originalLine: lineA,
        echoLine: lineB,
        flickerMarkers: generateFlickerMarkers(lineA, lineB),
      });
    }
  }

  return report;
}
