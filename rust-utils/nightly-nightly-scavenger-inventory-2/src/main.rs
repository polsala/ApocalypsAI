use rand::prelude::*;
use std::env;

const ITEMS: &[&str] = &[
    "Canned Beans",
    "Rusty Pipe",
    "Solar Charger",
    "Mutant Mushroom",
    "Tattered Map",
    "Water Purifier",
    "Makeshift Armor",
    "Old Radio",
    "Scrap Metal",
    "Radiation Suit",
];

fn generate_inventory(seed: Option<u64>) -> Vec<(u32, &'static str)> {
    let mut rng: StdRng = match seed {
        Some(s) => SeedableRng::seed_from_u64(s),
        None => StdRng::from_entropy(),
    };
    let mut chosen = Vec::new();
    let mut indices: Vec<usize> = (0..ITEMS.len()).collect();
    indices.shuffle(&mut rng);
    for &idx in indices.iter().take(5) {
        let qty = rng.gen_range(1..=10);
        chosen.push((qty, ITEMS[idx]));
    }
    chosen
}

fn main() {
    let seed = env::var("SCAV_SEED")
        .ok()
        .and_then(|s| s.parse::<u64>().ok());
    let inventory = generate_inventory(seed);
    for (qty, item) in inventory {
        println!("{} x {}", qty, item);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_inventory_fixed_seed() {
        let inv = generate_inventory(Some(42));
        let expected = vec![
            (4, "Radiation Suit"),
            (9, "Scrap Metal"),
            (2, "Old Radio"),
            (5, "Solar Charger"),
            (3, "Canned Beans"),
        ];
        assert_eq!(inv, expected);
    }
}
