export interface PackageJson {
  name: string;
  version: string;
  dependencies?: Record<string, string>;
  devDependencies?: Record<string, string>;
  peerDependencies?: Record<string, string>;
  optionalDependencies?: Record<string, string>;
}

export interface OutdatedPackage {
  current: string;
  wanted: string;
  latest: string;
  type: 'dependencies' | 'devDependencies';
  url: string;
}

export interface AuditAdvisory {
  id: number;
  title: string;
  severity: string;
  vulnerable_versions: string;
  patched_versions: string;
  url: string;
  module_name: string;
}

export interface AuditReport {
  advisories: Record<string, AuditAdvisory>;
  metadata: {
    vulnerabilities: {
      info: number;
      low: number;
      moderate: number;
      high: number;
      critical: number;
    };
  };
}
