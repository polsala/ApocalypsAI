use std::env;
use std::process;
use radiation_estimator::compute_max_hours;

fn print_usage() {
    eprintln!("Usage: radiation-estimator <level> [limit]");
    eprintln!("  <level>: radiation level in µSv/h (positive number)");
    eprintln!("  [limit]: dose limit in µSv (default 1000)");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 || args.len() > 3 {
        print_usage();
        process::exit(1);
    }

    let level: f64 = match args[1].parse() {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Error: invalid radiation level");
            process::exit(1);
        }
    };

    let limit: f64 = if args.len() == 3 {
        match args[2].parse() {
            Ok(v) => v,
            Err(_) => {
                eprintln!("Error: invalid dose limit");
                process::exit(1);
            }
        }
    } else {
        1000.0
    };

    match compute_max_hours(level, limit) {
        Ok(hours) => {
            println!(
                "You can stay exposed for up to {:.2} hours before reaching {:.0} µSv.",
                hours, limit
            );
        }
        Err(msg) => {
            eprintln!("Error: {}", msg);
            process::exit(1);
        }
    }
}
