use clap::{Parser, ValueEnum};

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
pub struct Args {
    /// Description of the temporal anomaly
    #[arg(short, long)]
    pub description: String,

    /// Type of the anomaly (e.g., Echo, Warp, Flicker, Loop)
    #[arg(short, long, value_enum)]
    pub anomaly_type: AnomalyType,

    /// Severity of the anomaly (e.g., Trivial, Minor, Moderate, Severe, Critical)
    #[arg(short, long, value_enum)]
    pub severity: Severity,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum, Debug)]
pub enum AnomalyType {
    Echo,
    Warp,
    Flicker,
    Loop,
    Glitch,
    Phantom,
    Shift,
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum, Debug)]
pub enum Severity {
    Trivial,
    Minor,
    Moderate,
    Severe,
    Critical,
}

/// Generates a formatted tag for a temporal anomaly.
pub fn tag_anomaly(description: &str, anomaly_type: AnomalyType, severity: Severity) -> String {
    format!("[ANOMALY:{:?}|{:?}] {}", anomaly_type, severity, description)
}

fn main() {
    let args = Args::parse();
    let tag = tag_anomaly(&args.description, args.anomaly_type, args.severity);
    println!("{}", tag);
}
