export type Mood = 'low' | 'medium' | 'high' | 'any';

export interface MicroQuest {
  id: string;
  title: string;
  description: string;
  moods: Mood[];
  durationMinutes: number;
}

export interface DistractionDetox {
  id: string;
  title: string;
  description: string;
  durationMinutes: number;
}

export const microQuests: MicroQuest[] = [
  {
    id: 'hydrate',
    title: 'Hydrate with Irradiated Water',
    description: 'Replenish your internal reserves. Drink a glass of water.',
    moods: ['low', 'medium', 'high'],
    durationMinutes: 2,
  },
  {
    id: 'scan-horizon',
    title: 'Scan the Horizon for Anomalies',
    description: 'Take a moment to look away from your screen. Stretch your neck and shoulders.',
    moods: ['low', 'medium'],
    durationMinutes: 3,
  },
  {
    id: 'repair-tear',
    title: 'Repair a Small Temporal Tear',
    description: 'Organize one small thing: a file, an email, or a browser tab.',
    moods: ['medium', 'high'],
    durationMinutes: 5,
  },
  {
    id: 'data-scavenge',
    title: 'Data Scavenge for Lost Knowledge',
    description: 'Read one article or documentation page related to a current task.',
    moods: ['high'],
    durationMinutes: 10,
  },
  {
    id: 'recalibrate-sensor',
    title: 'Recalibrate Your Focus Sensor',
    description: 'Close all unnecessary applications and tabs. Clear your desktop.',
    moods: ['low', 'medium', 'high'],
    durationMinutes: 5,
  },
];

export const distractionDetoxes: DistractionDetox[] = [
  {
    id: 'silence-void',
    title: 'Silence the Void Whispers',
    description: 'Turn off all notifications (phone, email, chat) for the next 15 minutes.',
    durationMinutes: 15,
  },
  {
    id: 'temporal-perception',
    title: 'Calibrate Temporal Perception',
    description: 'Take 3 deep, slow breaths. Focus only on your breath.',
    durationMinutes: 2,
  },
  {
    id: 'reality-check',
    title: 'Perform a Reality Check',
    description: 'Stand up, walk around for 2 minutes, and observe your surroundings.',
    durationMinutes: 2,
  },
  {
    id: 'energy-siphon',
    title: 'Siphon Ambient Energy',
    description: 'Listen to 5 minutes of calming music or ambient sounds.',
    durationMinutes: 5,
  },
];
