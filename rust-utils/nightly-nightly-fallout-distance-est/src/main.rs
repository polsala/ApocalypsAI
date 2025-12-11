use clap::Parser;

/// Simple CLI to estimate safe distance from a fallout source.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Initial radiation level at 1 km (Sv/h)
    #[arg(short, long)]
    initial: f64,

    /// Radioactive half‑life in hours
    #[arg(short = 'l', long)]
    half_life: f64,

    /// Time elapsed since the event in hours
    #[arg(short, long)]
    time: f64,

    /// Safety threshold in Sv/h (default 0.001)
    #[arg(short, long, default_value_t = 0.001)]
    threshold: f64,
}

/// Compute radiation at distance `d` (km) after `t` hours.
fn radiation_at_distance(initial: f64, half_life: f64, time: f64, distance: f64) -> f64 {
    let decay_factor = 0.5_f64.powf(time / half_life);
    initial * decay_factor / (distance * distance)
}

/// Solve for the minimum distance where radiation <= threshold.
fn safe_distance(initial: f64, half_life: f64, time: f64, threshold: f64) -> f64 {
    // Rearranged formula: d = sqrt( initial * decay / threshold )
    let decay_factor = 0.5_f64.powf(time / half_life);
    ((initial * decay_factor) / threshold).sqrt()
}

fn main() {
    let args = Args::parse();
    let distance = safe_distance(args.initial, args.half_life, args.time, args.threshold);
    let radiation = radiation_at_distance(args.initial, args.half_life, args.time, distance);
    println!("Safe distance: {:.2} km (radiation = {:.6} Sv/h)", distance, radiation);
}
