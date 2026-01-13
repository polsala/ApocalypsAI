use clap::{Parser, Subcommand};

/// Simple duration converter
#[derive(Parser)]
#[command(name = "chrono-converter")]
#[command(author = "ApocalypsAI Nightly")]
#[command(version = "0.1.0")]
#[command(about = "Convert between duration strings and seconds")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Convert a duration string like 1d2h3m4s to total seconds
    ToSeconds {
        /// Duration string
        #[arg(value_name = "DURATION")]
        duration: String,
    },
    /// Convert total seconds to a duration string
    FromSeconds {
        /// Number of seconds
        #[arg(value_name = "SECONDS")]
        seconds: u64,
    },
}

fn parse_duration(s: &str) -> Result<u64, String> {
    let mut total = 0u64;
    let mut num = String::new();
    for ch in s.chars() {
        if ch.is_ascii_digit() {
            num.push(ch);
        } else {
            let value: u64 = num.parse().map_err(|_| format!("Invalid number '{}'", num))?;
            match ch {
                'd' => total += value * 86400,
                'h' => total += value * 3600,
                'm' => total += value * 60,
                's' => total += value,
                _ => return Err(format!("Unknown unit '{}'", ch)),
            }
            num.clear();
        }
    }
    if !num.is_empty() {
        return Err("Trailing number without unit".into());
    }
    Ok(total)
}

fn format_duration(mut secs: u64) -> String {
    let days = secs / 86400;
    secs %= 86400;
    let hours = secs / 3600;
    secs %= 3600;
    let minutes = secs / 60;
    secs %= 60;
    let seconds = secs;
    let mut parts = Vec::new();
    if days > 0 {
        parts.push(format!("{}d", days));
    }
    if hours > 0 {
        parts.push(format!("{}h", hours));
    }
    if minutes > 0 {
        parts.push(format!("{}m", minutes));
    }
    if seconds > 0 || parts.is_empty() {
        parts.push(format!("{}s", seconds));
    }
    parts.concat()
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::ToSeconds { duration } => {
            match parse_duration(&duration) {
                Ok(sec) => println!("{}", sec),
                Err(e) => {
                    eprintln!("Error: {}", e);
                    std::process::exit(1);
                }
            }
        }
        Commands::FromSeconds { seconds } => {
            let out = format_duration(seconds);
            println!("{}", out);
        }
    }
}

