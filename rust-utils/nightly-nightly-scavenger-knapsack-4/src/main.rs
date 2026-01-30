use std::io::{self, Read};

mod lib;
use lib::{Item, solve_knapsack};

fn main() {
    // Read entire stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read stdin");
    let mut lines = input.lines();

    // First line: weight limit
    let limit_line = match lines.next() {
        Some(l) => l.trim(),
        None => {
            eprintln!("Expected weight limit on first line");
            std::process::exit(1);
        }
    };
    let limit: usize = match limit_line.parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid weight limit: {}", limit_line);
            std::process::exit(1);
        }
    };

    // Remaining lines: name weight value
    let mut items = Vec::new();
    for (idx, line) in lines.enumerate() {
        let parts: Vec<&str> = line.split_whitespace().collect();
        if parts.len() != 3 {
            eprintln!("Line {} malformed: '{}', expected 'name weight value'", idx + 2, line);
            std::process::exit(1);
        }
        let name = parts[0].to_string();
        let weight: usize = match parts[1].parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Invalid weight on line {}", idx + 2);
                std::process::exit(1);
            }
        };
        let value: usize = match parts[2].parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Invalid value on line {}", idx + 2);
                std::process::exit(1);
            }
        };
        items.push(Item { name, weight, value });
    }

    let selected = solve_knapsack(limit, &items);
    for name in selected {
        println!("{}", name);
    }
}
