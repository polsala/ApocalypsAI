use clap::{Parser, Subcommand};
use nightly_emoji_crypt::{decode, encode};

#[derive(Parser)]
#[command(name = "nightly-emoji-crypt")]
#[command(author = "ApocalypsAI Community")]
#[command(version = "0.1.0")]
#[command(about = "Encode and decode messages as emojis", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encode plain text into emojis
    Encode {
        /// Text to encode (wrap in quotes if it contains spaces)
        text: String,
    },
    /// Decode an emoji string back to plain text
    Decode {
        /// Emoji sequence to decode (wrap in quotes)
        emoji: String,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Encode { text } => {
            let out = encode(&text);
            println!("{}", out);
        }
        Commands::Decode { emoji } => {
            let out = decode(&emoji);
            println!("{}", out);
        }
    }
}
