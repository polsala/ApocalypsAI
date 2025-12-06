use clap::{Parser, Subcommand};
use sha2::{Digest, Sha256};
use std::fs;
use std::io::{self, Read, Write};
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance CLI tool to checksum, whimsically scramble, and verify digital 'relic' files, ensuring their integrity in a chaotic world.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Computes the SHA256 checksum of a file.
    Checksum {
        /// The path to the file to checksum.
        #[arg(short, long)]
        file: PathBuf,
    },
    /// Whimsically scrambles a file using a simple XOR cipher with a given key.
    Scramble {
        /// The path to the input file.
        #[arg(short, long)]
        input: PathBuf,
        /// The path to the output scrambled file.
        #[arg(short, long)]
        output: PathBuf,
        /// The 'temporal frequency' key for scrambling.
        #[arg(short, long)]
        key: String,
    },
    /// Unscrambles a file using the same 'temporal frequency' key.
    Unscramble {
        /// The path to the input scrambled file.
        #[arg(short, long)]
        input: PathBuf,
        /// The path to the output unscrambled file.
        #[arg(short, long)]
        output: PathBuf,
        /// The 'temporal frequency' key used for scrambling.
        #[arg(short, long)]
        key: String,
    },
    /// Verifies a scrambled file against its original SHA256 hash using the 'temporal frequency' key.
    Verify {
        /// The path to the scrambled file.
        #[arg(short, long)]
        scrambled_file: PathBuf,
        /// The expected SHA256 hash of the *original* unscrambled file.
        #[arg(short, long)]
        original_hash: String,
        /// The 'temporal frequency' key used for scrambling.
        #[arg(short, long)]
        key: String,
    },
}

fn calculate_sha256_from_path(path: &PathBuf) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

fn xor_transform_files(input_path: &PathBuf, output_path: &PathBuf, key: &str) -> io::Result<()> {
    let input_bytes = fs::read(input_path)?;
    let key_bytes = key.as_bytes();
    if key_bytes.is_empty() {
        return Err(io::Error::new(io::ErrorKind::InvalidInput, "Key cannot be empty"));
    }

    let transformed_bytes: Vec<u8> = input_bytes
        .iter()
        .enumerate()
        .map(|(i, &byte)| byte ^ key_bytes[i % key_bytes.len()])
        .collect();

    fs::write(output_path, transformed_bytes)?;
    Ok(())
}

fn main() -> io::Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Checksum { file } => {
            let hash = calculate_sha256_from_path(file)?;
            println!("SHA256 of {}: {}", file.display(), hash);
        }
        Commands::Scramble { input, output, key } => {
            xor_transform_files(input, output, key)?;
            println!("File '{}' scrambled to '{}' with key.", input.display(), output.display());
        }
        Commands::Unscramble { input, output, key } => {
            xor_transform_files(input, output, key)?;
            println!("File '{}' unscrambled to '{}' with key.", input.display(), output.display());
        }
        Commands::Verify { scrambled_file, original_hash, key } => {
            let temp_unscrambled_path = scrambled_file.with_extension("unscrambled.tmp");
            xor_transform_files(scrambled_file, &temp_unscrambled_path, key)?;
            let actual_unscrambled_hash = calculate_sha256_from_path(&temp_unscrambled_path)?;
            fs::remove_file(&temp_unscrambled_path)?; // Clean up temp file

            if actual_unscrambled_hash == *original_hash {
                println!("Verification successful! Original content hash matches.");
            } else {
                eprintln!("Verification FAILED! Expected hash: {}, Actual hash: {}", original_hash, actual_unscrambled_hash);
                std::process::exit(1);
            }
        }
    }
    Ok(())
}
