export function computeTotalWeight(items) {
  // items: array of {name:string, weight:number, durability:number}
  return items.reduce((sum, item) => sum + (item.weight || 0), 0);
}
