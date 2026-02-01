export type EchoStatus = 'raw' | 'reframed';

export interface TemporalEcho {
  id: string;
  timestamp: string; // ISO string of when the echo was logged
  description: string;
  impact: string; // Negative impact or feeling associated with the echo
  status: 'raw';
}

export interface ReframedEcho {
  id: string;
  timestamp: string; // Original ISO string of when the echo was logged
  description: string;
  impact: string; // Original negative impact
  status: 'reframed';
  reframedTimestamp: string; // ISO string of when it was reframed
  lesson: string; // The positive lesson learned from the echo
  action: string; // A concrete action to take based on the lesson
}

export type EchoData = TemporalEcho | ReframedEcho;
