use clap::{Parser, Subcommand};
use emoji_crypt::{decode, encode};

#[derive(Parser)]
#[command(name = "emoji-crypt")]
#[command(about = "Encode/decode text to emojis", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encode plain text to an emoji sequence
    Encode {
        /// Text to encode
        text: String,
    },
    /// Decode an emoji sequence back to plain text
    Decode {
        /// Emoji sequence
        emojis: String,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Encode { text } => {
            let out = encode(&text);
            println!("{}", out);
        }
        Commands::Decode { emojis } => match decode(&emojis) {
            Ok(s) => println!("{}", s),
            Err(e) => eprintln!("Error: {}", e),
        },
    }
}
