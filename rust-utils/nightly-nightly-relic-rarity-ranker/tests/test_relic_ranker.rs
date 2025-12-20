#![cfg(test)]

use crate::Relic;

// Mock rationale: These tests operate purely on in-memory `Relic` structs to verify the scoring and sorting logic.
// No file I/O or external dependencies are involved, ensuring determinism and offline execution.

#[test]
fn test_relic_rarity_scoring() {
    let relic1 = Relic {
        name: "Ancient PDA".to_string(),
        category: "data".to_string(),
        condition: 90,
        scarcity_factor: 8,
    };
    // Expected: 8 * (1.0 + 90/100) = 8 * 1.9 = 15.2
    assert_eq!(relic1.rarity_score(), 15.2);

    let relic2 = Relic {
        name: "Common Rock".to_string(),
        category: "decoration".to_string(),
        condition: 100,
        scarcity_factor: 1,
    };
    // Expected: 1 * (1.0 + 100/100) = 1 * 2.0 = 2.0
    assert_eq!(relic2.rarity_score(), 2.0);

    let relic3 = Relic {
        name: "Broken Laser Pistol".to_string(),
        category: "weapon".to_string(),
        condition: 10,
        scarcity_factor: 7,
    };
    // Expected: 7 * (1.0 + 10/100) = 7 * 1.1 = 7.7
    assert_eq!(relic3.rarity_score(), 7.7);
}

#[test]
fn test_relic_utility_scoring() {
    let relic1 = Relic {
        name: "Working Water Purifier".to_string(),
        category: "tool".to_string(),
        condition: 80,
        scarcity_factor: 7,
    };
    // Expected: 9.0 (tool) * (80/100) = 9.0 * 0.8 = 7.2
    assert_eq!(relic1.utility_score(), 7.2);

    let relic2 = Relic {
        name: "Moldy Bread".to_string(),
        category: "food".to_string(),
        condition: 10,
        scarcity_factor: 2,
    };
    // Expected: 7.0 (food) * (10/100) = 7.0 * 0.1 = 0.7
    assert_eq!(relic2.utility_score(), 0.7);

    let relic3 = Relic {
        name: "Shiny Bottlecap".to_string(),
        category: "decoration".to_string(),
        condition: 99,
        scarcity_factor: 1,
    };
    // Expected: 1.0 (decoration) * (99/100) = 1.0 * 0.99 = 0.99
    assert_eq!(relic3.utility_score(), 0.99);

    let relic4 = Relic {
        name: "Unknown Device".to_string(),
        category: "mystery".to_string(),
        condition: 50,
        scarcity_factor: 5,
    };
    // Expected: 3.0 (default) * (50/100) = 3.0 * 0.5 = 1.5
    assert_eq!(relic4.utility_score(), 1.5);
}

#[test]
fn test_relic_sorting_by_rarity() {
    let relic1 = Relic {
        name: "A".to_string(), category: "tool".to_string(), condition: 90, scarcity_factor: 8,
    }; // Rarity: 15.2
    let relic2 = Relic {
        name: "B".to_string(), category: "food".to_string(), condition: 50, scarcity_factor: 5,
    }; // Rarity: 7.5
    let relic3 = Relic {
        name: "C".to_string(), category: "weapon".to_string(), condition: 100, scarcity_factor: 9,
    }; // Rarity: 18.0

    let mut relics = vec![relic1.clone(), relic2.clone(), relic3.clone()];
    relics.sort_by(|a, b| b.rarity_score().partial_cmp(&a.rarity_score()).unwrap_or(std::cmp::Ordering::Equal));

    assert_eq!(relics[0], relic3);
    assert_eq!(relics[1], relic1);
    assert_eq!(relics[2], relic2);
}

#[test]
fn test_relic_sorting_by_utility() {
    let relic1 = Relic {
        name: "A".to_string(), category: "tool".to_string(), condition: 90, scarcity_factor: 8,
    }; // Utility: 9.0 * 0.9 = 8.1
    let relic2 = Relic {
        name: "B".to_string(), category: "food".to_string(), condition: 50, scarcity_factor: 5,
    }; // Utility: 7.0 * 0.5 = 3.5
    let relic3 = Relic {
        name: "C".to_string(), category: "weapon".to_string(), condition: 100, scarcity_factor: 9,
    }; // Utility: 10.0 * 1.0 = 10.0

    let mut relics = vec![relic1.clone(), relic2.clone(), relic3.clone()];
    relics.sort_by(|a, b| b.utility_score().partial_cmp(&a.utility_score()).unwrap_or(std::cmp::Ordering::Equal));

    assert_eq!(relics[0], relic3);
    assert_eq!(relics[1], relic1);
    assert_eq!(relics[2], relic2);
}
