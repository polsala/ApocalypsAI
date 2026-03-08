export enum RippleType {
  TemporalShift = "TemporalShift",
  ObjectDuplication = "ObjectDuplication",
  MinorGlitch = "MinorGlitch",
  AuditoryDistortion = "AuditoryDistortion",
  VisualFlicker = "VisualFlicker"
}

export interface RealityRipple {
  id: string;
  type: RippleType;
  description: string;
  timestamp: string; // ISO 8601 string
}
