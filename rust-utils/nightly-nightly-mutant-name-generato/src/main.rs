use std::env;
use mutant_name_generator::generate_name;

fn parse_seed(args: &[String]) -> Option<u64> {
    let mut iter = args.iter();
    while let Some(arg) = iter.next() {
        if arg == "--seed" {
            if let Some(val) = iter.next() {
                return val.parse::<u64>().ok();
            }
        }
    }
    None
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let seed = parse_seed(&args).unwrap_or_else(|| {
        // Fallback: use current Unix timestamp as seed
        use std::time::{SystemTime, UNIX_EPOCH};
        let duration = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap_or_default();
        duration.as_secs()
    });
    let name = generate_name(seed);
    println!("{}", name);
}
