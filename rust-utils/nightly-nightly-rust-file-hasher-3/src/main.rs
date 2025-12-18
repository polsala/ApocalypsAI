use std::env;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;

// Import hashing algorithms from the 'sha2' and 'md-5' crates.
// Note: 'md-5' is a separate crate for MD5, as it's not in the standard Rust crypto libraries.
use sha2::{Digest, Sha256, Sha512};
use md5::Md5;

// Define a trait for hashing to abstract over different algorithms.
trait Hasher {
    fn update(&mut self, data: &[u8]);
    fn finalize(self) -> Vec<u8>;
    fn name(&self) -> &'static str;
}

// Implement the Hasher trait for Sha256.
impl Hasher for Sha256 {
    fn update(&mut self, data: &[u8]) {
        Digest::update(self, data);
    }

    fn finalize(self) -> Vec<u8> {
        Digest::finalize(self).to_vec()
    }

    fn name(&self) -> &'static str {
        "sha256"
    }
}

// Implement the Hasher trait for Sha512.
impl Hasher for Sha512 {
    fn update(&mut self, data: &[u8]) {
        Digest::update(self, data);
    }

    fn finalize(self) -> Vec<u8> {
        Digest::finalize(self).to_vec()
    }

    fn name(&self) -> &'static str {
        "sha512"
    }
}

// Implement the Hasher trait for Md5.
impl Hasher for Md5 {
    fn update(&mut self, data: &[u8]) {
        Digest::update(self, data);
    }

    fn finalize(self) -> Vec<u8> {
        Digest::finalize(self).to_vec()
    }

    fn name(&self) -> &'static str {
        "md5"
    }
}

// Function to read a file into a byte vector.
fn read_file_bytes<P: AsRef<Path>>(filepath: P) -> io::Result<Vec<u8>> {
    let mut file = File::open(filepath)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;
    Ok(buffer)
}

// Function to compute the hash of a file using a generic Hasher.
fn compute_hash<H: Hasher + Default>(file_bytes: &[u8]) -> Vec<u8> {
    let mut hasher = H::default();
    hasher.update(file_bytes);
    hasher.finalize()
}

// Function to convert a byte vector to a hexadecimal string.
fn to_hex_string(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{:02x}", b)).collect()
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();

    if args.len() != 3 {
        eprintln!("Usage: nightly-rust-file-hasher <algorithm> <file_path>");
        eprintln!("Supported algorithms: md5, sha1, sha256, sha512");
        std::process::exit(1);
    }

    let algorithm = &args[1];
    let file_path = &args[2];

    let file_bytes = read_file_bytes(file_path)?;

    let hash_result = match algorithm.as_str() {
        "md5" => {
            let mut hasher = Md5::new();
            hasher.update(&file_bytes);
            to_hex_string(&hasher.finalize())
        }
        "sha1" => {
            // SHA1 is not directly implemented in the sha2 crate, and is generally discouraged.
            // For this example, we'll return an error or a placeholder.
            // In a real-world scenario, you'd add a 'sha1' crate.
            eprintln!("SHA1 is not supported in this version. Please use md5, sha256, or sha512.");
            std::process::exit(1);
        }
        "sha256" => {
            let mut hasher = Sha256::new();
            hasher.update(&file_bytes);
            to_hex_string(&hasher.finalize())
        }
        "sha512" => {
            let mut hasher = Sha512::new();
            hasher.update(&file_bytes);
            to_hex_string(&hasher.finalize())
        }
        _ => {
            eprintln!("Unsupported algorithm: {}", algorithm);
            eprintln!("Supported algorithms: md5, sha1, sha256, sha512");
            std::process::exit(1);
        }
    };

    println!("{}", hash_result);

    Ok(())
}
