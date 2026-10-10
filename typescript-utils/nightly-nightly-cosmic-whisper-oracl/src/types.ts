export type WhisperCategory = "Resource" | "Shelter" | "Social" | "Exploration" | "Self-Care" | "Wildcard";

export interface WhisperPrompt {
  id: string;
  category: WhisperCategory;
  prompt: string;
  actionVerb: string;
  riskLevel: "Low" | "Medium" | "High" | "Unknown";
}

export interface WhisperOutcome {
  category: WhisperCategory;
  prompt: string;
  action: string;
  risk: "Low" | "Medium" | "High" | "Unknown";
  timestamp: string;
}
