use clap::Parser;

mod lib;

#[derive(Parser)]
#[command(author, version, about = "Estimate radiation decay using half‑life")]
struct Args {
    /// Initial radiation dose in millisieverts
    #[arg(short, long)]
    initial: f64,
    /// Half‑life duration in hours
    #[arg(short, long)]
    half_life: f64,
    /// Elapsed time in hours
    #[arg(short, long)]
    elapsed: f64,
}

fn main() {
    let args = Args::parse();
    let remaining = lib::calculate_decay(args.initial, args.half_life, args.elapsed);
    println!("{:.3} mSv remaining", remaining);
}
