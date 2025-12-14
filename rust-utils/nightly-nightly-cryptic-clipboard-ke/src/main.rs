use clap::{Parser, Subcommand};
use base64::{engine::general_purpose, Engine as _};

/// Simple XOR cipher with repeating key
fn xor(data: &[u8], key: &[u8]) -> Vec<u8> {
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key.len()])
        .collect()
}

#[derive(Parser)]
#[command(name = "nightly-cryptic-clipboard-keeper")]
#[command(about = "Encrypt or decrypt text via XOR + Base64", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encrypt plaintext from stdin using passphrase
    Encrypt {
        /// Passphrase
        passphrase: String,
    },
    /// Decrypt Base64 ciphertext from stdin using passphrase
    Decrypt {
        /// Passphrase
        passphrase: String,
    },
}

fn main() {
    let cli = Cli::parse();

    // Read all stdin
    let mut input = String::new();
    std::io::Read::read_to_string(&mut std::io::stdin(), &mut input).expect("Failed to read stdin");
    let input = input.trim_end(); // remove trailing newline

    match cli.command {
        Commands::Encrypt { passphrase } => {
            let encrypted = xor(input.as_bytes(), passphrase.as_bytes());
            let encoded = general_purpose::STANDARD.encode(&encrypted);
            println!("{}", encoded);
        }
        Commands::Decrypt { passphrase } => {
            let decoded = match general_purpose::STANDARD.decode(input) {
                Ok(d) => d,
                Err(_) => {
                    eprintln!("Invalid Base64 input");
                    std::process::exit(1);
                }
            };
            let decrypted = xor(&decoded, passphrase.as_bytes());
            match String::from_utf8(decrypted) {
                Ok(s) => println!("{}", s),
                Err(_) => {
                    eprintln!("Decryption produced invalid UTF-8");
                    std::process::exit(1);
                }
            }
        }
    }
}

// Exported for tests
pub fn encrypt(plaintext: &str, passphrase: &str) -> String {
    let encrypted = xor(plaintext.as_bytes(), passphrase.as_bytes());
    general_purpose::STANDARD.encode(&encrypted)
}

pub fn decrypt(ciphertext: &str, passphrase: &str) -> Result<String, String> {
    let decoded = general_purpose::STANDARD
        .decode(ciphertext)
        .map_err(|e| format!("Base64 decode error: {}", e))?;
    let decrypted = xor(&decoded, passphrase.as_bytes());
    String::from_utf8(decrypted).map_err(|e| format!("UTF-8 error: {}", e))
}
