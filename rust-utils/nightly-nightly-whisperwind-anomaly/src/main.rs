use clap::Parser;
use colored::*;
use std::io::{self, BufRead};
use std::fs::File;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about = "Detects and classifies environmental anomalies.", long_about = None)]
struct Args {
    /// Input file to read environmental data from. If not specified, reads from stdin.
    #[arg(short, long)]
    file: Option<PathBuf>,
}

enum Anomaly {
    HarmlessRustle,
    CuriousGust,
    OminousHowl,
    CataclysmicRoar,
    UnintelligibleStatic,
}

impl Anomaly {
    fn classify(reading: f64) -> Anomaly {
        if reading >= 0.0 && reading <= 0.2 {
            Anomaly::HarmlessRustle
        } else if reading > 0.2 && reading <= 0.5 {
            Anomaly::CuriousGust
        } else if reading > 0.5 && reading <= 1.0 {
            Anomaly::OminousHowl
        } else if reading > 1.0 {
            Anomaly::CataclysmicRoar
        } else {
            Anomaly::UnintelligibleStatic // For negative values or other unexpected floats
        }
    }

    fn display(&self) -> ColoredString {
        match self {
            Anomaly::HarmlessRustle => "Harmless Rustle".green(),
            Anomaly::CuriousGust => "Curious Gust".yellow(),
            Anomaly::OminousHowl => "Ominous Howl".red(),
            Anomaly::CataclysmicRoar => "Cataclysmic Roar!".magenta().bold(),
            Anomaly::UnintelligibleStatic => "Unintelligible Static".dimmed(),
        }
    }
}

fn process_line(line: &str) {
    match line.trim().parse::<f64>() {
        Ok(reading) => {
            let anomaly = Anomaly::classify(reading);
            println!("Reading: {:<8.4} -> {}", reading, anomaly.display());
        }
        Err(_) => {
            println!("Reading: {:<8} -> {}", line.trim(), Anomaly::UnintelligibleStatic.display());
        }
    }
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    match args.file {
        Some(path) => {
            let file = File::open(&path)?;
            let reader = io::BufReader::new(file);
            for line in reader.lines() {
                process_line(&line?);
            }
        }
        None => {
            let stdin = io::stdin();
            let reader = stdin.lock();
            for line in reader.lines() {
                process_line(&line?);
            }
        }
    }
    Ok(())
}
