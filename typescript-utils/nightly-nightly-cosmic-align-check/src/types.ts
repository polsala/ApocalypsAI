export type AlignmentStatus = 'Favorable' | 'Unfavorable' | 'Neutral';

export interface CosmicFactor {
  name: string;
  status: AlignmentStatus;
  description: string;
}

export interface AlignmentResult {
  overallStatus: AlignmentStatus;
  factors: CosmicFactor[];
  message: string;
}
