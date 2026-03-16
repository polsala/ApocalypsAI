const fs = require('fs');

/**
 * Loads resources from a JSON file.
 * @param {string} filePath - Path to the resources JSON file.
 * @returns {Object.<string, Object>} An object mapping resource names to their data.
 */
function loadResources(filePath) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    const resourcesArray = JSON.parse(data);
    // Convert array to object for easier lookup by name
    return resourcesArray.reduce((acc, res) => {
      acc[res.name] = res;
      return acc;
    }, {});
  } catch (error) {
    if (error.code === 'ENOENT') {
      // File not found, return empty resources and create default
      console.warn('Resources file not found. Creating default resources.json.');
      const defaultResources = [
        { name: 'Water', baseValue: 10, scarcity: 0.8, desirability: 1.5 },
        { name: 'Canned Food', baseValue: 15, scarcity: 1.2, desirability: 1.3 },
        { name: 'Batteries', baseValue: 20, scarcity: 0.5, desirability: 1.8 },
        { name: 'Scrap Metal', baseValue: 5, scarcity: 1.5, desirability: 0.7 },
        { name: 'Meds', baseValue: 50, scarcity: 0.1, desirability: 2.0 }
      ];
      saveResources(filePath, defaultResources.reduce((acc, res) => { acc[res.name] = res; return acc; }, {}));
      return defaultResources.reduce((acc, res) => { acc[res.name] = res; return acc; }, {});
    }
    console.error('Error loading resources:', error.message);
    return {};
  }
}

/**
 * Saves resources to a JSON file.
 * @param {string} filePath - Path to the resources JSON file.
 * @param {Object.<string, Object>} resources - An object mapping resource names to their data.
 */
function saveResources(filePath, resources) {
  try {
    // Convert object back to array for saving
    const resourcesArray = Object.values(resources);
    fs.writeFileSync(filePath, JSON.stringify(resourcesArray, null, 2), 'utf8');
  } catch (error) {
    console.error('Error saving resources:', error.message);
  }
}

/**
 * Calculates a weighted value for a given resource.
 * Formula: baseValue * (desirability / scarcity)
 * @param {string} resourceName - The name of the resource.
 * @param {Object.<string, Object>} resources - All available resources.
 * @returns {number} The calculated weighted value.
 */
function calculateResourceValue(resourceName, resources) {
  const resource = resources[resourceName];
  if (!resource) {
    throw new Error(`Resource '${resourceName}' not found.`);
  }
  // Ensure scarcity is not zero to prevent division by zero
  const scarcityFactor = resource.scarcity > 0 ? resource.scarcity : 0.01; 
  return resource.baseValue * (resource.desirability / scarcityFactor);
}

/**
 * Suggests a fair amount of 'wantResource' for a given amount of 'haveResource'.
 * @param {string} haveResource - The name of the resource you have.
 * @param {string} wantResource - The name of the resource you want.
 * @param {number} haveAmount - The amount of the resource you have.
 * @param {Object.<string, Object>} resources - All available resources.
 * @returns {number} The suggested amount of the wanted resource.
 */
function suggestTrade(haveResource, wantResource, haveAmount, resources) {
  const haveValue = calculateResourceValue(haveResource, resources);
  const wantValue = calculateResourceValue(wantResource, resources);

  if (wantValue === 0) {
    // Avoid division by zero if wantResource has effectively no value
    return 0;
  }

  return (haveValue * haveAmount) / wantValue;
}

module.exports = {
  loadResources,
  saveResources,
  calculateResourceValue,
  suggestTrade
};
