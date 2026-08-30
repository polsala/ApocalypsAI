use std::env;

mod lib;
use lib::{parse_items, knapsack, Item};

fn print_usage() {
    eprintln!("Usage: scavenger_knapsack <capacity> <item1> <item2> ...");
    eprintln!("Each item: name,weight,value (comma separated)");
    eprintln!("Example: scavenger_knapsack 10 apple,2,5 water,3,8 medkit,5,12");
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() < 2 {
        print_usage();
        std::process::exit(1);
    }
    let capacity = match args[0].parse::<usize>() {
        Ok(c) => c,
        Err(_) => {
            eprintln!("Invalid capacity: {}", args[0]);
            std::process::exit(1);
        }
    };
    let items = parse_items(&args[1..]);
    if items.is_empty() {
        eprintln!("No valid items provided.");
        std::process::exit(1);
    }
    let (selected, total) = knapsack(&items, capacity);
    println!("Selected items: {}", selected.join(", "));
    println!("Total value: {}", total);
}
