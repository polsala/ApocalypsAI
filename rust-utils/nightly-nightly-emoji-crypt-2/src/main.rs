use clap::{Parser, Subcommand};
use nightly_emoji_crypt::{encode, decode};

#[derive(Parser)]
#[command(name = "nightly-emoji-crypt")]
#[command(about = "Encode/decode text to emojis", version)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Encode {
        #[arg(value_name = "TEXT")]
        text: String,
    },
    Decode {
        #[arg(value_name = "EMOJI")]
        emoji: String,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Encode { text } => {
            println!("{}", encode(&text));
        }
        Commands::Decode { emoji } => {
            println!("{}", decode(&emoji));
        }
    }
}
