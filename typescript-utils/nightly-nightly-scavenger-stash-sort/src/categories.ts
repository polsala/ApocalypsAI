import { StashCategory } from './types';

export const defaultCategories: StashCategory[] = [
  {
    name: 'Survival Essentials',
    priority: 100,
    rules: [
      (item) => item.type === 'Food',
      (item) => item.type === 'Water',
      (item) => item.type === 'Medicine',
      (item) => item.type === 'Tool' && item.value > 10,
    ],
  },
  {
    name: 'Tradeable Trinkets',
    priority: 80,
    rules: [
      (item) => item.type === 'Relic' && item.value > 50,
      (item) => item.type === 'Component' && item.value > 20,
      (item) => item.type === 'Weapon' && item.value > 30,
    ],
  },
  {
    name: 'Curious Collectibles',
    priority: 60,
    rules: [
      (item) => item.type === 'Relic',
      (item) => item.type === 'Book',
      (item) => item.type === 'Toy',
    ],
  },
  {
    name: 'Scrap & Salvage',
    priority: 10,
    rules: [
      (item) => item.type === 'Junk',
      (item) => item.type === 'Component',
      (item) => item.weight > 1.5 && item.value < 15,
    ],
  },
];
