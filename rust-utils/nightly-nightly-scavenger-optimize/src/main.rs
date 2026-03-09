use std::env;
use scavenger_optimize::{parse_items, optimal_subset};

fn print_usage() {
    eprintln!("Usage: scavenger-optimize <capacity> <items>");
    eprintln!("  capacity: integer weight limit");
    eprintln!("  items: comma-separated list of weight:value:name");
    eprintln!("Example: 5 \"2:5:water,1:3:food,3:9:medicine\"");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }
    let capacity: u32 = match args[1].parse() {
        Ok(c) => c,
        Err(_) => {
            eprintln!("Invalid capacity");
            std::process::exit(1);
        }
    };
    let items_str = &args[2];
    let items = parse_items(items_str);
    let optimal = optimal_subset(capacity, &items);
    if optimal.is_empty() {
        println!("No items can be taken within capacity {}", capacity);
    } else {
        let total_value: u32 = optimal.iter().map(|i| i.value).sum();
        println!("Optimal selection (total value {}):", total_value);
        for item in optimal {
            println!("- {} (weight {}, value {})", item.name, item.weight, item.value);
        }
    }
}
