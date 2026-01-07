use clap::Parser;
use nightly_cryptic_fortune::{hash_input, FORTUNES};

#[derive(Parser)]
#[command(name = "nightly-cryptic-fortune")]
#[command(about = "Generate a deterministic whimsical fortune based on input text.")]
struct Args {
    /// Input text to generate fortune
    #[arg(required = true)]
    input: String,
}

fn main() {
    let args = Args::parse();
    let index = hash_input(&args.input) % FORTUNES.len();
    println!("Fortune: {}", FORTUNES[index]);
}
