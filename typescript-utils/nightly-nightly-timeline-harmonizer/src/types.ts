export interface TemporalEcho {
  timestamp: number; // Unix timestamp in milliseconds
  value: number;
  source: string;
}

export type HarmonizationStrategy = 'average' | 'median' | 'first' | 'last';

export interface AlignedEchoGroup {
  timestamp: number;
  echoes: TemporalEcho[];
}

export interface Discrepancy {
  timestamp: number;
  alignedGroup: AlignedEchoGroup;
  deviation: number; // e.g., max percentage deviation from average
}
