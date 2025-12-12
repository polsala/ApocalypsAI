const ANOMALIES = [
  { id: 'a1', type: 'Temporal Ripple', location: 'Sector Gamma-7', severity: 'Minor', status: 'Active', coordinates: { lat: 34.0522, lng: -118.2437 }, description: 'A faint shimmer in the chronal fabric near old LA.' },
  { id: 'a2', type: 'Echo Cascade', location: 'Neo-Kyoto Outskirts', severity: 'Moderate', status: 'Active', coordinates: { lat: 35.0116, lng: 135.7680 }, description: 'Repeated echoes of a past event, growing louder.' },
  { id: 'a3', type: 'Chronal Drift', location: 'Sahara Reclamation Zone', severity: 'Minor', status: 'Stabilized', coordinates: { lat: 23.4514, lng: 10.9410 }, description: 'Localized time dilation, successfully contained.' },
  { id: 'a4', type: 'Void Whisper', location: 'Deep Space Anomaly 001', severity: 'Severe', status: 'Active', coordinates: { lat: 0, lng: 0 }, description: 'Unintelligible whispers from the void, source unknown.' },
  { id: 'a5', type: 'Temporal Loop', location: 'Abandoned Research Facility', severity: 'Critical', status: 'Active', coordinates: { lat: 40.7128, lng: -74.0060 }, description: 'A small area reliving the same 30 seconds repeatedly.' }
];

export const getAnomalies = () => ANOMALIES;
export const stabilizeAnomaly = (id) => {
  const anomaly = ANOMALIES.find(a => a.id === id);
  if (anomaly) {
    anomaly.status = 'Stabilized';
    anomaly.severity = 'Minor'; // Reduced severity after stabilization
  }
  return anomaly;
};
