use std::env;
use std::process;

fn print_usage() {
    eprintln!("Usage: <charge_percent> <consumption_rate_per_hour> [--survival]");
}

fn parse_arg(arg: &str) -> Result<f64, &'static str> {
    arg.parse::<f64>().map_err(|_| "Invalid number")
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() < 2 || args.len() > 3 {
        print_usage();
        process::exit(1);
    }

    let charge = match parse_arg(&args[0]) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("{}", e);
            process::exit(1);
        }
    };
    let mut rate = match parse_arg(&args[1]) {
        Ok(v) => v,
        Err(e) => {
            eprintln!("{}", e);
            process::exit(1);
        }
    };
    let survival = args.get(2).map(|s| s == "--survival").unwrap_or(false);
    if survival {
        rate = nightly_battery_estimator::apply_survival(rate);
    }

    match nightly_battery_estimator::estimate_hours(charge, rate) {
        Some(hours) => {
            if survival {
                println!("Estimated remaining time (survival mode): {:.2} hours", hours);
            } else {
                println!("Estimated remaining time: {:.2} hours", hours);
            }
        }
        None => {
            println!("Cannot estimate time with non‑positive consumption rate.");
        }
    }
}
