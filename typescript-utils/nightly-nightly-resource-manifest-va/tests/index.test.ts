import { validateManifestFile } from '../src/index';
import * as fs from 'fs';

// Mock rationale: We need to simulate file system operations without actually touching the disk
// to ensure tests are deterministic and run offline.
jest.mock('fs', () => ({
  readFileSync: jest.fn(),
}));

const mockReadFileSync = fs.readFileSync as jest.Mock;
const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
const consoleLogSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});

describe('Manifest Validator', () => {
  beforeEach(() => {
    mockReadFileSync.mockClear();
    consoleSpy.mockClear();
    consoleLogSpy.mockClear();
    consoleWarnSpy.mockClear();
  });

  afterAll(() => {
    consoleSpy.mockRestore();
    consoleLogSpy.mockRestore();
    consoleWarnSpy.mockRestore();
  });

  it('should return true for a valid manifest file', () => {
    const validManifest = {
      manifestName: 'Alpha Base Supplies',
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: [
        {
          name: 'Water Bottle',
          quantity: 15,
          unit: 'bottles',
          perishable: true,
          expiryDate: '2025-01-01T00:00:00Z',
        },
        {
          name: 'Canned Beans',
          quantity: 30,
          unit: 'cans',
          perishable: false,
        },
      ],
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(validManifest));

    const result = validateManifestFile('path/to/valid-manifest.json');
    expect(result).toBe(true);
    expect(consoleLogSpy).toHaveBeenCalledWith(expect.stringContaining('✅ Manifest "Alpha Base Supplies" at "Sector 7G" is VALID.'));
    expect(consoleSpy).not.toHaveBeenCalled();
  });

  it('should return false and log error for a non-existent file', () => {
    mockReadFileSync.mockImplementationOnce(() => {
      const error = new Error('File not found');
      (error as any).code = 'ENOENT';
      throw error;
    });

    const result = validateManifestFile('path/to/non-existent.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('❌ File not found: path/to/non-existent.json'));
  });

  it('should return false and log error for invalid JSON', () => {
    mockReadFileSync.mockReturnValueOnce('this is not valid json');

    const result = validateManifestFile('path/to/invalid.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('❌ Failed to parse JSON file: path/to/invalid.json. Error: Unexpected token \'h\' at 2:1'));
  });

  it('should return false and log error for missing manifestName', () => {
    const invalidManifest = {
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: [],
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(invalidManifest));

    const result = validateManifestFile('path/to/missing-name.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Error: Manifest "manifestName" must be a non-empty string.'));
  });

  it('should return false and log error for invalid timestamp format', () => {
    const invalidManifest = {
      manifestName: 'Alpha Base Supplies',
      timestamp: 'not-a-date',
      location: 'Sector 7G',
      resources: [],
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(invalidManifest));

    const result = validateManifestFile('path/to/invalid-timestamp.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Error: Manifest "timestamp" must be a valid ISO 8601 date string.'));
  });

  it('should return false and log error for resources not being an array', () => {
    const invalidManifest = {
      manifestName: 'Alpha Base Supplies',
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: 'not-an-array',
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(invalidManifest));

    const result = validateManifestFile('path/to/invalid-resources-type.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Error: Manifest "resources" must be an array.'));
  });

  it('should return false and log error for an invalid resource within the array (missing name)', () => {
    const invalidManifest = {
      manifestName: 'Alpha Base Supplies',
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: [
        {
          quantity: 10,
          unit: 'units',
          perishable: false,
        },
      ],
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(invalidManifest));

    const result = validateManifestFile('path/to/invalid-resource-item.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Error: Resource "name" must be a non-empty string.'));
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Error: Invalid resource found at index 0 in manifest "Alpha Base Supplies".'));
  });

  it('should return false and log error for a perishable resource missing expiryDate', () => {
    const invalidManifest = {
      manifestName: 'Alpha Base Supplies',
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: [
        {
          name: 'Fresh Fruit',
          quantity: 5,
          unit: 'pieces',
          perishable: true,
          // expiryDate is missing
        },
      ],
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(invalidManifest));

    const result = validateManifestFile('path/to/perishable-no-expiry.json');
    expect(result).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Error: Resource "Fresh Fruit" is perishable but "expiryDate" is missing or not a string.'));
  });

  it('should warn about unexpected properties in manifest', () => {
    const manifestWithExtra = {
      manifestName: 'Alpha Base Supplies',
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: [],
      extraField: 'should not be here',
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(manifestWithExtra));

    const result = validateManifestFile('path/to/manifest-with-extra.json');
    expect(result).toBe(true); // Still valid if extra fields are just warnings
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Warning: Manifest "Alpha Base Supplies" has unexpected property "extraField".'));
  });

  it('should warn about unexpected properties in resource', () => {
    const manifestWithExtraResource = {
      manifestName: 'Alpha Base Supplies',
      timestamp: '2024-07-20T10:00:00Z',
      location: 'Sector 7G',
      resources: [
        {
          name: 'Water Bottle',
          quantity: 15,
          unit: 'bottles',
          perishable: true,
          expiryDate: '2025-01-01T00:00:00Z',
          extraResourceField: 'should not be here',
        },
      ],
    };
    mockReadFileSync.mockReturnValueOnce(JSON.stringify(manifestWithExtraResource));

    const result = validateManifestFile('path/to/resource-with-extra.json');
    expect(result).toBe(true); // Still valid if extra fields are just warnings
    expect(consoleWarnSpy).toHaveBeenCalledWith(expect.stringContaining('Validation Warning: Resource "Water Bottle" has unexpected property "extraResourceField".'));
  });
});
