mod lib;
use lib::{read_radiation_csv, color_for_level};
use std::env;
use std::process;

fn print_usage() {
    eprintln!("Usage: radiomap <path-to-csv>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage();
        process::exit(1);
    }
    let path = &args[1];
    match read_radiation_csv(path) {
        Ok(records) => {
            println!("{:<20} {:>10}", "Location", "Level (µSv/h)");
            for (loc, lvl) in records {
                let color = color_for_level(lvl);
                let reset = "\x1b[0m";
                println!("{}{: <20} {:>10.2}{}", color, loc, lvl, reset);
            }
        }
        Err(e) => {
            eprintln!("Error reading CSV: {}", e);
            process::exit(1);
        }
    }
}
