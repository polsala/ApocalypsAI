use rand::seq::SliceRandom;
use rand::Rng;
use std::env;

mod lib;
use lib::{generate_item, GearItem};

fn main() {
    let args: Vec<String> = env::args().collect();
    let mut count = 1usize;
    if args.len() > 1 {
        if let Some(pos) = args.iter().position(|a| a == "-n" || a == "--number") {
            if let Some(val) = args.get(pos + 1) {
                count = val.parse().unwrap_or(1);
            }
        }
    }

    let mut rng = rand::thread_rng();
    for _ in 0..count {
        let item = generate_item(&mut rng);
        println!("Item: {}", item.name);
        println!("Rarity: {}", item.rarity);
        println!("Description: {}", item.description);
        println!();
    }
}
