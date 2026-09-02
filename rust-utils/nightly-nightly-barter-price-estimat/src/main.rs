use std::collections::HashMap;
use std::env;

fn base_prices() -> HashMap<&'static str, u32> {
    let mut m = HashMap::new();
    m.insert("water", 10);
    m.insert("canned-food", 15);
    m.insert("medicine", 30);
    m.insert("ammo", 25);
    m.insert("fuel", 20);
    m.insert("scrap-metal", 5);
    m
}

/// Deterministic modifier based on the sum of the UTF‑8 bytes of the item name.
/// The sum modulo 5 yields a value in 0..4, which translates to a 0‑40% increase.
fn price_for(item: &str) -> Option<u32> {
    let base = base_prices().get(item)?;
    let sum: u32 = item.bytes().map(|b| b as u32).sum();
    let modifier = 1.0 + (sum % 5) as f64 * 0.1; // 1.0, 1.1, …, 1.4
    Some((*base as f64 * modifier).round() as u32)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <item-name>", args[0]);
        std::process::exit(1);
    }
    let item = args[1].as_str();
    match price_for(item) {
        Some(p) => println!("Estimated barter price for '{}' is {} caps", item, p),
        None => {
            eprintln!(
                "Unknown item '{}'. Known items: water, canned-food, medicine, ammo, fuel, scrap-metal",
                item
            );
            std::process::exit(1);
        }
    }
}
