import { CosmicEvent } from '../types';

export const defaultCosmicEvents: CosmicEvent[] = [
  {
    name: 'Mercury in Retrograde',
    startDate: '2024-04-01',
    endDate: '2024-04-25',
    impacts: ['Communication', 'Technology', 'Travel', 'Planning'],
  },
  {
    name: 'Mercury in Retrograde', // Example of another retrograde period
    startDate: '2024-08-05',
    endDate: '2024-08-28',
    impacts: ['Communication', 'Technology', 'Travel', 'Planning'],
  },
  {
    name: 'Full Moon in Taurus',
    startDate: '2024-10-17',
    endDate: '2024-10-18', // Full moon is typically a single day, but can have lingering effects
    impacts: ['Stability', 'Resources', 'Grounding', 'Manifestation'],
  },
  {
    name: 'New Moon in Scorpio',
    startDate: '2024-10-31',
    endDate: '2024-11-01',
    impacts: ['Transformation', 'Introspection', 'Secrets', 'Rebirth'],
  },
  {
    name: 'Mars in Gemini',
    startDate: '2024-08-01',
    endDate: '2024-09-15',
    impacts: ['Action', 'Communication', 'Energy', 'Versatility'],
  },
  {
    name: 'Venus in Leo',
    startDate: '2024-07-11',
    endDate: '2024-08-04',
    impacts: ['Love', 'Creativity', 'Self-Expression', 'Romance'],
  },
  {
    name: 'Jupiter in Gemini',
    startDate: '2024-05-25',
    endDate: '2025-06-09',
    impacts: ['Expansion', 'Learning', 'Communication', 'Curiosity'],
  },
];
