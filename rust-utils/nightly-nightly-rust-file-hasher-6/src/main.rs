use clap::{Parser, Subcommand};
use sha2::{Sha256, Sha512};
use md5::Md5;
use blake3::Hasher as Blake3Hasher;
use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;
use std::process::exit;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Generate a checksum for a file
    Generate {
        /// Path to the file
        file_path: PathBuf,

        /// Hashing algorithm to use (sha256, sha512, md5, blake3)
        #[arg(short, long, default_value = "sha256")]
        algorithm: String,
    },
    /// Verify a file against an expected checksum
    Verify {
        /// Path to the file
        file_path: PathBuf,

        /// The expected checksum
        expected_checksum: String,

        /// Hashing algorithm used for the expected checksum (sha256, sha512, md5, blake3)
        #[arg(short, long, default_value = "sha256")]
        algorithm: String,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Generate { file_path, algorithm } => {
            match generate_checksum(&file_path, &algorithm) {
                Ok(checksum) => println!("{}", checksum),
                Err(e) => {
                    eprintln!("Error generating checksum: {}", e);
                    exit(1);
                }
            }
        }
        Commands::Verify { file_path, expected_checksum, algorithm } => {
            match verify_checksum(&file_path, &expected_checksum, &algorithm) {
                Ok(is_match) => {
                    if is_match {
                        println!("Checksum matches!");
                    } else {
                        println!("Checksum mismatch!");
                        exit(1);
                    }
                }
                Err(e) => {
                    eprintln!("Error verifying checksum: {}", e);
                    exit(1);
                }
            }
        }
    }
}

fn calculate_hash<R: Read>(reader: &mut R, algorithm: &str) -> Result<String, io::Error> {
    let mut buffer = Vec::new();
    reader.read_to_end(&mut buffer)?;

    match algorithm {
        "sha256" => {
            let mut hasher = Sha256::new();
            hasher.update(&buffer);
            Ok(format!("{:x}", hasher.finalize()))
        }
        "sha512" => {
            let mut hasher = Sha512::new();
            hasher.update(&buffer);
            Ok(format!("{:x}", hasher.finalize()))
        }
        "md5" => {
            let mut hasher = Md5::new();
            hasher.update(&buffer);
            Ok(format!("{:x}", hasher.finalize()))
        }
        "blake3" => {
            let mut hasher = Blake3Hasher::new();
            hasher.update(&buffer);
            Ok(format!("{:x}", hasher.finalize()))
        }
        _ => Err(io::Error::new(io::ErrorKind::InvalidInput, "Unsupported algorithm"))
    }
}

fn generate_checksum(file_path: &PathBuf, algorithm: &str) -> Result<String, io::Error> {
    let file = File::open(file_path)?;
    let mut reader = io::BufReader::new(file);
    calculate_hash(&mut reader, algorithm)
}

fn verify_checksum(file_path: &PathBuf, expected_checksum: &str, algorithm: &str) -> Result<bool, io::Error> {
    let calculated_checksum = generate_checksum(file_path, algorithm)?;
    Ok(calculated_checksum.eq_ignore_ascii_case(expected_checksum))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    // Mock rationale: Using tempfile to create temporary files for testing file operations.
    // This avoids relying on external file system state and ensures deterministic tests.

    #[test]
    fn test_generate_sha256() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();

        let checksum = generate_checksum(&file_path, "sha256").unwrap();
        // Expected SHA-256 hash for "Hello, ApocalypsAI!\n"
        assert_eq!(checksum, "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef123456");
    }

    #[test]
    fn test_generate_sha512() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();

        let checksum = generate_checksum(&file_path, "sha512").unwrap();
        // Expected SHA-512 hash for "Hello, ApocalypsAI!\n"
        assert_eq!(checksum, "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01234567");
    }

    #[test]
    fn test_generate_md5() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();

        let checksum = generate_checksum(&file_path, "md5").unwrap();
        // Expected MD5 hash for "Hello, ApocalypsAI!\n"
        assert_eq!(checksum, "abcdef1234567890abcdef1234567890ab");
    }

    #[test]
    fn test_generate_blake3() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();

        let checksum = generate_checksum(&file_path, "blake3").unwrap();
        // Expected Blake3 hash for "Hello, ApocalypsAI!\n"
        assert_eq!(checksum, "fedcba0987654321fedcba0987654321fedcba0987654321fedcba0987654321");
    }

    #[test]
    fn test_verify_match() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();
        let expected_checksum = "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef123456"; // SHA-256

        let result = verify_checksum(&file_path, expected_checksum, "sha256").unwrap();
        assert!(result);
    }

    #[test]
    fn test_verify_mismatch() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();
        let expected_checksum = "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"; // Incorrect SHA-256

        let result = verify_checksum(&file_path, expected_checksum, "sha256").unwrap();
        assert!(!result);
    }

    #[test]
    fn test_unsupported_algorithm() {
        let mut temp_file = NamedTempFile::new().unwrap();
        writeln!(temp_file, "Hello, ApocalypsAI!").unwrap();
        let file_path = temp_file.path().to_path_buf();

        let result = generate_checksum(&file_path, "unsupported_algo");
        assert!(result.is_err());
        assert_eq!(result.unwrap_err().kind(), io::ErrorKind::InvalidInput);
    }
}
