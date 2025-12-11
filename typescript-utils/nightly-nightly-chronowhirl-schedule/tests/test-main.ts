import { getOptimalSlots } from '../src/main';
import { format, addHours } from 'date-fns';

jest.useFakeTimers().setSystemTime(new Date('2024-04-05T12:00:00Z'));

describe('ChronoWhirl Scheduler', () => {
  test('assigns slots with correct emojis', () => {
    const schedule = getOptimalSlots(['Task A', 'Task B'], 'UTC');
    expect(schedule[0].emoji).toBe('🌅');
    expect(schedule[1].emoji).toBe('💻');
  });

  test('handles timezone formatting', () => {
    const schedule = getOptimalSlots(['Task'], 'Europe/London');
    expect(schedule[0].slot).toContain('🌅');
  });

  test('shuffles tasks deterministically', () => {
    // Mocked random to ensure deterministic shuffling
    jest.spyOn(Math, 'random').mockReturnValue(0.5);
    const schedule1 = getOptimalSlots(['A', 'B', 'C'], 'UTC');
    const schedule2 = getOptimalSlots(['A', 'B', 'C'], 'UTC');
    expect(schedule1).toEqual(schedule2);
  });
});
