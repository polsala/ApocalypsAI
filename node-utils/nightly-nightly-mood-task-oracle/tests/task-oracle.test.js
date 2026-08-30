const { getTaskSuggestion, tasks } = require('../src/task-oracle');

describe('getTaskSuggestion', () => {
  // Mock rationale: Math.random is non-deterministic. Mocking it ensures tests
  // always pick the same "random" item from a list, making tests reliable.
  const mockMathRandom = (returnValue) => {
    const originalMathRandom = Math.random;
    Math.random = jest.fn(() => returnValue);
    return () => { Math.random = originalMathRandom; }; // Cleanup function
  };

  it('should return a task for a specified valid mood', () => {
    const cleanup = mockMathRandom(0.5); // Always pick middle element
    const suggestion = getTaskSuggestion('low-energy');
    expect(suggestion.mood).toBe('low-energy');
    expect(tasks['low-energy']).toContain(suggestion.task);
    cleanup();
  });

  it('should return a task for a different specified valid mood', () => {
    const cleanup = mockMathRandom(0.1); // Always pick first element
    const suggestion = getTaskSuggestion('high-chaos');
    expect(suggestion.mood).toBe('high-chaos');
    expect(tasks['high-chaos']).toContain(suggestion.task);
    cleanup();
  });

  it('should return a random mood and task if no mood is specified', () => {
    // Mock rationale: We need to control which random mood is picked, and then
    // which random task from that mood. By mocking Math.random multiple times,
    // we can simulate the sequence of random number generations.
    const availableMoods = Object.keys(tasks).filter(m => m !== 'default');
    const mockMoodIndex = 0; // Pick the first available mood
    const mockTaskIndex = 0; // Pick the first task from that mood

    const originalMathRandom = Math.random;
    Math.random = jest.fn()
      .mockReturnValueOnce(mockMoodIndex / availableMoods.length) // For mood selection
      .mockReturnValueOnce(mockTaskIndex / tasks[availableMoods[mockMoodIndex]].length); // For task selection

    const suggestion = getTaskSuggestion();
    expect(availableMoods).toContain(suggestion.mood);
    expect(tasks[suggestion.mood]).toContain(suggestion.task);
    expect(suggestion.mood).toBe(availableMoods[mockMoodIndex]);
    expect(suggestion.task).toBe(tasks[availableMoods[mockMoodIndex]][mockTaskIndex]);

    Math.random = originalMathRandom; // Restore Math.random
  });

  it('should return a random mood and task if an invalid mood is specified', () => {
    // Mock rationale: Same as above, ensure deterministic random selection when
    // an invalid mood forces a random fallback.
    const availableMoods = Object.keys(tasks).filter(m => m !== 'default');
    const mockMoodIndex = 1; // Pick the second available mood
    const mockTaskIndex = 1; // Pick the second task from that mood

    const originalMathRandom = Math.random;
    Math.random = jest.fn()
      .mockReturnValueOnce(mockMoodIndex / availableMoods.length) // For mood selection
      .mockReturnValueOnce(mockTaskIndex / tasks[availableMoods[mockMoodIndex]].length); // For task selection

    const suggestion = getTaskSuggestion('non-existent-mood');
    expect(availableMoods).toContain(suggestion.mood);
    expect(tasks[suggestion.mood]).toContain(suggestion.task);
    expect(suggestion.mood).toBe(availableMoods[mockMoodIndex]);
    expect(suggestion.task).toBe(tasks[availableMoods[mockMoodIndex]][mockTaskIndex]);

    Math.random = originalMathRandom; // Restore Math.random
  });

  it('should handle an empty tasks list gracefully (though unlikely in this setup)', () => {
    // Mock rationale: Temporarily modify the tasks object to simulate an edge case
    // where only a 'default' category exists or no categories are found.
    const originalTasks = { ...tasks };
    const emptyTasks = { 'default': ['Fallback task.'] };
    // Clear existing tasks by iterating and deleting, then assign only default
    Object.keys(tasks).forEach(key => delete tasks[key]);
    Object.assign(tasks, emptyTasks);

    const cleanup = mockMathRandom(0); // Should pick default as it's the only option
    const suggestion = getTaskSuggestion('any-mood');
    expect(suggestion.mood).toBe('default');
    expect(suggestion.task).toBe('Fallback task.');
    cleanup();

    // Restore original tasks to avoid side effects on other tests
    Object.keys(tasks).forEach(key => delete tasks[key]);
    Object.assign(tasks, originalTasks);
  });
});
