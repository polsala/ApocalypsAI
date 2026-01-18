use clap::Parser;
use radiation_decay::decay;

/// Simple CLI to estimate radiation decay.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Initial radiation level
    #[arg(short, long)]
    initial: f64,

    /// Half‑life period (same units as time)
    #[arg(short = 'l', long)]
    half_life: f64,

    /// Elapsed time
    #[arg(short, long)]
    time: f64,
}

fn main() {
    let args = Args::parse();
    let remaining = decay(args.initial, args.half_life, args.time);
    println!("Remaining radiation: {}", remaining);
}
