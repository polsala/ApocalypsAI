import { TemporalEcho, HarmonizationStrategy, AlignedEchoGroup, Discrepancy } from './types';

/**
 * Aligns multiple temporal echo streams by timestamp.
 * Missing timestamps in a stream will result in that stream not contributing to the group at that timestamp.
 * @param echoStreams An array of arrays, where each inner array is a temporal echo stream.
 * @returns An array of AlignedEchoGroup, sorted by timestamp.
 */
export function alignEchoStreams(echoStreams: TemporalEcho[][]): AlignedEchoGroup[] {
  const allTimestamps = new Set<number>();
  echoStreams.forEach(stream => stream.forEach(echo => allTimestamps.add(echo.timestamp)));

  const sortedTimestamps = Array.from(allTimestamps).sort((a, b) => a - b);

  const alignedGroups: AlignedEchoGroup[] = [];

  for (const timestamp of sortedTimestamps) {
    const group: TemporalEcho[] = [];
    for (const stream of echoStreams) {
      const echoAtTimestamp = stream.find(echo => echo.timestamp === timestamp);
      if (echoAtTimestamp) {
        group.push(echoAtTimestamp);
      }
    }
    // Only add groups that actually have echoes present at this timestamp
    if (group.length > 0) {
      alignedGroups.push({ timestamp, echoes: group });
    }
  }

  return alignedGroups;
}

/**
 * Detects discrepancies within aligned echo groups.
 * A discrepancy is identified if the values in a group deviate significantly.
 * @param alignedGroups The output from alignEchoStreams.
 * @param threshold The maximum allowed percentage deviation (e.g., 0.1 for 10%).
 * @returns An array of Discrepancy objects.
 */
export function detectDiscrepancies(alignedGroups: AlignedEchoGroup[], threshold: number = 0.1): Discrepancy[] {
  const discrepancies: Discrepancy[] = [];

  for (const group of alignedGroups) {
    if (group.echoes.length < 2) continue; // Need at least two echoes to compare

    const values = group.echoes.map(e => e.value);
    const sum = values.reduce((s, val) => s + val, 0);
    const average = sum / values.length;

    if (average === 0) {
      // If average is 0, check if all values are 0. If not, it's a discrepancy.
      if (values.some(val => val !== 0)) {
        // Max deviation from 0 for non-zero values is infinite, so we just flag it if any non-zero exists.
        // For simplicity, if average is 0 and not all values are 0, it's a discrepancy.
        discrepancies.push({
          timestamp: group.timestamp,
          alignedGroup: group,
          deviation: Infinity, // Indicate a severe deviation from zero
        });
      }
      continue;
    }

    const maxDeviation = Math.max(...values.map(val => Math.abs(val - average) / average));

    if (maxDeviation > threshold) {
      discrepancies.push({
        timestamp: group.timestamp,
        alignedGroup: group,
        deviation: maxDeviation,
      });
    }
  }

  return discrepancies;
}

/**
 * Harmonizes aligned echo groups into a single timeline using a specified strategy.
 * @param alignedGroups The output from alignEchoStreams.
 * @param strategy The harmonization strategy to apply.
 * @returns A single TemporalEcho stream representing the harmonized timeline.
 */
export function harmonizeEchoes(alignedGroups: AlignedEchoGroup[], strategy: HarmonizationStrategy = 'average'): TemporalEcho[] {
  const harmonizedTimeline: TemporalEcho[] = [];

  for (const group of alignedGroups) {
    if (group.echoes.length === 0) continue;

    let harmonizedValue: number;
    const values = group.echoes.map(e => e.value);

    switch (strategy) {
      case 'average':
        harmonizedValue = values.reduce((sum, val) => sum + val, 0) / values.length;
        break;
      case 'median':
        const sortedValues = [...values].sort((a, b) => a - b);
        const mid = Math.floor(sortedValues.length / 2);
        harmonizedValue = sortedValues.length % 2 === 0
          ? (sortedValues[mid - 1] + sortedValues[mid]) / 2
          : sortedValues[mid];
        break;
      case 'first':
        harmonizedValue = group.echoes[0].value;
        break;
      case 'last':
        harmonizedValue = group.echoes[group.echoes.length - 1].value;
        break;
      default:
        throw new Error(`Unknown harmonization strategy: ${strategy}`);
    }

    harmonizedTimeline.push({
      timestamp: group.timestamp,
      value: harmonizedValue,
      source: 'Harmonized', // Indicate that this value is a result of harmonization
    });
  }

  return harmonizedTimeline;
}
