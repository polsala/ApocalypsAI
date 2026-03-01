import { Task } from '../src/types';
import { getCosmicScore, prioritizeTasks } from '../src/taskOracle';

describe('taskOracle', () => {
  // # Mock rationale: Math.random is mocked to ensure deterministic cosmic energy scores.
  // This allows tests to predict the exact score without relying on randomness.
  const mockMathRandom = jest.spyOn(Math, 'random').mockReturnValue(0.5);

  // # Mock rationale: Date is mocked to ensure deterministic "moon phase" calculations.
  // This allows tests to predict the exact date-based score without relying on the current system date.
  const mockDate = new Date('2023-10-21T10:00:00Z'); // Day 21, not divisible by 3 or 7
  const mockDateNewMoon = new Date('2023-10-03T10:00:00Z'); // Day 3, divisible by 3
  const mockDateFullMoon = new Date('2023-10-07T10:00:00Z'); // Day 7, divisible by 7

  afterAll(() => {
    mockMathRandom.mockRestore();
  });

  describe('getCosmicScore', () => {
    it('should calculate base score from description length', () => {
      const task: Task = { id: '1', description: 'Short task' };
      const { score, rationale } = getCosmicScore(task, mockDate);
      // 'Short task' (10 chars) * 0.1 = 1
      // Random (0.5 * 20) = 10
      // Standard alignment = 2
      // Total = 1 + 10 + 2 = 13
      expect(score).toBeCloseTo(13);
      expect(rationale).toContain('Base score from description length (10): +1.0');
      expect(rationale).toContain('Random cosmic energy: +10.0');
      expect(rationale).toContain('Standard cosmic alignment: +2');
    });

    it('should apply keyword bonuses', () => {
      const task: Task = { id: '2', description: 'Urgent bug fix for feature X, a dream project' };
      const { score, rationale } = getCosmicScore(task, mockDate);
      // 'Urgent bug fix for feature X, a dream project' (45 chars) * 0.1 = 4.5
      // Urgent: +10
      // Bug: +8
      // Feature: +5
      // Dream: +15
      // Random (0.5 * 20) = 10
      // Standard alignment = 2
      // Total = 4.5 + 10 + 8 + 5 + 15 + 10 + 2 = 54.5
      expect(score).toBeCloseTo(54.5);
      expect(rationale).toContain("Contains 'urgent' keyword: +10");
      expect(rationale).toContain("Contains 'bug' keyword: +8");
      expect(rationale).toContain("Contains 'feature' keyword: +5");
      expect(rationale).toContain("Contains 'dream' keyword (whimsical bonus!): +15");
    });

    it('should apply new moon phase bonus', () => {
      const task: Task = { id: '3', description: 'Simple task' };
      const { score, rationale } = getCosmicScore(task, mockDateNewMoon);
      // 'Simple task' (11 chars) * 0.1 = 1.1
      // Random (0.5 * 20) = 10
      // New moon alignment = 5
      // Total = 1.1 + 10 + 5 = 16.1
      expect(score).toBeCloseTo(16.1);
      expect(rationale).toContain("Aligned with a 'new moon' phase: +5");
    });

    it('should apply full moon phase bonus', () => {
      const task: Task = { id: '4', description: 'Another task' };
      const { score, rationale } = getCosmicScore(task, mockDateFullMoon);
      // 'Another task' (12 chars) * 0.1 = 1.2
      // Random (0.5 * 20) = 10
      // Full moon alignment = 10
      // Total = 1.2 + 10 + 10 = 21.2
      expect(score).toBeCloseTo(21.2);
      expect(rationale).toContain("Aligned with a 'full moon' phase: +10");
    });
  });

  describe('prioritizeTasks', () => {
    it('should prioritize tasks based on cosmic score', () => {
      const tasks: Task[] = [
        { id: 'A', description: 'Low priority task' }, // Score: 1.7 + 10 + 2 = 13.7
        { id: 'B', description: 'Urgent bug fix' },    // Score: 1.4 + 10 + 8 + 10 + 2 = 31.4
        { id: 'C', description: 'Dream feature idea' },// Score: 2.0 + 15 + 5 + 10 + 2 = 34.0
      ];
      const prioritized = prioritizeTasks(tasks, mockDate);

      expect(prioritized.length).toBe(3);
      expect(prioritized[0].id).toBe('C');
      expect(prioritized[0].cosmicScore).toBeCloseTo(34.0);
      expect(prioritized[1].id).toBe('B');
      expect(prioritized[1].cosmicScore).toBeCloseTo(31.4);
      expect(prioritized[2].id).toBe('A');
      expect(prioritized[2].cosmicScore).toBeCloseTo(13.7);
    });

    it('should handle empty task list', () => {
      const tasks: Task[] = [];
      const prioritized = prioritizeTasks(tasks, mockDate);
      expect(prioritized).toEqual([]);
    });
  });
});
