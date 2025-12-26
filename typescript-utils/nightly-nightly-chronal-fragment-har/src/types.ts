export interface DataFragment {
  id: string;
  content: string;
  timestamp: string; // ISO 8601 string
  temporalDistortion: number; // 0-100, lower is better
  origin: string;
}

export type FragmentCategory = 'Stable' | 'Unstable' | 'Highly Distorted';

export interface HarmonizationReport {
  totalFragments: number;
  stableFragments: DataFragment[];
  unstableFragments: DataFragment[];
  highlyDistortedFragments: DataFragment[];
  recommendations: string[];
}
