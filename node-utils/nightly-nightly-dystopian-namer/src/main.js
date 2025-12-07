const prefixes = ['Rusted', 'Ashen', 'Crimson', 'Feral', 'Wasteland', 'Scorched', 'Broken', 'Dustbound'];
const suffixes = ['Sanctum', 'Hive', 'Grid', 'Outpost', 'Collective', 'Bastion', 'Node', 'Enclave'];

export function generateDystopianName() {
  const prefix = prefixes[Math.floor(Math.random() * prefixes.length)];
  const suffix = suffixes[Math.floor(Math.random() * suffixes.length)];
  return `${prefix}${suffix}`;
}

if (require.main === module) {
  console.log(generateDystopianName());
}
