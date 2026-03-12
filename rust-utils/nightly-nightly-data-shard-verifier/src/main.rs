use clap::Parser;
use sha2::{Digest, Sha256};
use std::{fs, path::PathBuf, io::{self, Read}};

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// Path to the data shard (file or directory) to verify
    #[clap(short, long, value_parser)]
    path: PathBuf,

    /// Expected SHA256 checksum (optional, for verification)
    #[clap(short, long, value_parser)]
    expected_checksum: Option<String>,
}

enum FileType {
    Png,
    Jpeg,
    Pdf,
    Zip,
    Text,
    Unknown,
}

impl FileType {
    fn identify(bytes: &[u8]) -> Self {
        if bytes.len() < 4 { // Most magic bytes are at least 4 bytes
            return FileType::Unknown;
        }

        // PNG: 89 50 4E 47 0D 0A 1A 0A
        if bytes.starts_with(&[0x89, 0x50, 0x4E, 0x47]) {
            return FileType::Png;
        }
        // JPEG: FF D8 FF E0 (JFIF) or FF D8 FF E1 (Exif)
        if bytes.starts_with(&[0xFF, 0xD8, 0xFF]) && (bytes[3] == 0xE0 || bytes[3] == 0xE1) {
            return FileType::Jpeg;
        }
        // PDF: %PDF
        if bytes.starts_with(b"%PDF") {
            return FileType::Pdf;
        }
        // ZIP: PK\x03\x04
        if bytes.starts_with(&[0x50, 0x4B, 0x03, 0x04]) {
            return FileType::Zip;
        }
        // Simple text heuristic: check for printable ASCII characters
        if bytes.iter().all(|&b| b == 0x09 || b == 0x0A || b == 0x0D || (b >= 0x20 && b <= 0x7E)) {
            return FileType::Text;
        }

        FileType::Unknown
    }

    fn to_string(&self) -> &str {
        match self {
            FileType::Png => "PNG Image",
            FileType::Jpeg => "JPEG Image",
            FileType::Pdf => "PDF Document",
            FileType::Zip => "ZIP Archive",
            FileType::Text => "Plain Text",
            FileType::Unknown => "Unknown",
        }
    }
}

fn calculate_sha256(path: &PathBuf) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    io::copy(&mut file, &mut hasher)?;
    Ok(format!("{:x}", hasher.finalize()))
}

fn process_file(file_path: &PathBuf, expected_checksum: &Option<String>) -> io::Result<()> {
    println!("Processing: {}", file_path.display());

    let mut file = fs::File::open(file_path)?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer)?;

    let calculated_checksum = calculate_sha256(file_path)?;
    println!("  SHA256: {}", calculated_checksum);

    if let Some(expected) = expected_checksum {
        if expected == &calculated_checksum {
            println!("  Checksum: MATCHES expected!");
        } else {
            println!("  Checksum: MISMATCH! Expected {} but got {}.", expected, calculated_checksum);
        }
    }

    let file_type = FileType::identify(&buffer);
    println!("  Identified Type: {}", file_type.to_string());

    Ok(())
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    if !args.path.exists() {
        eprintln!("Error: Path does not exist: {}", args.path.display());
        std::process::exit(1);
    }

    if args.path.is_file() {
        process_file(&args.path, &args.expected_checksum)?;
    } else if args.path.is_dir() {
        for entry in fs::read_dir(&args.path)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_file() {
                process_file(&path, &args.expected_checksum)?;
            }
        }
    }

    Ok(())
}
