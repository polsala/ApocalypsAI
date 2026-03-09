pub struct Item {
    pub name: String,
    pub weight: u32,
    pub value: u32,
}

impl Clone for Item {
    fn clone(&self) -> Self {
        Item {
            name: self.name.clone(),
            weight: self.weight,
            value: self.value,
        }
    }
}

/// Parse a comma‑separated list of `weight:value:name` strings into `Item`s.
///
/// # Panics
///
/// Panics if any entry does not contain exactly three parts or if weight/value are not valid integers.
pub fn parse_items(s: &str) -> Vec<Item> {
    s.split(',')
        .filter(|p| !p.trim().is_empty())
        .map(|p| {
            let parts: Vec<&str> = p.split(':').collect();
            if parts.len() != 3 {
                panic!("Invalid item format: {}", p);
            }
            let weight = parts[0]
                .parse::<u32>()
                .expect("Invalid weight component");
            let value = parts[1]
                .parse::<u32>()
                .expect("Invalid value component");
            let name = parts[2].to_string();
            Item { name, weight, value }
        })
        .collect()
}

/// Brute‑force solution to the 0/1 knapsack problem.
/// Returns the subset of items with the highest total value that does not exceed `capacity`.
pub fn optimal_subset(capacity: u32, items: &[Item]) -> Vec<Item> {
    let n = items.len();
    let mut best_value = 0u32;
    let mut best_subset: Vec<Item> = Vec::new();

    // Enumerate all possible subsets using a bitmask.
    for mask in 0u64..(1u64 << n) {
        let mut total_weight = 0u32;
        let mut total_value = 0u32;
        let mut subset: Vec<Item> = Vec::new();
        for i in 0..n {
            if (mask >> i) & 1 == 1 {
                let item = &items[i];
                total_weight += item.weight;
                total_value += item.value;
                subset.push(item.clone());
            }
        }
        if total_weight <= capacity && total_value > best_value {
            best_value = total_value;
            best_subset = subset;
        }
    }
    best_subset
}
