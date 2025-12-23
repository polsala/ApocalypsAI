export type EchoCategory = "Minor Glitch" | "Chronal Ripple" | "Void Whisper" | "Temporal Anomaly" | "Unknown Echo";

export interface TemporalEcho {
  message: string;
  category: EchoCategory;
  stabilizationProtocol: string;
}

export interface EchoRule {
  keywords: string[];
  category: EchoCategory;
  protocol: string;
}
