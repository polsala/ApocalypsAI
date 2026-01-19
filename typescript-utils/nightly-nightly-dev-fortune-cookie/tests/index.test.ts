import { getRandomFortune, runCli } from '../src/index';
import { fortunes } from '../src/fortunes';
import { FortuneCategory } from '../src/types';

describe('nightly-dev-fortune-cookie', () => {
  let consoleSpy: jest.SpyInstance;
  let errorSpy: jest.SpyInstance;
  let exitSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    errorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock error too
    exitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); });
  });

  afterEach(() => {
    consoleSpy.mockRestore();
    errorSpy.mockRestore();
    exitSpy.mockRestore();
    jest.restoreAllMocks();
  });

  it('should return a random fortune when no category is specified', () => {
    // Mock rationale: Ensure getRandomFortune is deterministic for testing purposes.
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Always pick the middle element

    const fortune = getRandomFortune();
    expect(fortunes).toContain(fortune);
    expect(fortune).toBe(fortunes[Math.floor(0.5 * fortunes.length)]);
  });

  it('should return a random fortune from the specified category', () => {
    const category: FortuneCategory = 'debugging';
    const debuggingFortunes = fortunes.filter(f => f.category === category);

    // Mock rationale: Ensure getRandomFortune is deterministic for testing purposes.
    jest.spyOn(Math, 'random').mockReturnValue(0.1); // Pick an early element

    const fortune = getRandomFortune(category);
    expect(debuggingFortunes).toContain(fortune);
    expect(fortune).toBe(debuggingFortunes[Math.floor(0.1 * debuggingFortunes.length)]);
  });

  it('should print a fortune to console when runCli is called without arguments', () => {
    // Mock rationale: Ensure getRandomFortune is deterministic for testing purposes.
    jest.spyOn(Math, 'random').mockReturnValue(0); // Always pick the first fortune

    runCli([]);
    expect(consoleSpy).toHaveBeenCalledTimes(3);
    expect(consoleSpy.mock.calls[1][0]).toContain(fortunes[0].message);
    expect(consoleSpy.mock.calls[2][0]).toContain(`Category: ${fortunes[0].category.charAt(0).toUpperCase() + fortunes[0].category.slice(1)}`);
  });

  it('should print a fortune from a specific category when runCli is called with --category', () => {
    const category: FortuneCategory = 'deployment';
    const deploymentFortunes = fortunes.filter(f => f.category === category);
    
    // Mock rationale: Ensure getRandomFortune is deterministic for testing purposes.
    jest.spyOn(Math, 'random').mockReturnValue(0); // Always pick the first fortune in the filtered list

    runCli(['--category', category]);
    expect(consoleSpy).toHaveBeenCalledTimes(3);
    expect(consoleSpy.mock.calls[1][0]).toContain(deploymentFortunes[0].message);
    expect(consoleSpy.mock.calls[2][0]).toContain(`Category: ${category.charAt(0).toUpperCase() + category.slice(1)}`);
  });

  it('should exit with an error for an invalid category', () => {
    const invalidCategory = 'invalid-cat' as FortuneCategory;
    
    // Mock rationale: process.exit is mocked to throw an error to prevent actual process termination during tests.
    // This allows Jest to catch the "exit" and assert on it.
    expect(() => runCli(['--category', invalidCategory])).toThrow('process.exit: 1');
    expect(errorSpy).toHaveBeenCalledWith(expect.stringContaining(`Error: Invalid category '${invalidCategory}'.`));
  });

  it('should handle empty category gracefully (though data should prevent this)', () => {
    // Temporarily empty fortunes to test edge case
    const originalFortunes = [...fortunes];
    fortunes.length = 0; // Clear the array

    // Mock rationale: Ensure getRandomFortune is deterministic for testing purposes.
    jest.spyOn(Math, 'random').mockReturnValue(0);

    const fortune = getRandomFortune('wisdom');
    expect(fortune.message).toBe("No fortunes found for this category. Perhaps you should write one!");
    expect(fortune.category).toBe("general");

    // Restore fortunes
    fortunes.push(...originalFortunes);
  });
});
