import { Config, ConfigDriftReport } from './types';

function getPath(path: string[], key: string): string {
  return [...path, key].join('.');
}

function deepCompare(
  objA: Config,
  objB: Config,
  currentPath: string[],
  report: ConfigDriftReport
): void {
  // Check for keys in A but not in B (removed) or modified
  for (const key in objA) {
    const path = getPath(currentPath, key);
    if (!(key in objB)) {
      report.removed.push(path);
    } else if (typeof objA[key] === 'object' && objA[key] !== null &&
               typeof objB[key] === 'object' && objB[key] !== null &&
               !Array.isArray(objA[key]) && !Array.isArray(objB[key])) {
      // Both are objects, recurse
      deepCompare(objA[key], objB[key], [...currentPath, key], report);
    } else if (JSON.stringify(objA[key]) !== JSON.stringify(objB[key])) {
      // Values are different (or one is object/array and other is not)
      report.modified.push({
        path: path,
        oldValue: objA[key],
        newValue: objB[key],
      });
    }
  }

  // Check for keys in B but not in A (added)
  for (const key in objB) {
    const path = getPath(currentPath, key);
    if (!(key in objA)) {
      report.added.push(path);
    }
  }
}

export function compareConfigs(configA: Config, configB: Config): ConfigDriftReport {
  const report: ConfigDriftReport = {
    added: [],
    removed: [],
    modified: [],
    noDrift: false,
  };

  deepCompare(configA, configB, [], report);

  report.noDrift = report.added.length === 0 && report.removed.length === 0 && report.modified.length === 0;

  return report;
}
