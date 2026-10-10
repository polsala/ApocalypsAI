use clap::{Arg, Command};
use sha2::{Sha256, Sha512};
use md5::Md5;
use sha1::Sha1;
use std::fs::File;
use std::io::{self, Read};
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::thread;

// Mock rationale: Using a fixed buffer size for reading files to simulate I/O operations.
const BUFFER_SIZE: usize = 8192;

// Enum to represent the different hashing algorithms supported.
#[derive(Debug, Clone, Copy)]
enum HashAlgorithm {
    Md5,
    Sha1,
    Sha256,
    Sha512,
}

impl HashAlgorithm {
    fn from_str(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "md5" => Some(HashAlgorithm::Md5),
            "sha1" => Some(HashAlgorithm::Sha1),
            "sha256" => Some(HashAlgorithm::Sha256),
            "sha512" => Some(HashAlgorithm::Sha512),
            _ => None,
        }
    }

    fn name(&self) -> &'static str {
        match self {
            HashAlgorithm::Md5 => "md5",
            HashAlgorithm::Sha1 => "sha1",
            HashAlgorithm::Sha256 => "sha256",
            HashAlgorithm::Sha512 => "sha512",
        }
    }
}

// Function to compute a single hash for a given file and algorithm.
fn compute_hash_single_thread<P: AsRef<Path>>(file_path: P, algorithm: HashAlgorithm) -> io::Result<String> {
    let mut file = File::open(file_path)?;
    let mut buffer = vec![0u8; BUFFER_SIZE];

    match algorithm {
        HashAlgorithm::Md5 => {
            let mut hasher = Md5::new();
            loop {
                let bytes_read = file.read(&mut buffer)?;
                if bytes_read == 0 { break; }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
        HashAlgorithm::Sha1 => {
            let mut hasher = Sha1::new();
            loop {
                let bytes_read = file.read(&mut buffer)?;
                if bytes_read == 0 { break; }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
        HashAlgorithm::Sha256 => {
            let mut hasher = Sha256::new();
            loop {
                let bytes_read = file.read(&mut buffer)?;
                if bytes_read == 0 { break; }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
        HashAlgorithm::Sha512 => {
            let mut hasher = Sha512::new();
            loop {
                let bytes_read = file.read(&mut buffer)?;
                if bytes_read == 0 { break; }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
    }
}

// Function to compute hash in parallel (simplified for demonstration).
// In a real-world scenario, this would involve more sophisticated chunking and thread management.
fn compute_hash_parallel<P: AsRef<Path>>(file_path: P, algorithm: HashAlgorithm) -> io::Result<String> {
    let file_path = Arc::new(file_path.as_ref().to_path_buf());
    let num_threads = num_cpus::get(); // Get number of logical cores
    let mut handles = vec![];

    // Mock rationale: For simplicity, we'll simulate parallel processing by having each thread read the entire file.
    // A more robust implementation would divide the file into chunks.
    for _ in 0..num_threads {
        let file_path_clone = Arc::clone(&file_path);
        let algorithm_clone = algorithm;

        let handle = thread::spawn(move || {
            // In a real parallel scenario, each thread would process a chunk.
            // Here, we just call the single-threaded function for demonstration.
            compute_hash_single_thread(file_path_clone, algorithm_clone)
        });
        handles.push(handle);
    }

    let mut final_hasher = match algorithm {
        HashAlgorithm::Md5 => Box::new(Md5::new()) as Box<dyn crypto::digest::Digest>,
        HashAlgorithm::Sha1 => Box::new(Sha1::new()) as Box<dyn crypto::digest::Digest>,
        HashAlgorithm::Sha256 => Box::new(Sha256::new()) as Box<dyn crypto::digest::Digest>,
        HashAlgorithm::Sha512 => Box::new(Sha512::new()) as Box<dyn crypto::digest::Digest>,
    };

    for handle in handles {
        match handle.join() {
            Ok(Ok(hash_str)) => {
                // This is a simplification. In a true parallel hash, you'd need to combine partial hashes.
                // For this example, we'll just use the first computed hash as the result.
                // A more correct approach would involve hashing the concatenated results of partial hashes.
                // For demonstration purposes, we'll just return the first valid hash.
                return Ok(hash_str);
            }
            Ok(Err(e)) => return Err(e),
            Err(_) => return Err(io::Error::new(io::ErrorKind::Other, "Thread panicked"))
        }
    }

    // Fallback if no threads completed successfully (should not happen with valid file)
    Err(io::Error::new(io::ErrorKind::NotFound, "Could not compute hash in parallel"))
}

fn main() -> io::Result<()> {
    let matches = Command::new("nightly-rust-file-hasher")
        .version("1.0")
        .author("ApocalypsAI Integrator")
        .about("Computes cryptographic hashes for files.")
        .arg(Arg::new("file_path")
            .help("The path to the file to hash")
            .required(true))
        .arg(Arg::new("algorithm")
            .short('a')
            .long("algorithm")
            .help("Hashing algorithm (md5, sha1, sha256, sha512)")
            .default_value("sha256"))
        .arg(Arg::new("parallel")
            .short('p')
            .long("parallel")
            .help("Enable parallel processing for large files"))
        .get_matches();

    let file_path = matches.get_one::<String>("file_path").unwrap();
    let algorithm_str = matches.get_one::<String>("algorithm").unwrap();
    let is_parallel = matches.get_flag("parallel");

    let algorithm = HashAlgorithm::from_str(algorithm_str)
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Unsupported algorithm"))?;

    let hash_result = if is_parallel {
        compute_hash_parallel(file_path, algorithm)?
    } else {
        compute_hash_single_thread(file_path, algorithm)?
    };

    println!("Algorithm: {}", algorithm.name());
    println!("File: {}", file_path);
    println!("Hash: {}", hash_result);

    Ok(())
}
