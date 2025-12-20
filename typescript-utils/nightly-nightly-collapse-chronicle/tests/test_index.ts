import { getElapsed } from "../src/index";
import * as assert from "assert";

/**
 * Mock rationale: replace the global Date constructor so that `new Date()`
 * returns a predictable timestamp without needing external libraries.
 */
function mockNow(iso: string): void {
  const RealDate = Date as any;
  // @ts-ignore
  global.Date = class extends RealDate {
    constructor(...args: any[]) {
      if (args.length === 0) {
        super(iso);
      } else {
        super(...args);
      }
    }
    static now() {
      return new RealDate(iso).getTime();
    }
  } as any;
}

function restoreDate(): void {
  // @ts-ignore
  global.Date = Date;
}

// Mock the current time to exactly one day, three hours, four minutes and five seconds
// after the collapse.
mockNow("2023-01-02T03:04:05Z");
const elapsed = getElapsed(new Date("2023-01-01T00:00:00Z"), new Date());
assert.deepStrictEqual(elapsed, { days: 1, hours: 3, minutes: 4, seconds: 5 });
restoreDate();

console.log("All tests passed.");
