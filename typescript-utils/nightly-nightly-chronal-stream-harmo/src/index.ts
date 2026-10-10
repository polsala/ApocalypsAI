export interface ChronalEvent<T> {
  id: string;
  timestamp: number; // Unix timestamp (milliseconds)
  payload: T;
}

/**
 * The ChronalStreamHarmonizer class processes event streams, harmonizing chronal echoes
 * and ensuring ordered, de-duplicated delivery despite temporal distortions.
 * It maintains a collection of unique events, keeping only the latest version of each
 * based on its ID and timestamp, and provides them in chronological order.
 */
export class ChronalStreamHarmonizer<T> {
  private events: Map<string, ChronalEvent<T>>;

  constructor() {
    this.events = new Map();
  }

  /**
   * Adds a chronal event to the harmonizer.
   * If an event with the same ID already exists, it will be updated
   * only if the new event has a more recent timestamp. Events with older
   * timestamps for an existing ID are ignored.
   * @param event The chronal event to add.
   */
  addEvent(event: ChronalEvent<T>): void {
    const existingEvent = this.events.get(event.id);
    if (!existingEvent || event.timestamp > existingEvent.timestamp) {
      this.events.set(event.id, event);
    }
  }

  /**
   * Retrieves the harmonized stream of events.
   * Events are de-duplicated by ID (keeping the latest version) and
   * sorted chronologically by timestamp. For events with identical timestamps,
   * a stable sort by ID is applied to ensure consistent output.
   * @returns An array of harmonized chronal events.
   */
  getHarmonizedStream(): ChronalEvent<T>[] {
    const harmonized = Array.from(this.events.values());
    harmonized.sort((a, b) => {
      if (a.timestamp === b.timestamp) {
        // Stable sort for events with identical timestamps by ID
        return a.id.localeCompare(b.id);
      }
      return a.timestamp - b.timestamp;
    });
    return harmonized;
  }

  /**
   * Clears all events from the harmonizer, resetting its internal state.
   */
  clear(): void {
    this.events.clear();
  }

  /**
   * Returns the current number of unique events stored in the harmonizer.
   * @returns The number of unique events.
   */
  size(): number {
    return this.events.size;
  }
}
