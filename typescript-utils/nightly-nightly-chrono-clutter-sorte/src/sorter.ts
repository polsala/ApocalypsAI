export interface Category {
  id: string;
  name: string;
  description: string;
  priority: number;
}

export interface Rule {
  keyword: string;
  targetCategoryId: string;
}

export interface ChronoConfig {
  categories: Category[];
  rules: Rule[];
  defaultCategoryId: string;
}

export type SortedResult = { [categoryId: string]: string[] };

export class ChronoClutterSorter {
  private categories: Map<string, Category>;
  private rules: Rule[];
  private defaultCategory: Category;

  constructor(config: ChronoConfig) {
    if (!config.categories || config.categories.length === 0) {
      throw new Error("Configuration must contain at least one category.");
    }
    if (!config.defaultCategoryId) {
      throw new Error("Configuration must specify a defaultCategoryId.");
    }

    this.categories = new Map(config.categories.map(cat => [cat.id, cat]));
    this.rules = config.rules || [];

    const defaultCat = this.categories.get(config.defaultCategoryId);
    if (!defaultCat) {
      throw new Error(`Default category with ID '${config.defaultCategoryId}' not found.`);
    }
    this.defaultCategory = defaultCat;
  }

  sort(items: string[]): SortedResult {
    const result: SortedResult = {};
    this.categories.forEach(cat => (result[cat.id] = [])); // Initialize all categories

    for (const item of items) {
      let assigned = false;
      for (const rule of this.rules) {
        if (item.toLowerCase().includes(rule.keyword.toLowerCase())) {
          if (this.categories.has(rule.targetCategoryId)) {
            result[rule.targetCategoryId].push(item);
            assigned = true;
            break;
          } else {
            console.warn(`Warning: Rule for keyword '${rule.keyword}' targets unknown category ID '${rule.targetCategoryId}'. Item '${item}' will be sorted to default.`);
          }
        }
      }
      if (!assigned) {
        result[this.defaultCategory.id].push(item);
      }
    }
    return result;
  }

  getCategoryById(id: string): Category | undefined {
    return this.categories.get(id);
  }

  getAllCategories(): Category[] {
    return Array.from(this.categories.values()).sort((a, b) => a.priority - b.priority);
  }
}
