// src/sorter.ts

export interface Item {
  name: string;
  // Whimsical attributes for prioritization
  attributes: { [key: string]: number };
}

export interface Category {
  name: string;
  priority: 'Very High' | 'High' | 'Medium' | 'Low';
  keywords: string[];
  attributeForPrioritization: string; // e.g., 'crunchiness', 'sparkle', 'danger'
}

export interface CategorizedStash {
  [categoryName: string]: Item[];
}

export class StashSorter {
  private categories: Category[] = [
    {
      name: 'Crunchy Sustenance',
      priority: 'High',
      keywords: ['food', 'snack', 'bar', 'fruit', 'vegetable', 'meat', 'ration', 'granola', 'cookie', 'nut', 'jerky'],
      attributeForPrioritization: 'crunchiness',
    },
    {
      name: 'Essential Oddities',
      priority: 'Medium',
      keywords: ['tool', 'wrench', 'tape', 'rope', 'wire', 'battery', 'light', 'knife', 'can opener', 'bottle opener', 'spoon', 'fork', 'cup', 'plate'],
      attributeForPrioritization: 'utility',
    },
    {
      name: 'Shiny Baubles',
      priority: 'Low',
      keywords: ['shiny', 'sparkle', 'gem', 'gold', 'silver', 'coin', 'jewelry', 'bottle cap', 'rock', 'mirror', 'glitter'],
      attributeForPrioritization: 'sparkle',
    },
    {
      name: 'Mysterious Gadgets',
      priority: 'Very High',
      keywords: ['glowing', 'vial', 'unknown', 'ancient', 'device', 'gadget', 'machine', 'scroll', 'orb', 'crystal', 'data', 'chip', 'mystery'],
      attributeForPrioritization: 'danger', // or 'mystery'
    },
    {
      name: 'Textiles',
      priority: 'Low',
      keywords: ['cloth', 'fabric', 'blanket', 'shirt', 'pants', 'sock', 'hat', 'scarf', 'tattered', 'worn'],
      attributeForPrioritization: 'warmth',
    },
  ];

  /**
   * Assigns whimsical attributes to an item based on its name.
   * This is a simplified, deterministic "mock" for generating attributes.
   * # Mock rationale: In a real-world scenario, attributes might come from a database,
   * # an external API, or a more complex NLP process. For this self-contained utility,
   * # we deterministically generate them based on string properties to ensure offline tests.
   */
  private generateWhimsicalAttributes(itemName: string): { [key: string]: number } {
    const lowerName = itemName.toLowerCase();
    const attributes: { [key: string]: number } = {};

    // General whimsy based on length
    attributes['whimsy'] = (itemName.length % 10) + 1;

    // Specific attributes based on keywords
    if (lowerName.includes('crunchy') || lowerName.includes('granola') || lowerName.includes('biscuit') || lowerName.includes('jerky')) {
      attributes['crunchiness'] = Math.min(10, (itemName.length % 5) + 6); // 6-10
    } else if (lowerName.includes('soft') || lowerName.includes('chewy') || lowerName.includes('jelly') || lowerName.includes('bread')) {
      attributes['crunchiness'] = Math.min(10, (itemName.length % 5) + 1); // 1-5
    } else {
      attributes['crunchiness'] = (itemName.length % 10) + 1;
    }

    if (lowerName.includes('shiny') || lowerName.includes('sparkle') || lowerName.includes('gem') || lowerName.includes('gold')) {
      attributes['sparkle'] = Math.min(10, (itemName.length % 5) + 6);
    } else if (lowerName.includes('dull') || lowerName.includes('plain')) {
      attributes['sparkle'] = Math.min(10, (itemName.length % 5) + 1);
    } else {
      attributes['sparkle'] = (itemName.length % 10) + 1;
    }

    if (lowerName.includes('tool') || lowerName.includes('wrench') || lowerName.includes('tape') || lowerName.includes('knife')) {
      attributes['utility'] = Math.min(10, (itemName.length % 5) + 6);
    } else {
      attributes['utility'] = (itemName.length % 10) + 1;
    }

    if (lowerName.includes('glowing') || lowerName.includes('vial') || lowerName.includes('unknown') || lowerName.includes('danger') || lowerName.includes('mysterious')) {
      attributes['danger'] = Math.min(10, (itemName.length % 5) + 6);
      attributes['mystery'] = Math.min(10, (itemName.length % 5) + 6);
    } else {
      attributes['danger'] = (itemName.length % 10) + 1;
      attributes['mystery'] = (itemName.length % 10) + 1;
    }

    if (lowerName.includes('blanket') || lowerName.includes('scarf') || lowerName.includes('warm') || lowerName.includes('hat')) {
      attributes['warmth'] = Math.min(10, (itemName.length % 5) + 6);
    } else {
      attributes['warmth'] = (itemName.length % 10) + 1;
    }

    return attributes;
  }

  public categorizeAndPrioritize(itemNames: string[]): CategorizedStash {
    const categorized: CategorizedStash = {};

    // Initialize categories
    this.categories.forEach(cat => {
      categorized[cat.name] = [];
    });

    for (const name of itemNames) {
      const item: Item = {
        name: name,
        attributes: this.generateWhimsicalAttributes(name),
      };

      let assigned = false;
      for (const category of this.categories) {
        const lowerName = name.toLowerCase();
        if (category.keywords.some(keyword => lowerName.includes(keyword))) {
          categorized[category.name].push(item);
          assigned = true;
          break; // Assign to the first matching category
        }
      }

      if (!assigned) {
        // Default category for unassigned items
        if (!categorized['Uncategorized Oddities']) {
          categorized['Uncategorized Oddities'] = [];
        }
        categorized['Uncategorized Oddities'].push(item);
      }
    }

    // Prioritize items within each category
    for (const categoryName in categorized) {
      const categoryConfig = this.categories.find(c => c.name === categoryName);
      if (categoryConfig) {
        categorized[categoryName].sort((a, b) => {
          const attrA = a.attributes[categoryConfig.attributeForPrioritization] || 0;
          const attrB = b.attributes[categoryConfig.attributeForPrioritization] || 0;
          // Sort descending by the primary attribute
          return attrB - attrA;
        });
      } else {
        // For 'Uncategorized Oddities', sort by general whimsy
        categorized[categoryName].sort((a, b) => {
          const attrA = a.attributes['whimsy'] || 0;
          const attrB = b.attributes['whimsy'] || 0;
          return attrB - attrA;
        });
      }
    }

    return categorized;
  }

  public getCategoryConfig(categoryName: string): Category | undefined {
    return this.categories.find(c => c.name === categoryName);
  }
}
