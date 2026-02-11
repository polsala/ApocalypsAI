export interface Rule {
    type: 'name' | 'extension' | 'size' | 'content';
    pattern?: string; // Regex string for name/extension/content
    minSizeKB?: number; // For size type, inclusive
    maxSizeKB?: number; // For size type, inclusive
}

export interface Category {
    name: string; // e.g., "Survival Blueprints"
    description: string;
    rules: Rule[];
    destinationSubdir: string; // e.g., "blueprints"
}

export interface ArchivistConfig {
    defaultCategoryName: string; // e.g., "Unclassified Scraps"
    categories: Category[];
}
