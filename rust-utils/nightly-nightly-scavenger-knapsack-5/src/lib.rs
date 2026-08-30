use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct Item {
    pub name: String,
    pub weight: u32,
    pub value: u32,
}

/// Greedy knapsack: sort by value/weight ratio descending, pick while weight permits.
pub fn greedy_knapsack(items: &[Item], max_weight: u32) -> Vec<Item> {
    let mut sorted = items.to_vec();
    sorted.sort_by(|a, b| {
        let r1 = a.value as f64 / a.weight as f64;
        let r2 = b.value as f64 / b.weight as f64;
        r2.partial_cmp(&r1).unwrap()
    });
    let mut total_weight = 0;
    let mut selected = Vec::new();
    for item in sorted {
        if total_weight + item.weight <= max_weight {
            total_weight += item.weight;
            selected.push(item);
        }
    }
    selected
}
