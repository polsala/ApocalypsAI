use clap::Parser;
use nightly_safehouse_name_generator::generate_name;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Optional seed for deterministic output
    #[arg(long)]
    seed: Option<u64>,
}

fn main() {
    let args = Args::parse();
    let seed = args.seed.unwrap_or_else(|| {
        // Fallback to current Unix timestamp if no seed is provided
        use std::time::{SystemTime, UNIX_EPOCH};
        let dur = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards");
        dur.as_secs()
    });
    let name = generate_name(seed);
    println!("{}", name);
}
