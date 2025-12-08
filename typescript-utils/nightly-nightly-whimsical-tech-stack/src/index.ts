import { shuffle } from 'lodash';

const ADJECTIVES = [
  'Quantum', 'Neon', 'Hyperloop', 'Velociraptor', 'Giggle',
  'Nebula', 'Pickle', 'Jello', 'Zombie', 'Rainbow'
];

const TECH_TERMS = [
  'Orchestration', 'API', 'Framework', 'Blockchain', 'Cloud',
  'Microservices', 'AI', 'Database', 'Compiler', 'Middleware'
];

function generateStack(): string {
  const adj = ADJECTIVES[Math.floor(Math.random() * ADJECTIVES.length)];
  const tech = TECH_TERMS[Math.floor(Math.random() * TECH_TERMS.length)];
  const suffix = Math.random() > 0.5 ? ` ${Math.floor(Math.random() * 100)}+` : '';
  return `${adj} ${tech}${suffix}`;
}

const count = process.argv[2] ? parseInt(process.argv[2]) : 5;

for (let i = 0; i < count; i++) {
  console.log(`${i+1}. ${generateStack()}`);
}
