// Mock rationale: Simulates fetching data from an API or parsing project files
// without requiring actual network requests or file system access,
// ensuring deterministic and offline tests.
const mockClutter = [
  {
    id: 'c1',
    name: 'feature/old-experimental-ui',
    type: 'Branch',
    temporalWeight: 365, // days old
    description: 'Branch for a UI experiment from last year, never merged.',
    link: 'https://github.com/polsala/ApocalypsAI/tree/feature/old-experimental-ui'
  },
  {
    id: 'c2',
    name: 'Bug: Infinite loop in temporal-anomaly-detector',
    type: 'Issue',
    temporalWeight: 180,
    description: 'Issue reported 6 months ago, still open, no activity.',
    link: 'https://github.com/polsala/ApocalypsAI/issues/123'
  },
  {
    id: 'c3',
    name: 'unused-dependency-lib',
    type: 'Dependency',
    temporalWeight: 730,
    description: 'A library installed 2 years ago, no longer used anywhere.',
    link: 'https://www.npmjs.com/package/unused-dependency-lib'
  },
  {
    id: 'c4',
    name: 'docs/outdated-setup-guide',
    type: 'Documentation',
    temporalWeight: 500,
    description: 'Setup guide for an old system version, needs update or removal.',
    link: 'https://github.com/polsala/ApocalypsAI/wiki/Outdated-Setup-Guide'
  },
  {
    id: 'c5',
    name: 'PR: Refactor legacy auth (stale)',
    type: 'Pull Request',
    temporalWeight: 250,
    description: 'PR opened 8 months ago, review comments unaddressed.',
    link: 'https://github.com/polsala/ApocalypsAI/pull/456'
  },
  {
    id: 'c6',
    name: 'Task: Investigate void-whispers-v2',
    type: 'Task',
    temporalWeight: 90,
    description: 'A task from last quarter, never started.',
    link: 'https://trello.com/b/apocalypsai/card/void-whispers-v2'
  },
  {
    id: 'c7',
    name: 'feature/new-temporal-stabilizer',
    type: 'Branch',
    temporalWeight: 30,
    description: 'New feature branch, recently active, but no PR yet.',
    link: 'https://github.com/polsala/ApocalypsAI/tree/feature/new-temporal-stabilizer'
  }
];

export default mockClutter;
