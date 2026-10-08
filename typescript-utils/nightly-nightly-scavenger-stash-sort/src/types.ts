export interface Item {
  name: string;
  type: string;
  weight: number;
  volume: number;
  value: number;
}

export type ItemRule = (item: Item) => boolean;

export interface StashCategory {
  name: string;
  priority: number; // Higher number means higher priority
  rules: ItemRule[];
}

export type SortedStash = {
  [categoryName: string]: Item[];
};
