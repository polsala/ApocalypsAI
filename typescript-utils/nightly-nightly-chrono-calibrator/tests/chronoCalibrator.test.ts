import { calibrateTask } from '../src/chronoCalibrator';
import { TemporalChunk } from '../src/types';

describe('calibrateTask', () => {
  // Mock rationale: The calibrateTask function is a pure function that takes inputs
  // and returns a deterministic output. No external dependencies or side effects
  // are involved, so no mocking is strictly necessary for its core logic.
  // We are testing the algorithm's correctness directly.

  it('should return an empty array for 0 minutes', () => {
    const chunks = calibrateTask('No Task', 0);
    expect(chunks).toEqual([]);
  });

  it('should handle a very short task (less than a full work chunk)', () => {
    const chunks = calibrateTask('Quick Check', 10);
    expect(chunks.length).toBe(1);
    expect(chunks[0]).toEqual({
      name: 'Stardust Sprint',
      durationMinutes: 10,
      type: 'work',
      description: "Focused work on 'Quick Check'"
    });
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(10);
  });

  it('should handle a single work chunk with a short break', () => {
    const chunks = calibrateTask('Single Focus', 30);
    expect(chunks.length).toBe(2);
    expect(chunks[0]).toEqual({
      name: 'Stardust Sprint',
      durationMinutes: 25,
      type: 'work',
      description: "Focused work on 'Single Focus'"
    });
    expect(chunks[1]).toEqual({
      name: 'Nebula Nudge',
      durationMinutes: 5,
      type: 'short-break',
      description: 'Quick break, refocus'
    });
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(30);
  });

  it('should handle a task that perfectly fits two work chunks and a break', () => {
    const chunks = calibrateTask('Two Sprints', 55); // 25 work + 5 break + 25 work
    expect(chunks.length).toBe(3);
    expect(chunks[0].type).toBe('work');
    expect(chunks[0].durationMinutes).toBe(25);
    expect(chunks[1].type).toBe('short-break');
    expect(chunks[1].durationMinutes).toBe(5);
    expect(chunks[2].type).toBe('work');
    expect(chunks[2].durationMinutes).toBe(25);
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(55);
  });

  it('should handle a task that requires a long break (after 4 work chunks)', () => {
    const chunks = calibrateTask('Long Project', 120);
    // Expected breakdown for 120 minutes:
    // 1. Work: 25 min (rem 95)
    // 2. Break: 5 min (rem 90)
    // 3. Work: 25 min (rem 65)
    // 4. Break: 5 min (rem 60)
    // 5. Work: 25 min (rem 35)
    // 6. Break: 5 min (rem 30)
    // 7. Work: 25 min (rem 5) - This is the 4th work chunk
    // 8. Long Break: 5 min (rem 0) - Remaining 5 minutes used as a long break
    expect(chunks.length).toBe(8);
    expect(chunks[0].type).toBe('work'); expect(chunks[0].durationMinutes).toBe(25);
    expect(chunks[1].type).toBe('short-break'); expect(chunks[1].durationMinutes).toBe(5);
    expect(chunks[2].type).toBe('work'); expect(chunks[2].durationMinutes).toBe(25);
    expect(chunks[3].type).toBe('short-break'); expect(chunks[3].durationMinutes).toBe(5);
    expect(chunks[4].type).toBe('work'); expect(chunks[4].durationMinutes).toBe(25);
    expect(chunks[5].type).toBe('short-break'); expect(chunks[5].durationMinutes).toBe(5);
    expect(chunks[6].type).toBe('work'); expect(chunks[6].durationMinutes).toBe(25); // 4th work chunk
    expect(chunks[7].type).toBe('long-break'); expect(chunks[7].durationMinutes).toBe(5); // Remaining 5 minutes used as long break
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(120);
  });

  it('should handle a task that ends exactly on a work chunk boundary', () => {
    const chunks = calibrateTask('Exact Work', 25);
    expect(chunks.length).toBe(1);
    expect(chunks[0].type).toBe('work');
    expect(chunks[0].durationMinutes).toBe(25);
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(25);
  });

  it('should handle a task that ends exactly on a short break boundary', () => {
    const chunks = calibrateTask('Exact Break', 30); // 25 work + 5 break
    expect(chunks.length).toBe(2);
    expect(chunks[0].type).toBe('work');
    expect(chunks[0].durationMinutes).toBe(25);
    expect(chunks[1].type).toBe('short-break');
    expect(chunks[1].durationMinutes).toBe(5);
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(30);
  });

  it('should handle a task that ends exactly on a long break boundary (after 4 work chunks)', () => {
    const chunks = calibrateTask('Exact Long Break', 115);
    // Expected breakdown for 115 minutes:
    // 1. Work: 25 (rem 90)
    // 2. Break: 5 (rem 85)
    // 3. Work: 25 (rem 60)
    // 4. Break: 5 (rem 55)
    // 5. Work: 25 (rem 30)
    // 6. Break: 5 (rem 25)
    // 7. Work: 25 (rem 0) - This is the 4th work chunk. No break should follow as remainingMinutes is 0.
    expect(chunks.length).toBe(7);
    expect(chunks[0].type).toBe('work'); expect(chunks[0].durationMinutes).toBe(25);
    expect(chunks[1].type).toBe('short-break'); expect(chunks[1].durationMinutes).toBe(5);
    expect(chunks[2].type).toBe('work'); expect(chunks[2].durationMinutes).toBe(25);
    expect(chunks[3].type).toBe('short-break'); expect(chunks[3].durationMinutes).toBe(5);
    expect(chunks[4].type).toBe('work'); expect(chunks[4].durationMinutes).toBe(25);
    expect(chunks[5].type).toBe('short-break'); expect(chunks[5].durationMinutes).toBe(5);
    expect(chunks[6].type).toBe('work'); expect(chunks[6].durationMinutes).toBe(25);
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(115);
  });

  it('should ensure descriptions are correctly formatted with task name', () => {
    const task = 'Deep Dive Research';
    const chunks = calibrateTask(task, 40);
    expect(chunks[0].description).toContain(task);
    expect(chunks[0].description).toBe(`Focused work on '${task}'`);
  });

  it('should handle a task duration that is not a multiple of 5', () => {
    const chunks = calibrateTask('Odd Task', 27);
    // Expected breakdown for 27 minutes:
    // 1. Work: 25 min (rem 2)
    // 2. Break: 2 min (rem 0) - Remaining 2 minutes used as a short break
    expect(chunks.length).toBe(2);
    expect(chunks[0]).toEqual({
      name: 'Stardust Sprint',
      durationMinutes: 25,
      type: 'work',
      description: "Focused work on 'Odd Task'"
    });
    expect(chunks[1]).toEqual({
      name: 'Nebula Nudge',
      durationMinutes: 2,
      type: 'short-break',
      description: 'Quick break, refocus'
    });
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(27);
  });

  it('should handle a task duration that is slightly more than a long break boundary', () => {
    const chunks = calibrateTask('Beyond Long Break', 116);
    // Expected breakdown for 116 minutes:
    // 7 chunks for 115 minutes (4 work, 3 short breaks) as per previous test.
    // Then 1 minute remaining.
    // The loop will then try to add a work chunk, but remainingMinutes is 1.
    // 1. Work: 25 (rem 91)
    // 2. Break: 5 (rem 86)
    // 3. Work: 25 (rem 61)
    // 4. Break: 5 (rem 56)
    // 5. Work: 25 (rem 31)
    // 6. Break: 5 (rem 26)
    // 7. Work: 25 (rem 1) - 4th work chunk
    // 8. Long Break: 1 (rem 0) - Remaining 1 minute used as a long break
    expect(chunks.length).toBe(8);
    expect(chunks[0].type).toBe('work'); expect(chunks[0].durationMinutes).toBe(25);
    expect(chunks[1].type).toBe('short-break'); expect(chunks[1].durationMinutes).toBe(5);
    expect(chunks[2].type).toBe('work'); expect(chunks[2].durationMinutes).toBe(25);
    expect(chunks[3].type).toBe('short-break'); expect(chunks[3].durationMinutes).toBe(5);
    expect(chunks[4].type).toBe('work'); expect(chunks[4].durationMinutes).toBe(25);
    expect(chunks[5].type).toBe('short-break'); expect(chunks[5].durationMinutes).toBe(5);
    expect(chunks[6].type).toBe('work'); expect(chunks[6].durationMinutes).toBe(25); // 4th work chunk
    expect(chunks[7].type).toBe('long-break'); expect(chunks[7].durationMinutes).toBe(1); // Remaining 1 minute used as long break
    expect(chunks.reduce((sum, chunk) => sum + chunk.durationMinutes, 0)).toBe(116);
  });
});
