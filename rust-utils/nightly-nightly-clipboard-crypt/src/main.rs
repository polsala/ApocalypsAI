use clap::{Parser, Subcommand};
use clipboard::{ClipboardContext, ClipboardProvider};
use base64::{engine::general_purpose, Engine as _};

/// Simple XOR cipher that repeats the key.
fn xor(data: &[u8], key: &[u8]) -> Vec<u8> {
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key.len()])
        .collect()
}

/// Encrypt plaintext with passphrase, returning Base64 string.
fn encrypt(plaintext: &str, passphrase: &str) -> String {
    let key = passphrase.as_bytes();
    let cipher_bytes = xor(plaintext.as_bytes(), key);
    general_purpose::STANDARD.encode(&cipher_bytes)
}

/// Decrypt Base64 cipher text with passphrase, returning plaintext.
fn decrypt(ciphertext_b64: &str, passphrase: &str) -> Result<String, String> {
    let cipher_bytes = general_purpose::STANDARD
        .decode(ciphertext_b64)
        .map_err(|e| format!("Base64 decode error: {}", e))?;
    let key = passphrase.as_bytes();
    let plain_bytes = xor(&cipher_bytes, key);
    String::from_utf8(plain_bytes).map_err(|e| format!("UTF-8 error: {}", e))
}

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encrypt the current clipboard contents
    Encrypt {
        /// Passphrase to use
        passphrase: String,
    },
    /// Decrypt the current clipboard contents (expects Base64)
    Decrypt {
        /// Passphrase to use
        passphrase: String,
    },
}

fn main() {
    let cli = Cli::parse();

    // Obtain clipboard content
    let mut ctx: ClipboardContext = ClipboardProvider::new().expect("Failed to access clipboard");
    let clipboard_content = ctx.get_contents().unwrap_or_default();

    match cli.command {
        Commands::Encrypt { passphrase } => {
            let encrypted = encrypt(&clipboard_content, &passphrase);
            ctx.set_contents(encrypted.clone()).expect("Failed to set clipboard");
            println!("{}", encrypted);
        }
        Commands::Decrypt { passphrase } => {
            match decrypt(&clipboard_content, &passphrase) {
                Ok(plain) => {
                    ctx.set_contents(plain.clone()).expect("Failed to set clipboard");
                    println!("{}", plain);
                }
                Err(e) => eprintln!("Error: {}", e),
            }
        }
    }
}
