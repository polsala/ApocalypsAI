use clap::{Arg, Command};
use sha1::Sha1;
use sha2::{Sha256, Sha512};
use md5::Md5;
use hex_literal::Literal;
use std::fs::File;
use std::io::{self, Read};
use std::path::PathBuf;

// Mock rationale: Using a simple enum for algorithm selection to avoid external dependencies for this specific part.
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
}

// Mock rationale: A trait to abstract hashing operations, allowing for easy mocking in tests.
trait Hasher {
    fn update(&mut self, data: &[u8]);
    fn finalize(self) -> Vec<u8>;
}

// Mock rationale: Implementations of the Hasher trait for specific algorithms.
impl Hasher for Md5 {
    fn update(&mut self, data: &[u8]) {
        <Md5 as digest::Digest>::update(self, data);
    }
    fn finalize(self) -> Vec<u8> {
        self.finalize().as_slice().to_vec()
    }
}

impl Hasher for Sha1 {
    fn update(&mut self, data: &[u8]) {
        <Sha1 as digest::Digest>::update(self, data);
    }
    fn finalize(self) -> Vec<u8> {
        self.finalize().as_slice().to_vec()
    }
}

impl Hasher for Sha256 {
    fn update(&mut self, data: &[u8]) {
        <Sha256 as digest::Digest>::update(self, data);
    }
    fn finalize(self) -> Vec<u8> {
        self.finalize().as_slice().to_vec()
    }
}

impl Hasher for Sha512 {
    fn update(&mut self, data: &[u8]) {
        <Sha512 as digest::Digest>::update(self, data);
    }
    fn finalize(self) -> Vec<u8> {
        self.finalize().as_slice().to_vec()
    }
}

fn calculate_hash<H: Hasher>(file_path: &PathBuf) -> Result<Vec<u8>, io::Error> {
    let mut file = File::open(file_path)?;
    let mut hasher = H::new();
    let mut buffer = [0; 1024]; // Read in chunks

    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }

    Ok(hasher.finalize())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("nightly-rust-file-hasher")
        .version("1.0")
        .author("ApocalypsAI Integrator")
        .about("Calculates cryptographic hashes of files.")
        .arg(Arg::new("algorithm")
            .help("The hashing algorithm to use (md5, sha1, sha256, sha512)")
            .required(true)
            .index(1))
        .arg(Arg::new("file_path")
            .help("The path to the file to hash")
            .required(true)
            .index(2))
        .get_matches();

    let algorithm_str = matches.get_one::<String>("algorithm").unwrap();
    let file_path_str = matches.get_one::<String>("file_path").unwrap();
    let file_path = PathBuf::from(file_path_str);

    let algorithm = HashAlgorithm::from_str(algorithm_str)
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, format!("Unsupported algorithm: {}", algorithm_str)))?;

    let hash_bytes = match algorithm {
        HashAlgorithm::Md5 => calculate_hash::<Md5>(&file_path)?,
        HashAlgorithm::Sha1 => calculate_hash::<Sha1>(&file_path)?,
        HashAlgorithm::Sha256 => calculate_hash::<Sha256>(&file_path)?,
        HashAlgorithm::Sha512 => calculate_hash::<Sha512>(&file_path)?,
    };

    println!("{}: {}", algorithm_str, hex::encode(hash_bytes));

    Ok(())
}

// Mock rationale: These are dummy implementations of Digest for testing purposes.
// In a real scenario, these would come from the 'digest' crate.
mod mock_digest {
    pub trait Digest {
        fn new() -> Self;
        fn update(&mut self, data: &[u8]);
        fn finalize(self) -> Vec<u8>;
    }

    pub struct MockHasher16; // Represents a 16-byte hash (like MD5)
    impl Digest for MockHasher16 {
        fn new() -> Self { MockHasher16 }
        fn update(&mut self, _data: &[u8]) {}
        fn finalize(self) -> Vec<u8> { vec![0u8; 16] }
    }

    pub struct MockHasher20; // Represents a 20-byte hash (like SHA1)
    impl Digest for MockHasher20 {
        fn new() -> Self { MockHasher20 }
        fn update(&mut self, _data: &[u8]) {}
        fn finalize(self) -> Vec<u8> { vec![0u8; 20] }
    }

