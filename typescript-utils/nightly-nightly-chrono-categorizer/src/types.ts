export enum UrgencyCategory {
  IMMEDIATE_IMPLOSION = "Immediate Implosion",
  NEAR_TERM_NUISANCE = "Near-Term Nuisance",
  FUTURE_FOLLY = "Future Folly",
  COSMIC_CONTEMPLATION = "Cosmic Contemplation"
}

export interface Task {
  description: string;
  category: UrgencyCategory;
}

export interface CategorizationRule {
  category: UrgencyCategory;
  keywords: string[];
}
