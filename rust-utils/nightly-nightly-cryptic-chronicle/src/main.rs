use clap::{Parser, Subcommand};
use cryptic_chronicle::lib::{encrypt, decrypt};

#[derive(Parser)]
#[command(name = "cryptic-chronicle")]
#[command(about = "Encrypt or decrypt messages with a timestamp", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encrypt a message
    Encrypt {
        /// Secret key
        #[arg(short, long)]
        key: String,
        /// Message to encrypt
        message: String,
    },
    /// Decrypt a message
    Decrypt {
        /// Secret key
        #[arg(short, long)]
        key: String,
        /// Base64 string to decrypt
        ciphertext: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Encrypt { key, message } => {
            let out = encrypt(&message, &key);
            println!("{}", out);
        }
        Commands::Decrypt { key, ciphertext } => match decrypt(&ciphertext, &key) {
            Ok((msg, ts)) => {
                println!("Message: {}", msg);
                println!("Timestamp: {}", ts);
            }
            Err(e) => eprintln!("Error: {}", e),
        },
    }
}
