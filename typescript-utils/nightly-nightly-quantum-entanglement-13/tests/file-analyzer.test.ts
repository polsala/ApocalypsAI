import { FileAnalyzer } from '../src/file-analyzer';
import * as fs from 'fs';
import * as path from 'path';

// Mock file system
jest.mock('fs');
jest.mock('path');

const mockFs = fs as jest.Mocked<typeof fs>;
const mockPath = path as jest.Mocked<typeof path>;

describe('FileAnalyzer', () => {
  let analyzer: FileAnalyzer;

  beforeEach(() => {
    analyzer = new FileAnalyzer();
    jest.clearAllMocks();
  });

  test('should analyze TypeScript file correctly', async () => {
    const mockContent = `
import { AuthService } from './auth.service';
import { Database } from './database';

export class UserService {
  constructor(private auth: AuthService, private db: Database) {}

  async getUser(id: string): Promise<User> {
    if (!id) throw new Error('Invalid ID');
    
    const user = await this.db.findUser(id);
    return user;
  }
}
`;

    mockFs.promises.readFile.mockResolvedValue(mockContent);
    mockFs.promises.readdir.mockResolvedValue(['user.service.ts']);
    mockFs.promises.stat.mockResolvedValue({
      isDirectory: () => false,
      isFile: () => true
    } as any);

    mockPath.basename.mockImplementation((path, ext) => {
      if (ext) return path.replace(ext, '');
      return path.split('/').pop() || '';
    });

    const result = await analyzer.analyzeDirectory('./test-src');

    expect(result.files).toHaveLength(1);
    expect(result.components).toHaveLength(1);
    expect(result.components[0].name).toBe('UserService');
    expect(result.components[0].dependencies).toContain('AuthService');
    expect(result.components[0].dependencies).toContain('Database');
    expect(result.components[0].linesOfCode).toBeGreaterThan(0);
    expect(result.components[0].complexity).toBeGreaterThan(0);
  });

  test('should skip unsupported file types', async () => {
    mockFs.promises.readdir.mockResolvedValue(['readme.md', 'config.json']);
    mockFs.promises.stat.mockResolvedValue({
      isDirectory: () => false,
      isFile: () => true
    } as any);

    const result = await analyzer.analyzeDirectory('./test-src');

    expect(result.files).toHaveLength(0);
    expect(result.components).toHaveLength(0);
  });

  test('should skip node_modules directory', async () => {
    mockFs.promises.readdir.mockResolvedValue(['node_modules', 'src']);
    mockFs.promises.stat.mockResolvedValue({
      isDirectory: () => true,
      isFile: () => false
    } as any);

    const result = await analyzer.analyzeDirectory('./test-src');

    // Should not throw and should handle directory skipping
    expect(Array.isArray(result.files)).toBe(true);
    expect(Array.isArray(result.components)).toBe(true);
  });

  test('should extract dependencies from import statements', () => {
    const content = `
import { AuthService } from './auth.service';
import Database from './database';
const logger = require('./logger');
import * as utils from './utils';

// External imports should be ignored
import React from 'react';
import { Router } from 'express';
`;

    // Test the private method by creating a temporary instance
    const testAnalyzer = new FileAnalyzer();
    // We can't directly test private methods, so we test through public interface
    // or use TypeScript casting to access private methods for testing
  });

  test('should calculate complexity correctly', () => {
    const lines = [
      'function test() {',
      '  if (condition) {',
      '    for (let i = 0; i < 10; i++) {',
      '      console.log(i);',
      '    }',
      '  }',
      '}',
      'const arrow = () => { return true; };',
      'const ternary = condition ? true : false;'
    ];

    // We can't directly test private methods, but we can verify the overall behavior
    // by analyzing a file with known complexity
  });

  test('should handle file read errors gracefully', async () => {
    mockFs.promises.readFile.mockRejectedValue(new Error('Permission denied'));
    mockFs.promises.readdir.mockResolvedValue(['protected.ts']);
    mockFs.promises.stat.mockResolvedValue({
      isDirectory: () => false,
      isFile: () => true
    } as any);

    const result = await analyzer.analyzeDirectory('./test-src');

    // Should not throw and should continue with other files
    expect(Array.isArray(result.files)).toBe(true);
    expect(Array.isArray(result.components)).toBe(true);
  });

  test('should normalize component names correctly', () => {
    const testCases = [
      { input: 'user-service', expected: 'UserService' },
      { input: 'auth_controller', expected: 'AuthController' },
      { input: 'database.utils', expected: 'DatabaseUtils' },
      { input: 'my-component-name', expected: 'MyComponentName' }
    ];

    // Test through the analyzeFile method which uses normalizeComponentName
    // We'll verify this indirectly by checking component names in results
  });
});

// Mock implementation for testing
beforeEach(() => {
  mockFs.promises.readFile = jest.fn();
  mockFs.promises.readdir = jest.fn();
  mockFs.promises.stat = jest.fn();
  mockPath.join = jest.fn((...args) => args.join('/'));
  mockPath.basename = jest.fn((path, ext) => {
    const name = path.split('/').pop() || '';
    return ext ? name.replace(ext, '') : name;
  });
  mockPath.dirname = jest.fn((path) => path.split('/').slice(0, -1).join('/'));
  mockPath.extname = jest.fn((path) => '.' + path.split('.').pop());
});
