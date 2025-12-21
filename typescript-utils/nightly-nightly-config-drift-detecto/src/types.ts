export interface ConfigDriftReport {
  added: string[];
  removed: string[];
  modified: { path: string; oldValue: any; newValue: any }[];
  noDrift: boolean;
}

export type Config = Record<string, any>;
