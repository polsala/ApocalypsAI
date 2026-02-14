use std::env;
use std::time::{SystemTime, UNIX_EPOCH};

const ADJECTIVES: &[&str] = &["Gloomy", "Radiant", "Whispering", "Eternal", "Mysterious"];
const ROOTS: &[&str] = &["Acer", "Betula", "Cactus", "Daphne", "Eucalyptus"];

fn generate_name(seed: u64) -> String {
    let adj = ADJECTIVES[(seed as usize) % ADJECTIVES.len()];
    let root = ROOTS[((seed / ADJECTIVES.len() as u64) as usize) % ROOTS.len()];
    format!("{} {}ia", adj, root)
}

fn current_timestamp() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let seed = if args.len() > 2 && args[1] == "--seed" {
        args[2].parse::<u64>().unwrap_or_else(|_| {
            eprintln!("Invalid seed, using current time");
            current_timestamp()
        })
    } else {
        current_timestamp()
    };
    let name = generate_name(seed);
    println!("Your cryptic plant name: {}", name);
}

#[cfg(test)]
mod unit_tests {
    use super::*;

    #[test]
    fn test_generate_name_seed_42() {
        let name = generate_name(42);
        assert_eq!(name, "Whispering Daphneia");
    }
}
