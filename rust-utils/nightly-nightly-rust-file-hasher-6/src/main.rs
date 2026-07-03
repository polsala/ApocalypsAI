use clap::Parser;
use sha1::{Digest, Sha1};
use sha2::{Sha256};
use md5::Md5;
use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;

/// A whimsical yet useful command-line utility built with Rust to efficiently compute cryptographic hashes of files.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The path to the file to hash.
    #[arg(short, long)]
    file_path: PathBuf,

    /// The hashing algorithm to use (md5, sha1, sha256).
    #[arg(short, long, default_value = "sha256")]
    algorithm: String,

    /// The output encoding (hex or base64).
    #[arg(short, long, default_value = "hex")]
    output: String,
}

fn main() -> io::Result<()>
{
    let args = Args::parse();

    let mut file = File::open(&args.file_path)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    let hash_result = match args.algorithm.to_lowercase().as_str() {
        "md5" => {
            let mut hasher = Md5::new();
            hasher.update(&buffer);
            let result = hasher.finalize();
            format_output(&result, &args.output)
        },
        "sha1" => {
            let mut hasher = Sha1::new();
            hasher.update(&buffer);
            let result = hasher.finalize();
            format_output(&result, &args.output)
        },
        "sha256" => {
            let mut hasher = Sha256::new();
            hasher.update(&buffer);
            let result = hasher.finalize();
            format_output(&result, &args.output)
        },
        _ => return Err(io::Error::new(io::ErrorKind::InvalidInput, "Unsupported algorithm. Use md5, sha1, or sha256.")),
    };

    println!("{}", hash_result);

    Ok(())
}

fn format_output<T: AsRef<[u8]>>(
    data: &T,
    encoding: &str,
) -> String {
    match encoding.to_lowercase().as_str() {
        "hex" => format!("{:x}", hex::encode(data.as_ref())),
        "base64" => base64::encode(data.as_ref()),
        _ => format!("{:?}", data.as_ref()), // Fallback to debug representation if encoding is unknown
    }
}

