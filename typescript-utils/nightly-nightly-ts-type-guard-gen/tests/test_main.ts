import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: Using execSync to simulate the CLI execution and capture its output.
// This avoids complex mocking of file system operations and TypeScript compiler API.
// The tests are deterministic as they rely on fixed input files and expected outputs.

const CLI_PATH = path.join(__dirname, '../src/main.ts');

describe('ts-type-guard-gen', () => {
  const testInterfacesContent = `
export interface UserProfile {
  id: number;
  username: string;
  email?: string;
  isActive: boolean;
}

export interface Product {
  sku: string;
  name: string;
  price: number;
  inStock: boolean;
}

export interface SimpleData {
  value: string | number;
  optionalFlag?: boolean;
}
`;

  const expectedUserProfileGuard = `
export function isUserProfile(obj: any): obj is UserProfile {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.id === 'number' &&
    typeof obj.username === 'string' &&
    (typeof obj.email === 'undefined' || typeof obj.email === 'string') &&
    typeof obj.isActive === 'boolean'
  );
}
`;

  const expectedProductGuard = `
export function isProduct(obj: any): obj is Product {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.sku === 'string' &&
    typeof obj.name === 'string' &&
    typeof obj.price === 'number' &&
    typeof obj.inStock === 'boolean'
  );
}
`;

  const expectedSimpleDataGuard = `
export function isSimpleData(obj: any): obj is SimpleData {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    (typeof obj.value === 'string' || typeof obj.value === 'number') &&
    (typeof obj.optionalFlag === 'undefined' || typeof obj.optionalFlag === 'boolean')
  );
}
`;

  it('should generate type guards to stdout when no output file is specified', () => {
    const tempInterfacesFile = path.join(__dirname, 'temp_interfaces.ts');
    fs.writeFileSync(tempInterfacesFile, testInterfacesContent);

    try {
      const stdout = execSync(`node ${CLI_PATH} --input ${tempInterfacesFile}`).toString();
      expect(stdout).toContain(expectedUserProfileGuard);
      expect(stdout).toContain(expectedProductGuard);
      expect(stdout).toContain(expectedSimpleDataGuard);
    } finally {
      fs.unlinkSync(tempInterfacesFile);
    }
  });

  it('should generate type guards to a specified output file', () => {
    const tempInterfacesFile = path.join(__dirname, 'temp_interfaces.ts');
    const tempOutputFile = path.join(__dirname, 'generated_guards.ts');
    fs.writeFileSync(tempInterfacesFile, testInterfacesContent);

    try {
      execSync(`node ${CLI_PATH} --input ${tempInterfacesFile} --output ${tempOutputFile}`);
      const stdout = fs.readFileSync(tempOutputFile).toString();
      expect(stdout).toContain(expectedUserProfileGuard);
      expect(stdout).toContain(expectedProductGuard);
      expect(stdout).toContain(expectedSimpleDataGuard);
    } finally {
      fs.unlinkSync(tempInterfacesFile);
      if (fs.existsSync(tempOutputFile)) {
        fs.unlinkSync(tempOutputFile);
      }
    }
  });

  it('should handle interfaces with optional properties', () => {
    const optionalInterfaceContent = `
export interface OptionalUser {
  name: string;
  age?: number;
}
`;
    const expectedOptionalUserGuard = `
export function isOptionalUser(obj: any): obj is OptionalUser {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    typeof obj.name === 'string' &&
    (typeof obj.age === 'undefined' || typeof obj.age === 'number')
  );
}
`;
    const tempInterfacesFile = path.join(__dirname, 'temp_optional_interfaces.ts');
    fs.writeFileSync(tempInterfacesFile, optionalInterfaceContent);

    try {
      const stdout = execSync(`node ${CLI_PATH} --input ${tempInterfacesFile}`).toString();
      expect(stdout).toContain(expectedOptionalUserGuard);
    } finally {
      fs.unlinkSync(tempInterfacesFile);
    }
  });

  it('should handle interfaces with union types', () => {
    const unionInterfaceContent = `
export interface Status {
  code: number | string;
}
`;
    const expectedStatusGuard = `
export function isStatus(obj: any): obj is Status {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    (typeof obj.code === 'number' || typeof obj.code === 'string')
  );
}
`;
    const tempInterfacesFile = path.join(__dirname, 'temp_union_interfaces.ts');
    fs.writeFileSync(tempInterfacesFile, unionInterfaceContent);

    try {
      const stdout = execSync(`node ${CLI_PATH} --input ${tempInterfacesFile}`).toString();
      expect(stdout).toContain(expectedStatusGuard);
    } finally {
      fs.unlinkSync(tempInterfacesFile);
    }
  });

  it('should exit with an error if input file is not provided', () => {
    try {
      execSync(`node ${CLI_PATH}`);
    } catch (error: any) {
      expect(error.stderr.toString()).toContain('Error: --input file path is required.');
    }
  });
});
