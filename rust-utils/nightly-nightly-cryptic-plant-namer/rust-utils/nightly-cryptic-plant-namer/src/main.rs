use rand::seq::SliceRandom;
use rand::thread_rng;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    let describe = args.iter().any(|a| a == "--describe");
    let (name, description) = generate_plant();
    println!("{}", name);
    if describe {
        println!("{}", description);
    }
}

fn generate_plant() -> (String, String) {
    // Mock rationale: fixed adjective and root lists give deterministic randomness when seeded.
    let adjectives = [
        "Aurea", "Sable", "Verdant", "Noctis", "Luminosa", "Silva", "Crimson", "Ebon",
    ];
    let roots = [
        "luminosa", "thornus", "folia", "petala", "bloomus", "vinea", "cactus", "herba",
    ];
    let mut rng = thread_rng();
    let adj = adjectives.choose(&mut rng).unwrap();
    let root = roots.choose(&mut rng).unwrap();
    let name = format!("{} {}", adj, root);
    let description = format!(
        "A {} plant that {}.",
        adj.to_lowercase(),
        match *adj {
            "Aurea" => "shimmers with golden hues",
            "Sable" => "absorbs light like a dark veil",
            "Verdant" => "covers the ground in lush green",
            "Noctis" => "blooms only under moonlight",
            "Luminosa" => "glows faintly at dusk",
            "Silva" => "whispers with the wind of ancient forests",
            "Crimson" => "drips a ruby‑red sap",
            "Ebon" => "has bark as black as obsidian",
            _ => "has mysterious properties",
        }
    );
    (name, description)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_plant_name_non_empty() {
        let (name, description) = generate_plant();
        assert!(!name.trim().is_empty(), "Generated name should not be empty");
        assert!(!description.trim().is_empty(), "Generated description should not be empty");
    }

    #[test]
    fn test_name_structure() {
        let (name, _) = generate_plant();
        // Expect exactly one space (Unicode non‑breaking space) separating two words
        let parts: Vec<&str> = name.split('\u{202F}').collect();
        assert_eq!(parts.len(), 2, "Name should consist of two parts separated by a narrow no‑break space");
    }
}
