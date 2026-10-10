use std::env;
use nightly_gear_ratio_cli::compute_gear_inches;

fn print_usage() {
    eprintln!("Usage: <CHAINRING> <COG> [WHEEL_DIAMETER_MM]");
    eprintln!("Example: 50 12");
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() < 2 || args.len() > 3 {
        print_usage();
        std::process::exit(1);
    }
    let chainring: u32 = args[0].parse().unwrap_or_else(|_| {
        eprintln!("Invalid chainring value");
        std::process::exit(1);
    });
    let cog: u32 = args[1].parse().unwrap_or_else(|_| {
        eprintln!("Invalid cog value");
        std::process::exit(1);
    });
    let wheel_diameter_mm: u32 = if args.len() == 3 {
        args[2].parse().unwrap_or_else(|_| {
            eprintln!("Invalid wheel diameter value");
            std::process::exit(1);
        })
    } else {
        700
    };
    let gear_inches = compute_gear_inches(chainring, cog, wheel_diameter_mm);
    println!("Gear inches: {:.2}", gear_inches);
}