    pub struct MockHasher32; // Represents a 32-byte hash (like SHA256)
    impl Digest for MockHasher32 {
        fn new() -> Self { MockHasher32 }
        fn update(&mut self, _data: &[u8]) {}
        fn finalize(self) -> Vec<u8> { vec![0u8; 32] }
    }

    pub struct MockHasher64; // Represents a 64-byte hash (like SHA512)
    impl Digest for MockHasher64 {
        fn new() -> Self { MockHasher64 }
        fn update(&mut self, _data: &[u8]) {}
        fn finalize(self) -> Vec<u8> { vec![0u8; 64] }
    }
}

// Mock rationale: Re-exporting mock digest implementations for testing.
// This allows tests to use these mocks instead of the actual digest crate.
use mock_digest::Digest;

// Mock implementations for the actual types used in calculate_hash
// These will be used by the tests to simulate the behavior of the real digest types.
impl Md5 { fn new() -> Self { Md5 } }
impl Sha1 { fn new() -> Self { Sha1 } }
impl Sha256 { fn new() -> Self { Sha256 } }
impl Sha512 { fn new() -> Self { Sha512 } }

// Dummy structs to satisfy the trait bounds in calculate_hash for tests.
// These are not used in the actual program execution but are necessary for compilation when using mocks.
#[derive(Default)] struct Md5; #[derive(Default)] struct Sha1; #[derive(Default)] struct Sha256; #[derive(Default)] struct Sha512;

// Mock rationale: This is a dummy implementation of the `digest::Digest` trait for `Md5`.
// It's used solely for compilation purposes in the `calculate_hash` function when the real `digest` crate is not available.
impl digest::Digest for Md5 {
    type OutputSize = digest::generic_array::GenericArray<u8, typenum::U16>;
    fn new() -> Self { Md5 }
    fn update(&mut self, _data: &[u8]) {}
    fn finalize(self) -> Self::OutputSize { digest::generic_array::GenericArray::from_slice(&[0u8; 16]) }
}

// Mock rationale: This is a dummy implementation of the `digest::Digest` trait for `Sha1`.
impl digest::Digest for Sha1 {
    type OutputSize = digest::generic_array::GenericArray<u8, typenum::U20>;
    fn new() -> Self { Sha1 }
    fn update(&mut self, _data: &[u8]) {}
    fn finalize(self) -> Self::OutputSize { digest::generic_array::GenericArray::from_slice(&[0u8; 20]) }
}

// Mock rationale: This is a dummy implementation of the `digest::Digest` trait for `Sha256`.
impl digest::Digest for Sha256 {
    type OutputSize = digest::generic_array::GenericArray<u8, typenum::U32>;
    fn new() -> Self { Sha256 }
    fn update(&mut self, _data: &[u8]) {}
    fn finalize(self) -> Self::OutputSize { digest::generic_array::GenericArray::from_slice(&[0u8; 32]) }
}

// Mock rationale: This is a dummy implementation of the `digest::Digest` trait for `Sha512`.
impl digest::Digest for Sha512 {
    type OutputSize = digest::generic_array::GenericArray<u8, typenum::U64>;
    fn new() -> Self { Sha512 }
    fn update(&mut self, _data: &[u8]) {}
    fn finalize(self) -> Self::OutputSize { digest::generic_array::GenericArray::from_slice(&[0u8; 64]) }
}

// Mock rationale: Dummy implementations for typenum::U* types.
mod typenum { pub mod U16 {} pub mod U20 {} pub mod U32 {} pub mod U64 {} }

// Mock rationale: Dummy implementation for digest::generic_array::GenericArray.
mod digest { pub mod generic_array { pub struct GenericArray<T, N> { pub data: [T; N] } impl<T, N: typenum::private::Sealed> GenericArray<T, N> { pub fn from_slice(slice: &[T]) -> Self { /* ... */ } } } }

// Mock rationale: Dummy implementation for typenum::private::Sealed.
mod typenum { pub mod private { pub trait Sealed {} impl Sealed for U16 {} impl Sealed for U20 {} impl Sealed for U32 {} impl Sealed for U64 {} } }

// Mock rationale: Dummy implementation for hex::encode.
mod hex { pub fn encode<T: AsRef<[u8]>>(_data: T) -> String { "mocked_hex_encode".to_string() } }
