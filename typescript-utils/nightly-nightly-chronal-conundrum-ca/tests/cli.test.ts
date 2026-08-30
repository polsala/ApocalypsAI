import { exec } from 'child_process';
import path from 'path';

// Mock rationale: We are testing the CLI output, not the classification logic itself.
// We want to ensure the CLI correctly calls the classifier and formats the output.
// Mocking console.log allows us to capture the output without actually printing to the console
// during tests, making them deterministic and isolated.
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});

describe('nccc CLI', () => {
  const cliPath = path.resolve(__dirname, '../dist/index.js'); // Path to compiled JS

  beforeEach(() => {
    mockConsoleLog.mockClear();
  });

  afterAll(() => {
    mockConsoleLog.mockRestore();
  });

  it('should display an error for missing arguments', (done) => {
    exec(`node ${cliPath}`, (error, stdout, stderr) => {
      expect(stderr).toContain('error: missing required argument');
      expect(error).not.toBeNull(); // An error is expected for missing args
      done();
    });
  });

  it('should classify a temporal ripple and print formatted output', (done) => {
    const conundrum = 'The moon is made of cheese, but only on Tuesdays.';
    exec(`node ${cliPath} "${conundrum}"`, (error, stdout, stderr) => {
      expect(error).toBeNull(); // No error expected from the command itself
      expect(mockConsoleLog).toHaveBeenCalledTimes(6); // Header, Conundrum, Category, Action, Confidence, Footer
      expect(mockConsoleLog.mock.calls[1][0]).toContain(`Conundrum: ${conundrum}`);
      expect(mockConsoleLog.mock.calls[2][0]).toContain('Category: Reality Glitch'); // "cheese" -> Reality Glitch
      expect(mockConsoleLog.mock.calls[3][0]).toContain('Document the anomaly');
      expect(mockConsoleLog.mock.calls[4][0]).toContain('Confidence:');
      done();
    });
  });

  it('should classify a cosmic joke and print formatted output', (done) => {
    const conundrum = 'My socks are singing opera in a language only I understand.';
    exec(`node ${cliPath} "${conundrum}"`, (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(mockConsoleLog.mock.calls[1][0]).toContain(`Conundrum: ${conundrum}`);
      expect(mockConsoleLog.mock.calls[2][0]).toContain('Category: Cosmic Joke'); // "singing" -> Cosmic Joke
      expect(mockConsoleLog.mock.calls[3][0]).toContain('Appreciate the absurdity');
      expect(mockConsoleLog.mock.calls[4][0]).toContain('Confidence:');
      done();
    });
  });

  it('should handle descriptions with special characters', (done) => {
    const conundrum = 'Is this reality, or just a very elaborate dream?!';
    exec(`node ${cliPath} "${conundrum}"`, (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(mockConsoleLog.mock.calls[1][0]).toContain(`Conundrum: ${conundrum}`);
      expect(mockConsoleLog.mock.calls[2][0]).toContain('Category: Existential Echo'); // "reality", "dream" -> Existential Echo
      expect(mockConsoleLog.mock.calls[3][0]).toContain('pun');
      done();
    });
  });

  it('should correctly classify an unknown anomaly', (done) => {
    const conundrum = 'The sky is plaid today, and my dog is wearing a tiny hat.';
    exec(`node ${cliPath} "${conundrum}"`, (error, stdout, stderr) => {
      expect(error).toBeNull();
      expect(mockConsoleLog.mock.calls[1][0]).toContain(`Conundrum: ${conundrum}`);
      expect(mockConsoleLog.mock.calls[2][0]).toContain('Category: Unknown Anomaly');
      expect(mockConsoleLog.mock.calls[3][0]).toContain('Proceed with extreme caution');
      done();
    });
  });
});
