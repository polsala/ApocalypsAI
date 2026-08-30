export type ConundrumCategory =
  | "Temporal Ripple"
  | "Reality Glitch"
  | "Existential Echo"
  | "Cosmic Joke"
  | "Unknown Anomaly";

export interface ConundrumClassification {
  category: ConundrumCategory;
  action: string;
  confidence: number; // Whimsical confidence score between 0 and 1
}
