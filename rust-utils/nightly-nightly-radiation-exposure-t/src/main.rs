use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <file> [threshold]", args[0]);
        std::process::exit(1);
    }
    let file_path = &args[1];
    let threshold: Option<f64> = if args.len() >= 3 {
        match args[2].parse() {
            Ok(v) => Some(v),
            Err(_) => {
                eprintln!("Invalid threshold value: {}", args[2]);
                std::process::exit(1);
            }
        }
    } else {
        None
    };
    match nightly_radiation_exposure_tracker::parse_and_compute(file_path) {
        Ok(total) => {
            println!("Total dose: {:.3} mSv", total);
            if let Some(th) = threshold {
                if total > th {
                    println!("Warning: total dose exceeds threshold of {:.3} mSv!", th);
                }
            }
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
