use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

fn parse_line(line: &str) -> Option<(f64, f64)> {
    let parts: Vec<&str> = line.trim().split(',').collect();
    if parts.len() != 2 {
        return None;
    }
    let duration = parts[0].parse::<f64>().ok()?;
    let intensity = parts[1].parse::<f64>().ok()?;
    Some((duration, intensity))
}

fn read_events<R: BufRead>(reader: R) -> Vec<(f64, f64)> {
    reader
        .lines()
        .filter_map(|l| l.ok())
        .filter_map(|line| parse_line(&line))
        .collect()
}

fn main() {
    // Determine input source: file argument or stdin
    let args: Vec<String> = env::args().collect();
    let reader: Box<dyn BufRead> = if args.len() > 1 {
        let file = File::open(&args[1]).expect("Failed to open file");
        Box::new(BufReader::new(file))
    } else {
        Box::new(BufReader::new(io::stdin()))
    };

    let events = read_events(reader);
    let total = nightly_radiation_exposure_calculator::total_dose(&events);
    println!("Total dose: {:.3} mSv", total);
    if total > 100.0 {
        eprintln!("Warning: dose exceeds safe threshold of 100 mSv!");
    }
}
