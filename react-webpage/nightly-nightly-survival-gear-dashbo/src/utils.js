export function computeTotalWeight(items) {\n  // items: array of {name:string, weight:number, durability:number}\n  return items.reduce((sum, item) => sum + (item.weight || 0), 0);\n}
