export const environments = {
  Desert: [
    "Water purification tablets",
    "Sun hat",
    "Sunscreen",
    "Lightweight tarp",
    "Sand goggles"
  ],
  Tundra: [
    "Thermal blanket",
    "Insulated jacket",
    "Snow shovel",
    "Hand warmers",
    "Highâcalorie rations"
  ],
  Urban: [
    "Multiâtool",
    "Firstâaid kit",
    "Portable charger",
    "Crowbar",
    "Dust mask"
  ],
  Forest: [
    "Fire starter",
    "Compass",
    "Water filter",
    "Mosquito net",
    "Durable boots"
  ]
};

export function getKit(env) {
  return environments[env] || [];
}
