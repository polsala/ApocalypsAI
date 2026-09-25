const { faker } = require('@faker-js/faker');

/**
 * Generates a random star system name.
 * @returns {string} A fictional star system name.
 */
function generateStarSystemName() {
  return `${faker.word.adjective()} ${faker.word.noun()} Nebula`;
}

/**
 * Generates random celestial coordinates.
 * @returns {{sector: string, quadrant: string, cluster: string, designation: string}} Celestial coordinates.
 */
function generateCoordinates() {
  const sectors = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'];
  const quadrants = ['I', 'II', 'III', 'IV'];
  const clusters = ['Orion', 'Pleiades', 'Andromeda', 'Cygnus', 'Hercules'];
  const designation = faker.number.int({ min: 100, max: 9999 });

  return {
    sector: sectors[faker.number.int({ max: sectors.length - 1 })],
    quadrant: quadrants[faker.number.int({ max: quadrants.length - 1 })],
    cluster: clusters[faker.number.int({ max: clusters.length - 1 })],
    designation: `X-${designation}`
  };
}

/**
 * Generates a whimsical description for a star system.
 * @param {object} coordinates - The celestial coordinates of the star system.
 * @returns {string} A fictional star system description.
 */
function generateDescription(coordinates) {
  const phenomena = [
    'pulsating nebulae', 'uncharted asteroid fields', 'ancient alien ruins', 
    'rare crystalline formations', 'a sentient gas giant', 'a black hole anomaly',
    'a nexus of wormholes', 'a rogue planet', 'a binary star system with unusual orbits'
  ];
  const inhabitants = [
    'nomadic traders', 'a reclusive monastic order', 'sentient energy beings', 
    'a forgotten robotic civilization', 'silicon-based lifeforms', 'interdimensional travelers'
  ];

  return `Located in the ${coordinates.sector} ${coordinates.quadrant}, this system is known for its ${faker.helpers.arrayElement(phenomena)}. It is rumored to be a haven for ${faker.helpers.arrayElement(inhabitants)}.`;
}

/**
 * Generates a complete star system object.
 * @returns {Promise<{name: string, coordinates: object, description: string}>} A star system object.
 */
async function generateStarSystem() {
  const name = generateStarSystemName();
  const coordinates = generateCoordinates();
  const description = generateDescription(coordinates);

  return {
    name,
    coordinates,
    description
  };
}

/**
 * Main function to handle CLI execution.
 */
async function main() {
  if (process.argv.includes('--cli')) {
    const system = await generateStarSystem();
    console.log(`Star System: ${system.name}`);
    console.log(`Coordinates: ${system.coordinates.sector} ${system.coordinates.quadrant} ${system.coordinates.cluster} ${system.coordinates.designation}`);
    console.log(`Description: ${system.description}`);
  }
}

// Export for programmatic use and CLI execution
module.exports = {
  generateStarSystem,
  main
};

// Execute main if run directly as a script
if (require.main === module) {
  main();
}
