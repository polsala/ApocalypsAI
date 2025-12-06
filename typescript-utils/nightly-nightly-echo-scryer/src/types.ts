export type KeywordCategory = 'Survival' | 'Danger' | 'Resource' | 'Hope' | 'Mystery' | 'Technology';

export interface ScryOptions {
  fragmentThreshold: number; // How much "noise" to tolerate or simulate (0-1, lower means more noise removed/ignored)
  contextLevel: 'low' | 'medium' | 'high'; // How detailed the context inference should be
}

export interface KeywordMatch {
  keyword: string;
  category: KeywordCategory;
  index: number;
}

export interface ScryReport {
  originalText: string;
  cleanedText: string;
  identifiedKeywords: KeywordMatch[];
  categoryCounts: Record<KeywordCategory, number>;
  dominantCategory: KeywordCategory | 'Neutral';
  apocalypticVibe: string;
  suggestedAction: string;
}
