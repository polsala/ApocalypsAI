use clap::{Parser, Subcommand};
use nightly_cryptic_clipboard::{encrypt, decrypt};

#[derive(Parser)]
#[command(name = "nightly-cryptic-clipboard")]
#[command(about = "XOR encrypt/decrypt text with a passphrase, Base64 output")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encrypt plain text
    Encrypt {
        /// Passphrase
        passphrase: String,
        /// Plain text to encrypt
        text: String,
    },
    /// Decrypt Base64 cipher
    Decrypt {
        /// Passphrase
        passphrase: String,
        /// Base64 encoded cipher
        cipher: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Encrypt { passphrase, text } => {
            let out = encrypt(&passphrase, &text);
            println!("{}", out);
        }
        Commands::Decrypt { passphrase, cipher } => {
            match decrypt(&passphrase, &cipher) {
                Ok(txt) => println!("{}", txt),
                Err(e) => eprintln!("Error: {}", e),
            }
        }
    }
}