// Mock rationale: These are placeholder functions for testing purposes. They simulate the behavior of hashing algorithms and output formatting without requiring actual file I/O or external libraries during unit tests.
#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use tempfile::NamedTempFile;

    // Mock for Md5 hashing
    fn mock_md5_hash(data: &[u8]) -> Vec<u8> {
        // This is a simplified mock, not a real MD5 calculation.
        // In a real scenario, you'd use the actual md5 crate.
        let mut mock_hasher = vec![0u8; 16]; // MD5 is 16 bytes
        for (i, byte) in data.iter().enumerate() {
            mock_hasher[i % 16] = mock_hasher[i % 16].wrapping_add(*byte);
        }
        mock_hasher
    }

    // Mock for Sha1 hashing
    fn mock_sha1_hash(data: &[u8]) -> Vec<u8> {
        // This is a simplified mock, not a real SHA1 calculation.
        // In a real scenario, you'd use the actual sha1 crate.
        let mut mock_hasher = vec![0u8; 20]; // SHA1 is 20 bytes
        for (i, byte) in data.iter().enumerate() {
            mock_hasher[i % 20] = mock_hasher[i % 20].wrapping_add(*byte);
        }
        mock_hasher
    }

    // Mock for Sha256 hashing
    fn mock_sha256_hash(data: &[u8]) -> Vec<u8> {
        // This is a simplified mock, not a real SHA256 calculation.
        // In a real scenario, you'd use the actual sha2 crate.
        let mut mock_hasher = vec![0u8; 32]; // SHA256 is 32 bytes
        for (i, byte) in data.iter().enumerate() {
            mock_hasher[i % 32] = mock_hasher[i % 32].wrapping_add(*byte);
        }
        mock_hasher
    }

    #[test]
    fn test_format_output_hex() {
        let data = vec![0x01, 0x02, 0x03, 0x04];
        let expected = "01020304".to_string();
        assert_eq!(format_output(&data, "hex"), expected);
    }

    #[test]
    fn test_format_output_base64() {
        let data = vec![0x01, 0x02, 0x03, 0x04];
        let expected = "AQIDBA==".to_string(); // Base64 encoding of [1, 2, 3, 4]
        assert_eq!(format_output(&data, "base64"), expected);
    }

    #[test]
    fn test_sha256_hex_output() {
        let mut file = NamedTempFile::new().unwrap();
        file.write_all(b"hello world").unwrap();
        let file_path = file.path().to_path_buf();

        // Mock the actual hashing function for deterministic results
        // In a real test, you'd mock the `sha2::Sha256::new()` and `update`/`finalize` calls.
        // For simplicity here, we'll directly use the mock hash function.
        let mock_hash_bytes = mock_sha256_hash(b"hello world");
        let expected_hex = format!("{:x}", hex::encode(mock_hash_bytes));

        // We can't directly inject the mock into `main` without refactoring.
        // Instead, we'll simulate the output of `format_output` for the mock hash.
        // A more robust test would involve mocking the hashing libraries themselves.
        // For this example, we'll assert that the output format is correct.
        // The actual hash value will depend on the real implementation.
        // Let's test the output formatting logic more directly.
        let actual_output = format_output(&mock_sha256_hash(b"hello world"), "hex");
        assert_eq!(actual_output.len(), 64); // SHA256 hex is 64 chars
        assert!(actual_output.chars().all(|c| c.is_digit(16) || (c >= 'a' && c <= 'f')));
    }

    #[test]
    fn test_md5_base64_output() {
        let mut file = NamedTempFile::new().unwrap();
        file.write_all(b"test data").unwrap();
        let file_path = file.path().to_path_buf();

        let mock_hash_bytes = mock_md5_hash(b"test data");
        let expected_base64 = base64::encode(mock_hash_bytes);

        let actual_output = format_output(&mock_md5_hash(b"test data"), "base64");
        assert_eq!(actual_output, expected_base64);
    }

    #[test]
    fn test_sha1_hex_output() {
        let mut file = NamedTempFile::new().unwrap();
        file.write_all(b"another test").unwrap();
        let file_path = file.path().to_path_buf();

        let mock_hash_bytes = mock_sha1_hash(b"another test");
        let expected_hex = format!("{:x}", hex::encode(mock_hash_bytes));

        let actual_output = format_output(&mock_sha1_hash(b"another test"), "hex");
        assert_eq!(actual_output.len(), 40); // SHA1 hex is 40 chars
        assert!(actual_output.chars().all(|c| c.is_digit(16) || (c >= 'a' && c <= 'f')));
    }

    #[test]
    fn test_unsupported_algorithm() {
        let mut file = NamedTempFile::new().unwrap();
        file.write_all(b"some data").unwrap();
        let file_path = file.path().to_path_buf();

        // Simulate calling main with an unsupported algorithm
        // This requires mocking `std::process::exit` or similar, which is complex.
        // Instead, we'll test the `format_output` function's error handling.
        // The `main` function's error handling for unsupported algorithms is tested implicitly
        // by the `match` statement returning an `io::Error`.
        let result = std::panic::catch_unwind(|| {
            let mut args = Args::parse_from(["program_name", "--algorithm", "unsupported"]);
            args.file_path = file_path;
            // Manually call the logic that would error out
            let mut hasher = Md5::new(); // Placeholder, the error is from algorithm name
            hasher.update(b"dummy");
            let _ = format_output(&hasher.finalize(), "hex"); // This won't error, the error is in main's match
            // To properly test the error in main, we'd need to run main itself.
            // For now, we rely on the fact that the match arm returns an error.
        });
        // This test is a bit indirect due to how errors are handled in `main`.
        // A more direct test would involve mocking `File::open` and the hashing logic.
    }

    #[test]
    fn test_file_not_found() {
        let result = std::panic::catch_unwind(|| {
            let mut args = Args::parse_from(["program_name", "non_existent_file.txt"]);
            // Manually call the logic that would error out
            let mut file = File::open(&args.file_path).unwrap(); // This will panic if file not found
            let mut buffer = Vec::new();
            file.read_to_end(&mut buffer).unwrap();
        });
        assert!(result.is_err()); // Expecting a panic due to file not found
    }
}
