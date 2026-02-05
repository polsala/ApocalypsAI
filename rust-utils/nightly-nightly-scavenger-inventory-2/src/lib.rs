/// Represents a scavenged item.
#[derive(Debug, Clone, PartialEq)]
pub struct Item {
    pub name: String,
    pub weight: f64,
}

/// Parse a slice of strings like "name:weight" into a vector of `Item`.
///
/// Invalid entries are ignored (they are filtered out). This keeps the CLI robust.
pub fn parse_items(raw: &[String]) -> Vec<Item> {
    raw.iter()
        .filter_map(|s| {
            let parts: Vec<&str> = s.splitn(2, ':').collect();
            if parts.len() != 2 {
                return None;
            }
            let name = parts[0].trim().to_string();
            let weight_res = parts[1].trim().parse::<f64>();
            match weight_res {
                Ok(w) => Some(Item { name, weight: w }),
                Err(_) => None,
            }
        })
        .collect()
}

/// Given a list of items and an excess weight, suggest a minimal set of items to drop.
///
/// The algorithm sorts items by weight descending and picks the heaviest items until the
/// accumulated drop weight meets or exceeds the excess. This is a greedy approximation that
/// works well for small lists and keeps the implementation simple.
pub fn suggest_drops(items: &[Item], excess: f64) -> Vec<Item> {
    if excess <= 0.0 {
        return vec![];
    }
    let mut sorted = items.to_vec();
    sorted.sort_by(|a, b| b.weight.partial_cmp(&a.weight).unwrap());
    let mut dropped = Vec::new();
    let mut accumulated = 0.0;
    for item in sorted {
        if accumulated >= excess {
            break;
        }
        accumulated += item.weight;
        dropped.push(item);
    }
    dropped
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_items() {
        let raw = vec![
            "water:2.5".to_string(),
            "food:3".to_string(),
            "invalid".to_string(),
            "toolkit:bad".to_string(),
        ];
        let items = parse_items(&raw);
        assert_eq!(items.len(), 2);
        assert_eq!(items[0], Item { name: "water".into(), weight: 2.5 });
        assert_eq!(items[1], Item { name: "food".into(), weight: 3.0 });
    }

    #[test]
    fn test_suggest_drops_exact() {
        let items = vec![
            Item { name: "toolkit".into(), weight: 5.0 },
            Item { name: "water".into(), weight: 2.0 },
            Item { name: "food".into(), weight: 3.0 },
        ];
        let drops = suggest_drops(&items, 4.0);
        // Heaviest first: toolkit (5) already exceeds excess, so only toolkit is suggested.
        assert_eq!(drops, vec![Item { name: "toolkit".into(), weight: 5.0 }]);
    }

    #[test]
    fn test_suggest_drops_multiple() {
        let items = vec![
            Item { name: "ammo".into(), weight: 1.0 },
            Item { name: "water".into(), weight: 2.0 },
            Item { name: "food".into(), weight: 3.0 },
        ];
        let drops = suggest_drops(&items, 4.5);
        // Heaviest: food (3) + water (2) = 5 >= 4.5
        assert_eq!(drops.len(), 2);
        assert_eq!(drops[0].name, "food");
        assert_eq!(drops[1].name, "water");
    }
}
