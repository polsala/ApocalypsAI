use clap::{Arg, Command};
use sha1::Sha1;
use sha2::{Sha256, Sha512};
use md5::Md5;
use hex_literal::Literal;
use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;

// Mock rationale: Using a simple enum for algorithms to avoid external dependencies for algorithm listing.
enum SupportedAlgorithm {
    Md5,
    Sha1,
    Sha256,
    Sha512,
}

impl SupportedAlgorithm {
    fn from_str(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "md5" => Some(SupportedAlgorithm::Md5),
            "sha1" => Some(SupportedAlgorithm::Sha1),
            "sha256" => Some(SupportedAlgorithm::Sha256),
            "sha512" => Some(SupportedAlgorithm::Sha512),
            _ => None,
        }
    }

    fn to_string(&self) -> String {
        match self {
            SupportedAlgorithm::Md5 => "md5".to_string(),
            SupportedAlgorithm::Sha1 => "sha1".to_string(),
            SupportedAlgorithm::Sha256 => "sha256".to_string(),
            SupportedAlgorithm::Sha512 => "sha512".to_string(),
        }
    }
}

fn calculate_hash<R: Read>(mut reader: R, algorithm: &SupportedAlgorithm) -> io::Result<String> {
    let mut buffer = Vec::new();
    reader.read_to_end(&mut buffer)?;

    let hash_string = match algorithm {
        SupportedAlgorithm::Md5 => {
            let mut hasher = Md5::new();
            hasher.update(&buffer);
            format!("{:x}", hasher.finalize())
        }
        SupportedAlgorithm::Sha1 => {
            let mut hasher = Sha1::new();
            hasher.update(&buffer);
            format!("{:x}", hasher.finalize())
        }
        SupportedAlgorithm::Sha256 => {
            let mut hasher = Sha256::new();
            hasher.update(&buffer);
            format!("{:x}", hasher.finalize())
        }
        SupportedAlgorithm::Sha512 => {
            let mut hasher = Sha512::new();
            hasher.update(&buffer);
            format!("{:x}", hasher.finalize())
        }
    };
    Ok(hash_string)
}

fn main() -> io::Result<()> {
    let matches = Command::new("nightly-rust-file-hasher")
        .version("1.0")
        .author("ApocalypsAI Integrator")
        .about("Generates cryptographic hashes of files.")
        .arg(Arg::new("algorithm")
            .short('a')
            .long("algorithm")
            .help("The hashing algorithm to use (md5, sha1, sha256, sha512)")
            .takes_value(true)
            .required_unless_present("list_algorithms"))
        .arg(Arg::new("file")
            .short('f')
            .long("file")
            .help("The path to the file to hash")
            .takes_value(true)
            .required_unless_present("list_algorithms"))
        .arg(Arg::new("list_algorithms")
            .long("list-algorithms")
            .help("List all supported hashing algorithms")
            .takes_value(false))
        .get_matches();

    if matches.is_present("list_algorithms") {
        println!("Supported algorithms:");
        for algo in ["md5", "sha1", "sha256", "sha512"] {
            println!("- {}", algo);
        }
        return Ok(())
    }

    let algorithm_str = matches.value_of("algorithm").unwrap();
    let file_path_str = matches.value_of("file").unwrap();

    let algorithm = SupportedAlgorithm::from_str(algorithm_str)
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, format!("Unsupported algorithm: {}", algorithm_str)))?;

    let file_path = PathBuf::from(file_path_str);
    let file = File::open(file_path)?;

    let hash = calculate_hash(file, &algorithm)?;

    println!("Algorithm: {}", algorithm.to_string());
    println!("File: {}", file_path_str);
    println!("Hash: {}", hash);

    Ok(())
}
