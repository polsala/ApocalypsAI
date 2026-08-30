use clap::{Parser, Subcommand};
use nightly_emoji_mood_tracker::{add_entry, stats};

#[derive(Parser)]
#[command(name = "nightly-emoji-mood-tracker")]
#[command(about = "Log moods with emojis and view stats", version)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add a mood entry
    Add {
        /// Emoji representing the mood
        emoji: String,
        /// Optional note
        #[arg(short, long)]
        note: Option<String>,
    },
    /// Show statistics
    Stats,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Add { emoji, note } => {
            if let Err(e) = add_entry(&emoji, note.as_deref()) {
                eprintln!("Failed to add entry: {}", e);
                std::process::exit(1);
            } else {
                println!("Mood entry added.");
            }
        }
        Commands::Stats => {
            match stats() {
                Ok(map) => {
                    println!("Mood statistics:");
                    for (emoji, count) in map {
                        println!("{} : {}", emoji, count);
                    }
                }
                Err(e) => {
                    eprintln!("Failed to compute stats: {}", e);
                    std::process::exit(1);
                }
            }
        }
    }
}
