use std::env;

// Import the library function
use nightly_barter_calculator::calculate_exchange;

fn parse_arg<T: std::str::FromStr>(arg: Option<&String>, name: &str) -> T {
    arg.expect(&format!("Missing argument: {}", name))
        .parse()
        .ok()
        .expect(&format!("Invalid value for {}", name))
}

fn main() {
    let args: Vec<String> = env::args().collect();
    // args[0] is the program name
    let item_a = args.get(1).expect("Missing ITEM_A");
    let item_b = args.get(2).expect("Missing ITEM_B");
    let value_a: f64 = parse_arg(args.get(3), "VALUE_A");
    let value_b: f64 = parse_arg(args.get(4), "VALUE_B");

    let rate = calculate_exchange(value_a, value_b);
    // Show two decimal places for readability
    println!("You need {:.2} {} to equal 1 {}", rate, item_a, item_b);
}
