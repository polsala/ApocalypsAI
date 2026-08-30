// Mock rationale: Provides deterministic data for the React application
// and tests without requiring a backend or external API calls.
const mockAnomalies = [
  {
    id: 'anom-001',
    name: 'Whispering Sands Drift',
    location: { x: 150, y: 200 }, // Coordinates relative to a 800x600 map
    severity: 'high',
    resonanceFrequency: '4.7 Hz (Temporal)',
    driftMagnitude: '0.8 units/day',
    impactRadius: '5 km',
    description: 'A rapidly expanding temporal distortion causing localized time skips and echoes.',
  },
  {
    id: 'anom-002',
    name: 'Silent Mire Echo',
    location: { x: 400, y: 100 },
    severity: 'medium',
    resonanceFrequency: '2.1 Hz (Chronal)',
    driftMagnitude: '0.3 units/day',
    impactRadius: '2 km',
    description: 'A stable but persistent echo of past events, occasionally manifesting phantom structures.',
  },
  {
    id: 'anom-003',
    name: 'Forgotten Peak Ripple',
    location: { x: 650, y: 450 },
    severity: 'low',
    resonanceFrequency: '1.2 Hz (Spatiotemporal)',
    driftMagnitude: '0.1 units/day',
    impactRadius: '1 km',
    description: 'Minor temporal ripples, mostly affecting local flora and fauna growth cycles.',
  },
  {
    id: 'anom-004',
    name: 'Canyon of Lost Moments',
    location: { x: 250, y: 500 },
    severity: 'high',
    resonanceFrequency: '5.9 Hz (Reality Shear)',
    driftMagnitude: '1.2 units/day',
    impactRadius: '10 km',
    description: 'A dangerous zone where moments are lost and regained, leading to severe disorientation.',
  },
  {
    id: 'anom-005',
    name: 'Glimmering Oasis Flux',
    location: { x: 700, y: 180 },
    severity: 'medium',
    resonanceFrequency: '3.5 Hz (Temporal Flow)',
    driftMagnitude: '0.5 units/day',
    impactRadius: '3 km',
    description: 'A fluctuating temporal flow that causes objects to age and de-age unpredictably.',
  },
];

export default mockAnomalies;
