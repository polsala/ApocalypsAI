use clap::Parser;
use sha1::Sha1;
use sha2::{Sha256, Sha512};
use md5::Md5;
use hex_literal::Literal;
use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;
use digest::{Digest, Output};

/// A whimsical yet useful command-line utility written in Rust for generating cryptographic hashes of files.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The hashing algorithm to use (md5, sha1, sha256, sha512).
    #[arg(short, long)]
    algorithm: String,

    /// The path to the file to hash.
    #[arg(short, long)]
    file_path: PathBuf,
}

fn calculate_hash<D: Digest>(mut reader: impl Read) -> io::Result<Output<D>> {
    let mut hasher = D::new();
    let mut buffer = [0u8; 4096]; // Process in chunks

    loop {
        let bytes_read = reader.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(hasher.finalize())
}

fn main() -> io::Result<()>
{
    let args = Args::parse();

    let mut file = File::open(&args.file_path)?;

    let hash_result = match args.algorithm.to_lowercase().as_str() {
        "md5" => {
            let hash_bytes = calculate_hash::<Md5>(file)?;
            format!("{:x}", hash_bytes)
        }
        "sha1" => {
            let hash_bytes = calculate_hash::<Sha1>(file)?;
            format!("{:x}", hash_bytes)
        }
        "sha256" => {
            let hash_bytes = calculate_hash::<Sha256>(file)?;
            format!("{:x}", hash_bytes)
        }
        "sha512" => {
            let hash_bytes = calculate_hash::<Sha512>(file)?;
            format!("{:x}", hash_bytes)
        }
        _ => {
            eprintln!("Error: Unsupported algorithm '{}'. Supported algorithms are md5, sha1, sha256, sha512.", args.algorithm);
            std::process::exit(1);
        }
    };

    println!("{}", hash_result);

    Ok(())
}
