const skillsData = [
  {
    id: 'scavenging-1',
    name: 'Basic Scavenging',
    description: 'Improved ability to find useful items in ruins.',
    prerequisites: [],
    tier: 1,
    branch: 'Scavenging'
  },
  {
    id: 'scavenging-2',
    name: 'Advanced Scavenging',
    description: 'Locate rare components and hidden stashes.',
    prerequisites: ['scavenging-1'],
    tier: 2,
    branch: 'Scavenging'
  },
  {
    id: 'crafting-1',
    name: 'Makeshift Crafting',
    description: 'Assemble basic tools and repairs from scrap.',
    prerequisites: [],
    tier: 1,
    branch: 'Crafting'
  },
  {
    id: 'crafting-2',
    name: 'Resourceful Engineering',
    description: 'Craft more complex items and modify existing gear.',
    prerequisites: ['crafting-1', 'scavenging-1'],
    tier: 2,
    branch: 'Crafting'
  },
  {
    id: 'combat-1',
    name: 'Melee Proficiency',
    description: 'Basic training in close-quarters combat.',
    prerequisites: [],
    tier: 1,
    branch: 'Combat'
  },
  {
    id: 'combat-2',
    name: 'Ranged Weaponry',
    description: 'Familiarity with improvised firearms and projectile weapons.',
    prerequisites: ['combat-1'],
    tier: 2,
    branch: 'Combat'
  },
  {
    id: 'temporal-1',
    name: 'Temporal Awareness',
    description: 'Slight sensitivity to temporal distortions.',
    prerequisites: [],
    tier: 1,
    branch: 'Temporal'
  },
  {
    id: 'temporal-2',
    name: 'Echo Manipulation',
    description: 'Briefly glimpse or subtly alter recent echoes.',
    prerequisites: ['temporal-1', 'scavenging-2'],
    tier: 2,
    branch: 'Temporal'
  }
];

export default skillsData;
