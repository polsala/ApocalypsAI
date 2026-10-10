mod lib;
use lib::max_exposure_hours;
use std::env;
use std::process;

fn print_usage() {
    eprintln!("Usage: <radiation_uSv_per_h> <dose_limit_mSv>");
}

fn parse_arg(arg: &str) -> Result<f64, std::num::ParseFloatError> {
    arg.parse::<f64>()
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() != 2 {
        print_usage();
        process::exit(1);
    }
    let radiation = match parse_arg(&args[0]) {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid radiation value");
            process::exit(1);
        }
    };
    let dose = match parse_arg(&args[1]) {
        Ok(v) => v,
        Err(_) => {
            eprintln!("Invalid dose limit value");
            process::exit(1);
        }
    };
    let hours = max_exposure_hours(radiation, dose);
    if hours.is_infinite() {
        println!("Infinity (radiation level is zero)");
    } else {
        println!("{:.2}", hours);
    }
}
