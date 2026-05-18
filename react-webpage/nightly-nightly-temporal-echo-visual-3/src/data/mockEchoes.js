// Mock rationale: Using static mock data ensures deterministic tests without external dependencies.
const mockEchoes = [
  {
    id: 'e001',
    timestamp: '2077-10-23T14:30:00Z',
    location: 'Sector Gamma-7, Old Library Ruins',
    type: 'Temporal Ripple',
    severity: 2,
    description: 'Faint echoes of pre-collapse library chatter. Mostly harmless, but can cause mild disorientation.',
  },
  {
    id: 'e002',
    timestamp: '2077-10-23T15:15:00Z',
    location: 'Wasteland Crossroads, Junction 42',
    type: 'Echo Cascade',
    severity: 4,
    description: 'Rapid succession of past vehicle sounds and distant screams. High risk of auditory hallucinations and panic.',
  },
  {
    id: 'e003',
    timestamp: '2077-10-23T16:00:00Z',
    location: 'Forgotten Bunker, Level 3',
    type: 'Void Whisper',
    severity: 5,
    description: 'Whispers from the void, speaking in forgotten tongues. Causes extreme temporal nausea and potential reality slippage. Avoid at all costs.',
  },
  {
    id: 'e004',
    timestamp: '2077-10-23T17:05:00Z',
    location: 'Hydroponics Dome Alpha',
    type: 'Temporal Ripple',
    severity: 1,
    description: 'Brief flicker of sunlight from a bygone era. Mildly pleasant, no known adverse effects.',
  },
  {
    id: 'e005',
    timestamp: '2077-10-23T18:20:00Z',
    location: 'The Great Crater Rim',
    type: 'Echo Cascade',
    severity: 3,
    description: 'Visual distortions of a bustling marketplace. Can lead to confusion and misidentification of threats.',
  },
  {
    id: 'e006',
    timestamp: '2077-10-23T19:00:00Z',
    location: 'Relic Scrapyard, Section B',
    type: 'Temporal Ripple',
    severity: 2,
    description: 'Sound of a distant, perfectly tuned radio playing pre-collapse music. Can be distracting.',
  },
  {
    id: 'e007',
    timestamp: '2077-10-23T20:30:00Z',
    location: 'The Shifting Sands',
    type: 'Void Whisper',
    severity: 5,
    description: 'A chilling silence, deeper than any natural quiet, accompanied by a feeling of non-existence. Highly dangerous.',
  },
  {
    id: 'e008',
    timestamp: '2077-10-23T21:00:00Z',
    location: 'Old Highway 99, collapsed bridge',
    type: 'Temporal Ripple',
    severity: 1,
    description: 'Brief scent of fresh rain and ozone. Harmless, but can evoke strong nostalgia.',
  }
];

export default mockEchoes;
