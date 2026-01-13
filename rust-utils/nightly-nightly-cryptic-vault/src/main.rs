use clap::{Parser, Subcommand};
use aes_gcm::{Aes256Gcm, Key, Nonce};
use aes_gcm::aead::{Aead, NewAead};
use sha2::{Digest, Sha256};
use rand::RngCore;
use std::fs;
use std::io::{self, Read, Write};

/// Simple CLI for encrypting and decrypting text with a passphrase.
#[derive(Parser)]
#[command(name = "cryptic-vault")]
#[command(author = "ApocalypsAI")]
#[command(version = "0.1.0")]
#[command(about = "Encrypt or decrypt a secret string", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Encrypt text and write to a file.
    Encrypt {
        /// Passphrase used to derive the encryption key.
        #[arg(long)]
        passphrase: String,
        /// Text to encrypt. If omitted, reads from stdin.
        #[arg(short, long)]
        input: Option<String>,
        /// Output file (default: vault.bin)
        #[arg(short, long, default_value = "vault.bin")]
        output: String,
    },
    /// Decrypt a file and print the plaintext.
    Decrypt {
        /// Passphrase used to derive the encryption key.
        #[arg(long)]
        passphrase: String,
        /// Input file (default: vault.bin)
        #[arg(short, long, default_value = "vault.bin")]
        input: String,
    },
}

fn derive_key(passphrase: &str) -> Key<aes_gcm::aead::generic_array::typenum::U32> {
    let hash = Sha256::digest(passphrase.as_bytes());
    Key::from_slice(&hash).clone()
}

fn encrypt(plain: &[u8], key: &Key<aes_gcm::aead::generic_array::typenum::U32>) -> (Vec<u8>, Vec<u8>) {
    let cipher = Aes256Gcm::new(key);
    let mut nonce_bytes = [0u8; 12];
    rand::thread_rng().fill_bytes(&mut nonce_bytes);
    let nonce = Nonce::from_slice(&nonce_bytes);
    let ciphertext = cipher.encrypt(nonce, plain).expect("encryption failure");
    (nonce_bytes.to_vec(), ciphertext)
}

fn decrypt(nonce: &[u8], ciphertext: &[u8], key: &Key<aes_gcm::aead::generic_array::typenum::U32>) -> Vec<u8> {
    let cipher = Aes256Gcm::new(key);
    let nonce = Nonce::from_slice(nonce);
    cipher.decrypt(nonce, ciphertext).expect("decryption failure")
}

fn main() -> io::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Encrypt { passphrase, input, output } => {
            let mut data = Vec::new();
            if let Some(txt) = input {
                data.extend_from_slice(txt.as_bytes());
            } else {
                io::stdin().read_to_end(&mut data)?;
            }
            let key = derive_key(&passphrase);
            let (nonce, ciphertext) = encrypt(&data, &key);
            let mut file = fs::File::create(&output)?;
            file.write_all(&nonce)?;
            file.write_all(&ciphertext)?;
            eprintln!("Encrypted data written to {}", output);
        }
        Commands::Decrypt { passphrase, input } => {
            let mut file = fs::File::open(&input)?;
            let mut contents = Vec::new();
            file.read_to_end(&mut contents)?;
            if contents.len() < 12 {
                eprintln!("File too short to contain nonce");
                std::process::exit(1);
            }
            let (nonce, ciphertext) = contents.split_at(12);
            let key = derive_key(&passphrase);
            let plaintext = decrypt(nonce, ciphertext, &key);
            io::stdout().write_all(&plaintext)?;
        }
    }

    Ok(())
}

