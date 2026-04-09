use std::env;

fn parse_arg<T: std::str::FromStr>(arg: &str, name: &str) -> T {
    arg.parse::<T>().unwrap_or_else(|_| {
        eprintln!("Invalid {}: {}", name, arg);
        std::process::exit(1);
    })
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 7 {
        eprintln!(
            "Usage: {} <item1> <rarity1> <utility1> <item2> <rarity2> <utility2>",
            args[0]
        );
        std::process::exit(1);
    }
    let item1 = &args[1];
    let rarity1 = parse_arg::<u32>(&args[2], "rarity1");
    let utility1 = parse_arg::<u32>(&args[3], "utility1");
    let item2 = &args[5];
    let rarity2 = parse_arg::<u32>(&args[4], "rarity2");
    let utility2 = parse_arg::<u32>(&args[6], "utility2");

    // Simple validation: values must be between 1 and 10 inclusive.
    for (val, name) in [
        (rarity1, "rarity1"),
        (utility1, "utility1"),
        (rarity2, "rarity2"),
        (utility2, "utility2"),
    ] {
        if val == 0 || val > 10 {
            eprintln!("{} must be between 1 and 10", name);
            std::process::exit(1);
        }
    }

    let value1 = nightly_barter_calculator::compute_value(rarity1, utility1);
    let value2 = nightly_barter_calculator::compute_value(rarity2, utility2);

    let ratio = (value1 as f64) / (value2 as f64);
    println!("1 {} ≈ {:.2} {}", item1, ratio, item2);
}
