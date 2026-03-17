import { ResourceItem, ResourceCategory } from './types';

export const KNOWN_RESOURCES: ResourceItem[] = [
  { name: 'Nutrient Paste', category: 'Food', unit: 'can' },
  { name: 'Hydro-Purification Tablets', category: 'Water', unit: 'tablet' },
  { name: 'Temporal Stabilizers', category: 'Mystical', unit: 'device' },
  { name: 'Glimmering Dust', category: 'Mystical', unit: 'gram' },
  { name: 'Quantum Entanglement String', category: 'Components', unit: 'meter' },
  { name: 'First-Aid Medkit', category: 'Medical', unit: 'kit' },
  { name: 'Scrap Metal', category: 'Components', unit: 'kg' },
  { name: 'Water Ration', category: 'Water', unit: 'liter' },
  { name: 'Energy Cell', category: 'Tools', unit: 'unit' },
  { name: 'Pre-War Maps', category: 'Tools', unit: 'map' }
];

export const getResourceUnit = (resourceName: string): string => {
  const resource = KNOWN_RESOURCES.find(r => r.name === resourceName);
  return resource ? resource.unit : 'units';
};
