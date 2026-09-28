use std::env;

mod lib;

fn print_usage() {
    eprintln!("Usage: nightly-battery-life-estimator <capacity_mAh> <draw_mA>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        print_usage();
        std::process::exit(1);
    }

    let capacity = match lib::parse_arg(&args[1]) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("{}", e);
            std::process::exit(1);
        }
    };

    let draw = match lib::parse_arg(&args[2]) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("{}", e);
            std::process::exit(1);
        }
    };

    let hours = lib::estimate_hours(capacity, draw);
    if hours.is_infinite() {
        println!("Infinite runtime (draw is 0 mA)");
    } else {
        println!("{:.2} hours", hours);
    }
}
