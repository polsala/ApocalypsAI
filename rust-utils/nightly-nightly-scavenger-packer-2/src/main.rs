use std::env;
use scavenger_packer::{parse_item, knapsack, Item};

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <capacity> <item1> <item2> ...", args[0]);
        eprintln!("Item format: name:weight:value");
        std::process::exit(1);
    }
    let capacity = args[1]
        .parse::<usize>()
        .expect("Invalid capacity – must be a positive integer");
    let mut items = Vec::new();
    for arg in &args[2..] {
        match parse_item(arg) {
            Some(item) => items.push(item),
            None => {
                eprintln!("Invalid item format: {}", arg);
                std::process::exit(1);
            }
        }
    }
    let (max_value, selected) = knapsack(&items, capacity);
    println!("Maximum value: {}", max_value);
    println!("Selected items:");
    for &i in &selected {
        let it = &items[i];
        println!("- {} (weight: {}, value: {})", it.name, it.weight, it.value);
    }
}
