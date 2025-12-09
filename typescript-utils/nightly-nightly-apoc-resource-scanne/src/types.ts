export type ResourceCategory = "Edibles" | "Materials" | "Medical" | "Tech" | "Water";
export type ResourceRarity = "Common" | "Uncommon" | "Rare" | "Very Rare";

export interface Resource {
    name: string;
    category: ResourceCategory;
    rarity: ResourceRarity;
    discoveredAt: string; // ISO 8601 timestamp
}
