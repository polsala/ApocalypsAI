export type Confidence = 'High' | 'Medium' | 'Low' | 'None';

export interface ScrapedDate {
  original: string;
  parsed: Date | null;
  confidence: Confidence;
  error?: string;
}
