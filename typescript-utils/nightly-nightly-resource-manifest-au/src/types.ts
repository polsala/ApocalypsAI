export type ResourceCategory = 'Food' | 'Water' | 'Tools' | 'Mystical' | 'Components' | 'Medical';

export interface ResourceItem {
  name: string;
  category: ResourceCategory;
  unit: string;
}

export type ResourceManifest = Record<string, number>;

export type AuditStatus = 'shortage' | 'surplus' | 'ok';

export interface AuditReportItem {
  resourceName: string;
  status: AuditStatus;
  needed: number;
  current: number;
  difference: number;
  message: string;
}

export type AuditReport = AuditReportItem[];
