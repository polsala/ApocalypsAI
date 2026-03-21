export interface DataItem {
  [key: string]: any;
}

export class DataDicer<T extends DataItem> {
  private currentData: T[];

  constructor(initialData: T[]) {
    this.currentData = [...initialData]; // Work on a copy to avoid modifying original array
  }

  /**
   * Filters the data based on a predicate function.
   * @param predicate A function that returns true for items to keep.
   */
  filter(predicate: (item: T) => boolean): DataDicer<T> {
    this.currentData = this.currentData.filter(predicate);
    return this;
  }

  /**
   * Randomly samples N items from the data.
   * @param count The number of items to sample.
   * @param seed Optional seed for deterministic sampling. If not provided, uses Date.now().
   */
  sample(count: number, seed?: number): DataDicer<T> {
    if (count >= this.currentData.length) {
      return this; // No need to sample if count is greater or equal to current data length
    }

    // # Mock rationale: Math.random is non-deterministic. For testing, a fixed seed is crucial.
    // This pseudo-random number generator (PRNG) is implemented directly within the method
    // to ensure deterministic behavior when a seed is provided, without relying on global mocks.
    const pseudoRandom = (function() {
      let s = seed !== undefined ? seed : Date.now();
      return function() {
        s = (s * 9301 + 49297) % 233280;
        return s / 233280;
      };
    })();

    const shuffled = [...this.currentData];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(pseudoRandom() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    this.currentData = shuffled.slice(0, count);
    return this;
  }

  /**
   * Selects only specified keys from each item.
   * @param keys An array of keys to pick.
   */
  pick<K extends keyof T>(keys: K[]): DataDicer<Pick<T, K>> {
    this.currentData = this.currentData.map(item => {
      const newItem: Partial<T> = {};
      for (const key of keys) {
        if (Object.prototype.hasOwnProperty.call(item, key)) {
          newItem[key] = item[key];
        }
      }
      return newItem as Pick<T, K>;
    }) as any; // Type assertion needed due to generic transformation
    return this as any;
  }

  /**
   * Omits specified keys from each item.
   * @param keys An array of keys to omit.
   */
  omit<K extends keyof T>(keys: K[]): DataDicer<Omit<T, K>> {
    this.currentData = this.currentData.map(item => {
      const newItem: Partial<T> = { ...item };
      for (const key of keys) {
        delete newItem[key];
      }
      return newItem as Omit<T, K>;
    }) as any; // Type assertion needed due to generic transformation
    return this as any;
  }

  /**
   * Sorts the data by a specified key.
   * Supports string and number comparisons.
   * @param key The key to sort by.
   * @param ascending True for ascending (default), false for descending.
   */
  sort(key: keyof T, ascending: boolean = true): DataDicer<T> {
    this.currentData.sort((a, b) => {
      const valA = a[key];
      const valB = b[key];

      if (typeof valA === 'string' && typeof valB === 'string') {
        return ascending ? valA.localeCompare(valB) : valB.localeCompare(valA);
      }
      if (typeof valA === 'number' && typeof valB === 'number') {
        return ascending ? valA - valB : valB - valA;
      }
      // Fallback for other types or mixed types, treating them as comparable
      if (valA < valB) return ascending ? -1 : 1;
      if (valA > valB) return ascending ? 1 : -1;
      return 0;
    });
    return this;
  }

  /**
   * Executes all chained operations and returns the final data.
   */
  execute(): T[] {
    return this.currentData;
  }
}
