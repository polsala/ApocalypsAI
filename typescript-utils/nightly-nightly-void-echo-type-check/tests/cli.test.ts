import { exec } from 'child_process'; // # Mock rationale: Use child_process to simulate CLI execution, but capture stdout/stderr to ensure determinism and offline execution. This tests the full CLI flow without external network or file system interactions beyond the script itself.
import path from 'path';

const cliPath = path.resolve(__dirname, '../dist/cli.js');

describe('CLI Tool', () => {
  // Helper to run the CLI command
  const runCli = (args: string[]): Promise<{ stdout: string; stderr: string; code: number }> => {
    return new Promise((resolve) => {
      exec(`node ${cliPath} ${args.join(' ')}`, (error, stdout, stderr) => {
        resolve({
          stdout: stdout.trim(),
          stderr: stderr.trim(),
          code: error ? error.code || 1 : 0,
        });
      });
    });
  };

  it('should display usage if no arguments are provided', async () => {
    const { stdout, stderr, code } = await runCli([]);
    expect(stdout).toContain('Usage: nightly-void-echo-type-checker validate <schema-name> <message-type> <message-content>');
    expect(code).toBe(1);
  });

  it('should validate a string message successfully', async () => {
    const { stdout, stderr, code } = await runCli([
      'validate',
      'simple-status',
      'string',
      'VOID ECHO: INFO: All systems nominal.'
    ]);
    expect(stdout).toContain('✅ Message is valid against schema "simple-status".');
    expect(stderr).toBe('');
    expect(code).toBe(0);
  });

  it('should fail validation for a non-matching string message', async () => {
    const { stdout, stderr, code } = await runCli([
      'validate',
      'simple-status',
      'string',
      'Just a random message.'
    ]);
    expect(stdout).toBe('');
    expect(stderr).toContain('❌ Message is INVALID against schema "simple-status".');
    expect(stderr).toContain('Message does not match pattern "^VOID ECHO: (INFO|WARNING|ERROR): .+".');
    expect(code).toBe(1);
  });

  it('should validate a JSON message successfully', async () => {
    const jsonMessage = JSON.stringify({
      timestamp: 1678886400000,
      level: 'INFO',
      message: 'Service started.',
      source: 'backend'
    });
    const { stdout, stderr, code } = await runCli([
      'validate',
      'structured-log',
      'json',
      jsonMessage
    ]);
    expect(stdout).toContain('✅ Message is valid against schema "structured-log".');
    expect(stderr).toBe('');
    expect(code).toBe(0);
  });

  it('should fail validation for an invalid JSON message (missing required field)', async () => {
    const jsonMessage = JSON.stringify({
      timestamp: 1678886400000,
      level: 'INFO'
      // message is missing
    });
    const { stdout, stderr, code } = await runCli([
      'validate',
      'structured-log',
      'json',
      jsonMessage
    ]);
    expect(stdout).toBe('');
    expect(stderr).toContain('❌ Message is INVALID against schema "structured-log".');
    expect(stderr).toContain('Missing required property: "message".');
    expect(code).toBe(1);
  });

  it('should fail validation for an invalid JSON message (wrong enum value)', async () => {
    const jsonMessage = JSON.stringify({
      timestamp: 1678886400000,
      level: 'CRITICAL', // Invalid enum
      message: 'Critical error!'
    });
    const { stdout, stderr, code } = await runCli([
      'validate',
      'structured-log',
      'json',
      jsonMessage
    ]);
    expect(stdout).toBe('');
    expect(stderr).toContain('❌ Message is INVALID against schema "structured-log".');
    expect(stderr).toContain('Property "level" value "CRITICAL" is not one of the allowed enum values: INFO, WARN, ERROR.');
    expect(code).toBe(1);
  });

  it('should handle invalid JSON input gracefully', async () => {
    const { stdout, stderr, code } = await runCli([
      'validate',
      'structured-log',
      'json',
      '{ "timestamp": 123, "level": "INFO", "message": "test", ' // Malformed JSON
    ]);
    expect(stdout).toBe('');
    expect(stderr).toContain('Error: Invalid JSON message content provided.');
    expect(code).toBe(1);
  });

  it('should report error if schema is not found', async () => {
    const { stdout, stderr, code } = await runCli([
      'validate',
      'non-existent-schema',
      'string',
      'Some message'
    ]);
    expect(stdout).toBe('');
    expect(stderr).toContain('❌ Message is INVALID against schema "non-existent-schema".');
    expect(stderr).toContain('Schema "non-existent-schema" not found.');
    expect(code).toBe(1);
  });

  it('should report error for unknown message type', async () => {
    const { stdout, stderr, code } = await runCli([
      'validate',
      'simple-status',
      'unknown-type',
      'Some message'
    ]);
    expect(stdout).toBe('');
    expect(stderr).toContain('Error: Invalid message type. Must be "string" or "json".');
    expect(code).toBe(1);
  });
});
