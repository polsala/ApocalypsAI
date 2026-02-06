use std::env;

const EVENTS: [&str; 6] = [
    "Solar flares turned the sky crimson",
    "Mutant crows claimed the rooftops",
    "The Great Flood of 2077 receded",
    "Radioactive rain sang lullabies",
    "Robots held a tea party",
    "Time loops caused endless sunrise",
];

fn generate_event(date: &str) -> &'static str {
    // Simple deterministic hash: sum of ASCII bytes
    let sum: u32 = date.bytes().map(|b| b as u32).sum();
    let idx = (sum as usize) % EVENTS.len();
    EVENTS[idx]
}

fn print_usage() {
    eprintln!("Usage: chrono-chronicle <YYYY-MM-DD>");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        print_usage();
        std::process::exit(1);
    }
    let date = &args[1];
    // Very light validation – ensure the string looks like a date
    if date.len() != 10 || &date[4..5] != "-" || &date[7..8] != "-" {
        eprintln!("Error: date must be in YYYY-MM-DD format");
        std::process::exit(1);
    }
    let event = generate_event(date);
    println!("{}", event);
}
