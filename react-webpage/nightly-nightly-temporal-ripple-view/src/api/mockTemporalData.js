// Mock rationale: Provides a static dataset for the UI to render,
// ensuring the application is runnable and testable without a live backend.
const mockTemporalData = [
  {
    id: 'TR-001',
    type: 'Temporal Drift',
    severity: 4,
    timestamp: '2024-07-20T10:00:00Z',
    status: 'active',
  },
  {
    id: 'TR-002',
    type: 'Echo Chamber Resonance',
    severity: 2,
    timestamp: '2024-07-20T11:30:00Z',
    status: 'active',
  },
  {
    id: 'TR-003',
    type: 'Minor Chronal Tear',
    severity: 5,
    timestamp: '2024-07-20T12:45:00Z',
    status: 'active',
  },
  {
    id: 'TR-004',
    type: 'Localized Time Dilation',
    severity: 3,
    timestamp: '2024-07-19T15:20:00Z',
    status: 'stabilized', // Example of an already stabilized anomaly
  },
  {
    id: 'TR-005',
    type: 'Void Whisper Fluctuation',
    severity: 1,
    timestamp: '2024-07-20T09:10:00Z',
    status: 'active',
  },
  {
    id: 'TR-006',
    type: 'Temporal Echo Loop',
    severity: 3,
    timestamp: '2024-07-20T14:05:00Z',
    status: 'active',
  },
];

export default mockTemporalData;
