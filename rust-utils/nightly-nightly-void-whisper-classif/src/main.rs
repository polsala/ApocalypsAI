use clap::Parser;
use nightly_void_whisper_classif::{classify_whisper, Category, Urgency, ClassificationResult};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The cryptic whisper to classify
    #[clap(short, long)]
    whisper: String,
}

fn main() {
    let args = Args::parse();

    let result = classify_whisper(&args.whisper);

    println!("Whisper: \"{}\"", args.whisper);
    println!("Classification: {}", result.category);
    println!("Urgency: {}", result.urgency);
}
