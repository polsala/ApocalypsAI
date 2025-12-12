/**
 * Represents an inconsistency found in the temporal order of events.
 */
export interface TemporalInconsistency<T extends { [key: string]: any }> {
  event: T;
  index: number;
  previousTimestamp: number;
}

/**
 * A utility to check the temporal consistency of an event log.
 * Ensures that events are ordered chronologically based on a specified timestamp field.
 */
export class TemporalSyncChecker<T extends { [key: string]: any }> {
  private timestampField: keyof T;

  /**
   * Initializes the TemporalSyncChecker.
   * @param timestampField The name of the field in the event object that holds the timestamp.
   */
  constructor(timestampField: keyof T) {
    if (!timestampField) {
      throw new Error('Timestamp field must be provided.');
    }
    this.timestampField = timestampField;
  }

  /**
   * Checks an array of events for temporal consistency.
   * @param log An array of event objects.
   * @returns An array of TemporalInconsistency objects, detailing any out-of-order events.
   */
  public checkLog(log: T[]): TemporalInconsistency<T>[] {
    const inconsistencies: TemporalInconsistency<T>[] = [];
    if (!log || log.length === 0) {
      return inconsistencies;
    }

    let previousTimestamp: number | null = null;

    for (let i = 0; i < log.length; i++) {
      const currentEvent = log[i];
      const currentTimestamp = currentEvent[this.timestampField];

      if (typeof currentTimestamp !== 'number') {
        console.warn(`Warning: Event at index ${i} has a non-numeric timestamp for field '${String(this.timestampField)}'. Skipping temporal check for this event.`);
        continue;
      }

      if (previousTimestamp !== null && currentTimestamp < previousTimestamp) {
        inconsistencies.push({
          event: currentEvent,
          index: i,
          previousTimestamp: previousTimestamp,
        });
      }
      previousTimestamp = currentTimestamp;
    }

    return inconsistencies;
  }
}
