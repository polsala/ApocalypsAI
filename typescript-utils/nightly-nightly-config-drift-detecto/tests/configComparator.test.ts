import { compareConfigs } from '../src/configComparator';
import { ConfigDriftReport } from '../src/types';

describe('compareConfigs', () => {
  it('should report no drift for identical configurations', () => {
    const configA = { a: 1, b: { c: 2 } };
    const configB = { a: 1, b: { c: 2 } };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(true);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([]);
  });

  it('should report added keys', () => {
    const configA = { a: 1 };
    const configB = { a: 1, b: 2 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual(['b']);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([]);
  });

  it('should report removed keys', () => {
    const configA = { a: 1, b: 2 };
    const configB = { a: 1 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual(['b']);
    expect(report.modified).toEqual([]);
  });

  it('should report modified values', () => {
    const configA = { a: 1, b: 2 };
    const configB = { a: 1, b: 3 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([{ path: 'b', oldValue: 2, newValue: 3 }]);
  });

  it('should handle nested objects - added', () => {
    const configA = { a: { b: 1 } };
    const configB = { a: { b: 1, c: 2 } };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual(['a.c']);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([]);
  });

  it('should handle nested objects - removed', () => {
    const configA = { a: { b: 1, c: 2 } };
    const configB = { a: { b: 1 } };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual(['a.c']);
    expect(report.modified).toEqual([]);
  });

  it('should handle nested objects - modified', () => {
    const configA = { a: { b: 1 } };
    const configB = { a: { b: 2 } };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([{ path: 'a.b', oldValue: 1, newValue: 2 }]);
  });

  it('should handle mixed types - object to primitive', () => {
    const configA = { a: { b: 1 } };
    const configB = { a: 1 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([{ path: 'a', oldValue: { b: 1 }, newValue: 1 }]);
  });

  it('should handle mixed types - primitive to object', () => {
    const configA = { a: 1 };
    const configB = { a: { b: 1 } };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual([]);
    expect(report.removed).toEqual([]);
    expect(report.modified).toEqual([{ path: 'a', oldValue: 1, newValue: { b: 1 } }]);
  });

  it('should handle arrays as modified if content differs', () => {
    const configA = { arr: [1, 2] };
    const configB = { arr: [1, 3] };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.modified).toEqual([{ path: 'arr', oldValue: [1, 2], newValue: [1, 3] }]);
  });

  it('should handle arrays as modified if order differs', () => {
    const configA = { arr: [1, 2] };
    const configB = { arr: [2, 1] };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.modified).toEqual([{ path: 'arr', oldValue: [1, 2], newValue: [2, 1] }]);
  });

  it('should handle null values', () => {
    const configA = { a: null };
    const configB = { a: 1 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.modified).toEqual([{ path: 'a', oldValue: null, newValue: 1 }]);
  });

  it('should handle undefined values (not typically in JSON, but for robustness)', () => {
    const configA = { a: undefined };
    const configB = { a: 1 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.modified).toEqual([{ path: 'a', oldValue: undefined, newValue: 1 }]);
  });

  it('should handle empty objects', () => {
    const configA = {};
    const configB = { a: 1 };
    const report = compareConfigs(configA, configB);
    expect(report.noDrift).toBe(false);
    expect(report.added).toEqual(['a']);
  });
});
