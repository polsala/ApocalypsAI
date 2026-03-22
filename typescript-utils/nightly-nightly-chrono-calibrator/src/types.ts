export type TemporalChunkType = 'work' | 'short-break' | 'long-break';

export interface TemporalChunk {
  name: string;
  durationMinutes: number;
  type: TemporalChunkType;
  description: string;
}
