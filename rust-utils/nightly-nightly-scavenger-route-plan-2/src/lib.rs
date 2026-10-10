use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct Location {
    pub name: String,
    pub x: f64,
    pub y: f64,
}

fn distance(a: &Location, b: &Location) -> f64 {
    ((a.x - b.x).powi(2) + (a.y - b.y).powi(2)).sqrt()
}

fn nearest_neighbor_route(mut locations: Vec<Location>) -> Vec<String> {
    if locations.is_empty() {
        return vec![];
    }
    // Start from the first location in the list
    let mut current = locations.remove(0);
    let mut route = vec![current.name.clone()];

    while !locations.is_empty() {
        // Find the closest remaining location
        let (idx, _) = locations
            .iter()
            .enumerate()
            .min_by(|(_, a), (_, b)| {
                distance(&current, a)
                    .partial_cmp(&distance(&current, b))
                    .unwrap()
            })
            .unwrap();
        let next = locations.remove(idx);
        route.push(next.name.clone());
        current = next;
    }
    route
}

/// Compute a scavenger route from a JSON string.
///
/// Returns the ordered list of location names.
pub fn plan_route(json_data: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let locations: Vec<Location> = serde_json::from_str(json_data)?;
    Ok(nearest_neighbor_route(locations))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_distance() {
        let a = Location { name: "A".into(), x: 0.0, y: 0.0 };
        let b = Location { name: "B".into(), x: 3.0, y: 4.0 };
        assert_eq!(distance(&a, &b), 5.0);
    }

    #[test]
    fn test_nearest_neighbor_route() {
        let locs = vec![
            Location { name: "Start".into(), x: 0.0, y: 0.0 },
            Location { name: "A".into(), x: 1.0, y: 0.0 },
            Location { name: "B".into(), x: 2.0, y: 0.0 },
        ];
        let route = nearest_neighbor_route(locs);
        assert_eq!(route, vec!["Start", "A", "B"]);
    }

    #[test]
    fn test_plan_route() {
        let json = r#"[
            {"name": "Alpha", "x": 0.0, "y": 0.0},
            {"name": "Beta",  "x": 5.0, "y": 0.0},
            {"name": "Gamma", "x": 2.0, "y": 0.0}
        ]"#;
        let route = plan_route(json).unwrap();
        // Starting point is Alpha, then Gamma (closest), then Beta
        assert_eq!(route, vec!["Alpha", "Gamma", "Beta"]);
    }
}
