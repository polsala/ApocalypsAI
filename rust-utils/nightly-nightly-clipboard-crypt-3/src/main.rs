use std::io::{self, Read};
use clap::{Parser, ArgAction};
use base64::{engine::general_purpose, Engine as _};

/// Simple XOR cipher that repeats the passphrase over the data.
fn xor_cipher(data: &[u8], pass: &[u8]) -> Vec<u8> {
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ pass[i % pass.len()])
        .collect()
}

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Encrypt mode (default is decrypt if not set)
    #[arg(short, long, action = ArgAction::SetTrue)]
    encrypt: bool,

    /// Decrypt mode
    #[arg(short, long, action = ArgAction::SetTrue)]
    decrypt: bool,

    /// Passphrase for XOR cipher
    #[arg(short, long)]
    pass: String,
}

fn main() {
    let args = Args::parse();
    let mode_encrypt = args.encrypt || (!args.encrypt && !args.decrypt);
    // If both flags are set, encrypt takes precedence.

    // Read all stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read stdin");
    let pass_bytes = args.pass.as_bytes();

    if mode_encrypt {
        // Encrypt: XOR then Base64 encode
        let cipher_bytes = xor_cipher(input.as_bytes(), pass_bytes);
        let encoded = general_purpose::STANDARD.encode(&cipher_bytes);
        println!("{}", encoded);
    } else {
        // Decrypt: Base64 decode then XOR
        let decoded = general_purpose::STANDARD
            .decode(input.trim())
            .expect("Invalid Base64 input");
        let plain_bytes = xor_cipher(&decoded, pass_bytes);
        let plain = String::from_utf8(plain_bytes).expect("Decrypted data is not valid UTF-8");
        println!("{}", plain);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_xor_roundtrip() {
        let data = b"The quick brown fox jumps over the lazy dog";
        let pass = b"s3cr3t";
        let encrypted = xor_cipher(data, pass);
        let decrypted = xor_cipher(&encrypted, pass);
        assert_eq!(data.to_vec(), decrypted);
    }
}
