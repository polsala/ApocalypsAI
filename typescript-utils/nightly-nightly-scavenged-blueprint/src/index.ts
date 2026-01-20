export interface Component {
  name: string;
  quantity: number;
}

export interface BlueprintRequirement {
  componentName: string;
  requiredQuantity: number;
}

export interface Blueprint {
  name: string;
  requirements: BlueprintRequirement[];
}

export type Inventory = Map<string, number>; // Component name -> quantity

/**
 * Checks if a survivor's inventory contains all necessary components
 * to craft a given blueprint.
 * @param inventory The survivor's current inventory (Map of component name to quantity).
 * @param blueprint The blueprint to check against.
 * @returns An object indicating if the blueprint can be crafted and a list of missing components (if any).
 */
export function checkBlueprint(
  inventory: Inventory,
  blueprint: Blueprint
): { canCraft: boolean; missingComponents: Component[] } {
  const missingComponents: Component[] = [];
  let canCraft = true;

  for (const requirement of blueprint.requirements) {
    const { componentName, requiredQuantity } = requirement;
    const availableQuantity = inventory.get(componentName) || 0;

    if (availableQuantity < requiredQuantity) {
      canCraft = false;
      missingComponents.push({
        name: componentName,
        quantity: requiredQuantity - availableQuantity,
      });
    }
  }

  return { canCraft, missingComponents };
}
