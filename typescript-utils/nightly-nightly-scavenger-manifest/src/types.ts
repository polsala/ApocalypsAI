export type ItemCondition = "Pristine" | "Good" | "Worn" | "Damaged" | "Broken" | "Mysterious";

export interface ScavengedItem {
  id: string;
  name: string;
  category: string;
  condition: ItemCondition;
  quantity: number;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ManifestData {
  items: ScavengedItem[];
}
