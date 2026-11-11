import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

// Helper function to run the CLI command
const runCli = (interfaceFile: string, dataFile: string): { stdout: string; stderr: string } => {
  const cliPath = path.join(__dirname, '../src/main.ts');
  const command = `npx ts-node ${cliPath} --interface-file ${interfaceFile} --data-file ${dataFile}`;
  try {
    const stdout = execSync(command, { encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'] });
    return { stdout, stderr: '' };
  } catch (error: any) {
    return { stdout: error.stdout || '', stderr: error.stderr || error.message };
  }
};

describe('Nightly TypeScript Type Checker CLI', () => {
  const testDir = path.join(__dirname, 'fixtures');

  beforeAll(() => {
    // Create test directory and files
    if (!fs.existsSync(testDir)) {
      fs.mkdirSync(testDir);
    }
  });

  afterAll(() => {
    // Clean up test files and directory
    fs.readdirSync(testDir).forEach(file => {
      fs.unlinkSync(path.join(testDir, file));
    });
    fs.rmdirSync(testDir);
  });

  it('should validate valid JSON against a simple interface', () => {
    const interfaceContent = `
export interface User {
  id: number;
  name: string;
  isActive?: boolean;
}
`;
    const dataContent = `
{
  "id": 1,
  "name": "Alice",
  "isActive": true
}
`;
    const interfaceFile = path.join(testDir, 'User.ts');
    const dataFile = path.join(testDir, 'userData.json');
    fs.writeFileSync(interfaceFile, interfaceContent);
    fs.writeFileSync(dataFile, dataContent);

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toBe('');
    expect(result.stdout).toContain('JSON data is valid');
  });

  it('should report missing required properties', () => {
    const interfaceContent = `
export interface Product {
  sku: string;
  price: number;
}
`;
    const dataContent = `
{
  "sku": "ABC-123"
}
`;
    const interfaceFile = path.join(testDir, 'Product.ts');
    const dataFile = path.join(testDir, 'productData.json');
    fs.writeFileSync(interfaceFile, interfaceContent);
    fs.writeFileSync(dataFile, dataContent);

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toContain('JSON validation failed:');
    expect(result.stderr).toContain("Missing required property: 'price'");
  });

  it('should report incorrect property types', () => {
    const interfaceContent = `
export interface Settings {
  timeout: number;
  enabled: boolean;
}
`;
    const dataContent = `
{
  "timeout": "3000",
  "enabled": "true"
}
`;
    const interfaceFile = path.join(testDir, 'Settings.ts');
    const dataFile = path.join(testDir, 'settingsData.json');
    fs.writeFileSync(interfaceFile, interfaceContent);
    fs.writeFileSync(dataFile, dataContent);

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toContain('JSON validation failed:');
    expect(result.stderr).toContain("Property 'timeout' expected type 'number', but got 'string'");
    expect(result.stderr).toContain("Property 'enabled' expected type 'boolean', but got 'string'");
  });

  it('should report unexpected properties', () => {
    const interfaceContent = `
export interface Item {
  id: number;
}
`;
    const dataContent = `
{
  "id": 456,
  "extraField": "someValue"
}
`;
    const interfaceFile = path.join(testDir, 'Item.ts');
    const dataFile = path.join(testDir, 'itemData.json');
    fs.writeFileSync(interfaceFile, interfaceContent);
    fs.writeFileSync(dataFile, dataContent);

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toContain('JSON validation failed:');
    expect(result.stderr).toContain("Unexpected property found: 'extraField'");
  });

  it('should handle optional properties correctly', () => {
    const interfaceContent = `
export interface OptionalUser {
  id: number;
  email?: string;
}
`;
    const dataContent = `
{
  "id": 789
}
`;
    const interfaceFile = path.join(testDir, 'OptionalUser.ts');
    const dataFile = path.join(testDir, 'optionalUserData.json');
    fs.writeFileSync(interfaceFile, interfaceContent);
    fs.writeFileSync(dataFile, dataContent);

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toBe('');
    expect(result.stdout).toContain('JSON data is valid');
  });

  it('should report error if interface file does not exist', () => {
    const interfaceFile = path.join(testDir, 'NonExistentInterface.ts');
    const dataFile = path.join(testDir, 'dummyData.json');
    fs.writeFileSync(dataFile, '{}');

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toContain('Error: Interface file not found');
  });

  it('should report error if data file does not exist', () => {
    const interfaceFile = path.join(testDir, 'DummyInterface.ts');
    const dataFile = path.join(testDir, 'NonExistentData.json');
    fs.writeFileSync(interfaceFile, 'export interface Dummy {}');

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toContain('Error: Data file not found');
  });

  it('should report error for invalid JSON data', () => {
    const interfaceContent = `
export interface Simple {
  value: string;
}
`;
    const dataContent = `
{
  "value": "test",
`; // Malformed JSON
    const interfaceFile = path.join(testDir, 'Simple.ts');
    const dataFile = path.join(testDir, 'malformedData.json');
    fs.writeFileSync(interfaceFile, interfaceContent);
    fs.writeFileSync(dataFile, dataContent);

    const result = runCli(interfaceFile, dataFile);
    expect(result.stderr).toContain('An unexpected error occurred:');
    expect(result.stderr).toContain('Unexpected token'); // Expecting JSON parsing error
  });

  // Mock rationale: The TypeScript compiler API is complex and its behavior can be hard to mock directly. 
  // For unit tests, we are testing the CLI's integration with the TS compiler API and file system operations.
  // We are not trying to mock the TS compiler itself, but rather ensure our CLI correctly invokes it and handles its output.
  // The tests focus on the CLI's logic for file reading, JSON parsing, and interpreting the results from the validation function.
});
