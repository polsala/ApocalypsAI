use std::env;
use nightly_shelter_capacity_planner::can_survive;

fn print_usage() {
    eprintln!("Usage: nightly-shelter-capacity-planner <people> <water_per_day_liters> <total_water_liters> <food_per_day_kcal> <total_food_kcal> <days>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 7 {
        print_usage();
        std::process::exit(1);
    }
    let people: u32 = args[1].parse().unwrap_or_else(|_| { print_usage(); std::process::exit(1); });
    let water_per_day: f64 = args[2].parse().unwrap_or_else(|_| { print_usage(); std::process::exit(1); });
    let total_water: f64 = args[3].parse().unwrap_or_else(|_| { print_usage(); std::process::exit(1); });
    let food_per_day: f64 = args[4].parse().unwrap_or_else(|_| { print_usage(); std::process::exit(1); });
    let total_food: f64 = args[5].parse().unwrap_or_else(|_| { print_usage(); std::process::exit(1); });
    let days: u32 = args[6].parse().unwrap_or_else(|_| { print_usage(); std::process::exit(1); });

    let survivable = can_survive(people, water_per_day, total_water, food_per_day, total_food, days);
    if survivable {
        println!("Survivable: Yes");
    } else {
        println!("Survivable: No");
    }
}
