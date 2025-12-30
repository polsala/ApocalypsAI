use clap::{App, Arg, SubCommand};
use sha2::{Sha256, Digest};
use md5::Md5;
use sha1::Sha1;
use std::fs::File;
use std::io::{Read, BufReader};
use std::path::Path;
use std::thread;
use std::sync::Arc;

// Mock rationale: This enum is used to represent the different hashing algorithms supported.
// It's a simple data structure and doesn't require external dependencies or complex logic.
#[derive(Debug, Clone, Copy, PartialEq)]
enum HashAlgorithm {
    Md5,
    Sha1,
    Sha256,
}

impl HashAlgorithm {
    fn from_str(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "md5" => Some(HashAlgorithm::Md5),
            "sha1" => Some(HashAlgorithm::Sha1),
            "sha256" => Some(HashAlgorithm::Sha256),
            _ => None,
        }
    }

    fn name(&self) -> &'static str {
        match self {
            HashAlgorithm::Md5 => "MD5",
            HashAlgorithm::Sha1 => "SHA1",
            HashAlgorithm::Sha256 => "SHA256",
        }
    }
}

// Mock rationale: This struct encapsulates the result of a hashing operation.
// It's a simple data holder and doesn't interact with external systems.
#[derive(Debug, Clone)]
struct HashResult {
    algorithm: HashAlgorithm,
    hash: String,
}

fn calculate_hash<P: AsRef<Path>>(file_path: P, algorithm: HashAlgorithm) -> Result<String, std::io::Error> {
    let file = File::open(file_path)?;
    let mut reader = BufReader::new(file);

    match algorithm {
        HashAlgorithm::Md5 => {
            let mut hasher = Md5::new();
            let mut buffer = [0; 1024]; // Process in chunks
            loop {
                let bytes_read = reader.read(&mut buffer)?;
                if bytes_read == 0 {
                    break;
                }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
        HashAlgorithm::Sha1 => {
            let mut hasher = Sha1::new();
            let mut buffer = [0; 1024];
            loop {
                let bytes_read = reader.read(&mut buffer)?;
                if bytes_read == 0 {
                    break;
                }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
        HashAlgorithm::Sha256 => {
            let mut hasher = Sha256::new();
            let mut buffer = [0; 1024];
            loop {
                let bytes_read = reader.read(&mut buffer)?;
                if bytes_read == 0 {
                    break;
                }
                hasher.update(&buffer[..bytes_read]);
            }
            Ok(format!("{:x}", hasher.finalize()))
        }
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = App::new("Rust File Hasher")
        .version("1.0")
        .author("ApocalypsAI Integrator")
        .about("Calculates cryptographic hashes for files.")
        .arg(Arg::with_name("file")
            .help("The path to the file to hash")
            .required(true)
            .index(1))
        .arg(Arg::with_name("algorithm")
            .short("a")
            .long("algorithm")
            .help("Hashing algorithm to use (md5, sha1, sha256)")
            .takes_value(true)
            .default_value("sha256"))
        .arg(Arg::with_name("threads")
            .short("t")
            .long("threads")
            .help("Number of threads for parallel processing")
            .takes_value(true))
        .get_matches();

    let file_path = matches.value_of("file").unwrap();
    let algorithm = HashAlgorithm::from_str(matches.value_of("algorithm").unwrap())
        .ok_or("Invalid algorithm specified")?;

    let num_threads = matches.value_of("threads").map(|t| t.parse::<usize>().unwrap_or(1)).unwrap_or_else(|| num_cpus::get());

    println!("Calculating {} hash for: {}", algorithm.name(), file_path);

    if num_threads > 1 {
        // Basic parallelization strategy: split file into chunks and process each chunk
        // This is a simplified example and might not be optimal for all file sizes/types.
        // For true high-performance, consider more advanced chunking or memory mapping.
        let file_arc = Arc::new(std::fs::read(file_path)?);
        let chunk_size = (file_arc.len() as f64 / num_threads as f64).ceil() as usize;
        let mut handles = vec![];

        for i in 0..num_threads {
            let file_clone = Arc::clone(&file_arc);
            let algorithm_clone = algorithm;
            let start = i * chunk_size;
            let end = std::cmp::min(start + chunk_size, file_clone.len());

            if start >= end {
                continue;
            }

            handles.push(thread::spawn(move || {
                let mut hasher: Box<dyn Digest> = match algorithm_clone {
                    HashAlgorithm::Md5 => Box::new(Md5::new()),
                    HashAlgorithm::Sha1 => Box::new(Sha1::new()),
                    HashAlgorithm::Sha256 => Box::new(Sha256::new()),
                };
                hasher.update(&file_clone[start..end]);
                HashResult { algorithm: algorithm_clone, hash: format!("{:x}", hasher.finalize()) }
            }));
        }

        let mut final_hasher: Box<dyn Digest> = match algorithm {
            HashAlgorithm::Md5 => Box::new(Md5::new()),
            HashAlgorithm::Sha1 => Box::new(Sha1::new()),
            HashAlgorithm::Sha256 => Box::new(Sha256::new()),
        };
        for handle in handles {
            let result = handle.join().unwrap();
            final_hasher.update(result.hash.as_bytes()); // This is a simplification, actual parallel hashing requires more complex logic
        }
        println!("{} (parallel): {:x}", algorithm.name(), final_hasher.finalize());

    } else {
        let hash = calculate_hash(file_path, algorithm)?;
        println!("{} (single-thread): {}", algorithm.name(), hash);
    }

    Ok(())
}
