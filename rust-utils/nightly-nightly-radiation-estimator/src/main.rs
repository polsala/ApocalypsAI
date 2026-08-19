use std::env;
use crate::compute_dose;

fn print_usage() {
    eprintln!("Usage: --hours <hours> --level <level>");
    eprintln!("Example: cargo run -- --hours 3.5 --level 4");
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let mut hours_opt: Option<f64> = None;
    let mut level_opt: Option<u32> = None;
    let mut i = 0;
    while i < args.len() {
        match args[i].as_str() {
            "--hours" => {
                if i + 1 >= args.len() {
                    print_usage();
                    return;
                }
                hours_opt = args[i + 1].parse::<f64>().ok();
                i += 2;
            }
            "--level" => {
                if i + 1 >= args.len() {
                    print_usage();
                    return;
                }
                level_opt = args[i + 1].parse::<u32>().ok();
                i += 2;
            }
            _ => {
                print_usage();
                return;
            }
        }
    }

    let hours = match hours_opt {
        Some(h) => h,
        None => {
            print_usage();
            return;
        }
    };
    let level = match level_opt {
        Some(l) => l,
        None => {
            print_usage();
            return;
        }
    };

    let dose = compute_dose(hours, level);
    println!("Total radiation dose: {:.2} Sv", dose);
    if dose > 10.0 {
        println!("⚠️  Warning: Dose exceeds safe threshold!");
    }
}
