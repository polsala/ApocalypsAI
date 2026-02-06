import { checkBlueprint, Inventory, Blueprint, Component } from '../src/index';

describe('checkBlueprint', () => {
  // # Mock rationale: Using mock inventory and blueprint data to ensure deterministic and offline tests.
  // This avoids external dependencies and ensures test reliability.

  const mockInventory: Inventory = new Map([
    ['Rusty Cog', 10],
    ['Glimmering Shard', 5],
    ['Whisper-Infused Wire', 15],
    ['Scrap Metal', 100],
  ]);

  it('should return true and no missing components if blueprint can be crafted', () => {
    const craftableBlueprint: Blueprint = {
      name: 'Basic Survival Kit',
      requirements: [
        { componentName: 'Scrap Metal', requiredQuantity: 50 },
        { componentName: 'Whisper-Infused Wire', requiredQuantity: 5 },
      ],
    };

    const result = checkBlueprint(mockInventory, craftableBlueprint);
    expect(result.canCraft).toBe(true);
    expect(result.missingComponents).toEqual([]);
  });

  it('should return false and list missing components if a component is entirely absent', () => {
    const missingComponentBlueprint: Blueprint = {
      name: 'Temporal Stabilizer Mk. II',
      requirements: [
        { componentName: 'Rusty Cog', requiredQuantity: 2 },
        { componentName: 'Temporal Flux Capacitor', requiredQuantity: 1 }, // Not in inventory
      ],
    };

    const result = checkBlueprint(mockInventory, missingComponentBlueprint);
    expect(result.canCraft).toBe(false);
    expect(result.missingComponents).toEqual([
      { name: 'Temporal Flux Capacitor', quantity: 1 },
    ]);
  });

  it('should return false and list missing components if quantity is insufficient', () => {
    const insufficientQuantityBlueprint: Blueprint = {
      name: 'Advanced Energy Cell',
      requirements: [
        { componentName: 'Glimmering Shard', requiredQuantity: 10 }, // Only 5 in inventory
        { componentName: 'Rusty Cog', requiredQuantity: 1 },
      ],
    };

    const result = checkBlueprint(mockInventory, insufficientQuantityBlueprint);
    expect(result.canCraft).toBe(false);
    expect(result.missingComponents).toEqual([
      { name: 'Glimmering Shard', quantity: 5 }, // 10 required - 5 available = 5 missing
    ]);
  });

  it('should handle blueprints with no requirements', () => {
    const emptyBlueprint: Blueprint = {
      name: 'Simple Trinket',
      requirements: [],
    };

    const result = checkBlueprint(mockInventory, emptyBlueprint);
    expect(result.canCraft).toBe(true);
    expect(result.missingComponents).toEqual([]);
  });

  it('should handle multiple missing components', () => {
    const multipleMissingBlueprint: Blueprint = {
      name: 'Grand Void Engine',
      requirements: [
        { componentName: 'Void Crystal', requiredQuantity: 3 }, // Missing
        { componentName: 'Temporal Flux Capacitor', requiredQuantity: 2 }, // Missing
        { componentName: 'Glimmering Shard', requiredQuantity: 100 }, // Insufficient
      ],
    };

    const result = checkBlueprint(mockInventory, multipleMissingBlueprint);
    expect(result.canCraft).toBe(false);
    expect(result.missingComponents).toEqual([
      { name: 'Void Crystal', quantity: 3 },
      { name: 'Temporal Flux Capacitor', quantity: 2 },
      { name: 'Glimmering Shard', quantity: 95 },
    ]);
  });

  it('should return true if inventory has exact quantities required', () => {
    const exactMatchInventory: Inventory = new Map([
      ['Rare Alloy', 2],
      ['Power Core', 1],
    ]);
    const exactMatchBlueprint: Blueprint = {
      name: 'Power Armor Plating',
      requirements: [
        { componentName: 'Rare Alloy', requiredQuantity: 2 },
        { componentName: 'Power Core', requiredQuantity: 1 },
      ],
    };

    const result = checkBlueprint(exactMatchInventory, exactMatchBlueprint);
    expect(result.canCraft).toBe(true);
    expect(result.missingComponents).toEqual([]);
  });
});
