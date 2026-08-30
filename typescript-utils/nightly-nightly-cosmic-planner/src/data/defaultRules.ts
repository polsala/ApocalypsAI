import { AlignmentRule } from '../types';

export const defaultAlignmentRules: AlignmentRule[] = [
  {
    description: 'Avoid deployments during Mercury Retrograde',
    condition: {
      eventImpacts: ['Technology', 'Planning'],
    },
    action: 'AVOID',
    targetTasks: ['Deploy', 'Release', 'Launch'],
  },
  {
    description: 'Review and introspection favored during New Moon',
    condition: {
      eventName: 'New Moon in Scorpio', // Specific event name
    },
    action: 'RECOMMEND',
    targetTasks: ['Review', 'Introspect', 'Plan', 'Reflect'],
  },
  {
    description: 'Brainstorming and creative tasks are favored during Full Moon',
    condition: {
      eventImpacts: ['Manifestation', 'Creativity'],
    },
    action: 'RECOMMEND',
    targetTasks: ['Brainstorm', 'Create', 'Innovate', 'Design'],
  },
  {
    description: 'High-energy tasks are good when Mars is active',
    condition: {
      eventName: 'Mars in Gemini',
    },
    action: 'RECOMMEND',
    targetTasks: ['Execute', 'Action', 'Implement'],
  },
  {
    description: 'Avoid critical communications during Mercury Retrograde',
    condition: {
      eventImpacts: ['Communication'],
    },
    action: 'AVOID',
    targetTasks: ['Communicate', 'Negotiate', 'Present'],
  },
  {
    description: 'Focus on stability and resources during Taurus Full Moon',
    condition: {
      eventName: 'Full Moon in Taurus',
    },
    action: 'RECOMMEND',
    targetTasks: ['Budget', 'Resource Allocation', 'Stabilize', 'Secure'],
  },
];
