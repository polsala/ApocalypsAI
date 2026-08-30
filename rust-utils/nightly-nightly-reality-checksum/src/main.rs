use clap::{Parser, Subcommand, ValueEnum};
use std::collections::HashMap;
use std::fs::{self, File};
use std::io::{self, BufReader, Read, Write};
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

#[derive(Parser, Debug)]
#[command(author, version, about = "A high-performance Rust CLI tool to generate and verify cryptographic checksums of files and directories.", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// Generate checksums for a file or directory
    Generate {
        /// Path to the file or directory to checksum
        path: PathBuf,

        /// Output file to write checksums to
        #[arg(short, long)]
        output: PathBuf,

        /// Checksum algorithm to use (default: sha256)
        #[arg(short, long, default_value_t = Algorithm::Sha256)]
        algorithm: Algorithm,
    },
    /// Verify files or directories against a checksum file
    Verify {
        /// Path to the file or directory to verify
        path: PathBuf,

        /// Input checksum file to read from
        #[arg(short, long)]
        input: PathBuf,

        /// Fail if any file in the checksum file is missing from the path
        #[arg(short, long)]
        strict: bool,
    },
}

#[derive(Copy, Clone, PartialEq, Eq, PartialOrd, Ord, ValueEnum, Debug)]
enum Algorithm {
    Sha256,
    Md5,
}

impl std::fmt::Display for Algorithm {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Algorithm::Sha256 => write!(f, "sha256"),
            Algorithm::Md5 => write!(f, "md5"),
        }
    }
}

fn calculate_file_checksum(path: &Path, algorithm: Algorithm) -> io::Result<String> {
    let file = File::open(path)?;
    let mut reader = BufReader::new(file);
    let mut buffer = Vec::new();
    reader.read_to_end(&mut buffer)?;

    match algorithm {
        Algorithm::Sha256 => Ok(sha256::digest(&buffer)),
        Algorithm::Md5 => Ok(md5::compute(&buffer).iter().map(|b| format!("{:02x}", b)).collect()),
    }
}

fn generate_checksums(
    base_path: &Path,
    output_file: &Path,
    algorithm: Algorithm,
) -> io::Result<()> {
    let mut checksums = Vec::new();

    if base_path.is_file() {
        let checksum = calculate_file_checksum(base_path, algorithm)?;
        let relative_path = base_path
            .file_name()
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidInput, "Invalid file path"))?;
        checksums.push(format!("{}:{}  {}", algorithm, checksum, relative_path.to_string_lossy()));
    } else if base_path.is_dir() {
        for entry in WalkDir::new(base_path)
            .into_iter()
            .filter_map(|e| e.ok())
            .filter(|e| e.file_type().is_file())
        {
            let path = entry.path();
            let checksum = calculate_file_checksum(path, algorithm)?;
            let relative_path = path
                .strip_prefix(base_path)
                .map_err(|e| io::Error::new(io::ErrorKind::Other, format!("Path strip error: {}", e)))?;
            checksums.push(format!(
                "{}:{}  {}",
                algorithm,
                checksum,
                relative_path.to_string_lossy()
            ));
        }
    } else {
        return Err(io::Error::new(
            io::ErrorKind::NotFound,
            "Path does not exist or is not a file/directory",
        ));
    }

    let mut file = File::create(output_file)?;
    for line in checksums {
        writeln!(file, "{}", line)?;
    }
    println!("Checksums generated and saved to '{}'.", output_file.display());
    Ok(())
}

fn read_checksum_file(input_file: &Path) -> io::Result<HashMap<PathBuf, (Algorithm, String)>> {
    let file = File::open(input_file)?;
    let reader = BufReader::new(file);
    let mut checksums = HashMap::new();

    for line in io::BufRead::lines(reader) {
        let line = line?;
        let parts: Vec<&str> = line.splitn(2, ' ').collect();
        if parts.len() != 2 {
            eprintln!("Warning: Skipping malformed line in checksum file: '{}'", line);
            continue;
        }
        let (algo_checksum, filepath_str) = (parts[0], parts[1].trim());
        let algo_checksum_parts: Vec<&str> = algo_checksum.splitn(2, ':').collect();
        if algo_checksum_parts.len() != 2 {
            eprintln!("Warning: Skipping malformed checksum entry: '{}'", algo_checksum);
            continue;
        }
        let (algo_str, checksum_val) = (algo_checksum_parts[0], algo_checksum_parts[1]);

        let algorithm = match algo_str {
            "sha256" => Algorithm::Sha256,
            "md5" => Algorithm::Md5,
            _ => {
                eprintln!("Warning: Unknown algorithm '{}' in checksum file. Skipping line.", algo_str);
                continue;
            }
        };

        checksums.insert(PathBuf::from(filepath_str), (algorithm, checksum_val.to_string()));
    }
    Ok(checksums)
}

fn verify_checksums(
    base_path: &Path,
    input_file: &Path,
    strict_mode: bool,
) -> io::Result<()> {
    let expected_checksums = read_checksum_file(input_file)?;
    let mut discrepancies = 0;
    let mut verified_count = 0;

    let mut actual_files_in_dir = HashMap::new();

    let walker = if base_path.is_file() {
        vec![Ok(walkdir::DirEntry::new_from_path(base_path.to_path_buf()))].into_iter()
    } else if base_path.is_dir() {
        WalkDir::new(base_path).into_iter()
    } else {
        return Err(io::Error::new(io::ErrorKind::NotFound, "Base path for verification does not exist."));
    };

    for entry in walker.filter_map(|e| e.ok()).filter(|e| e.file_type().is_file()) {
        let path = entry.path();
        let relative_path = path
            .strip_prefix(base_path)
            .unwrap_or(path); // If base_path is a file, strip_prefix might fail, use path itself

        actual_files_in_dir.insert(relative_path.to_path_buf(), ());

        if let Some((expected_algo, expected_checksum)) = expected_checksums.get(relative_path) {
            match calculate_file_checksum(path, *expected_algo) {
                Ok(actual_checksum) => {
                    if actual_checksum == *expected_checksum {
                        println!("OK: {} ({})", relative_path.display(), expected_algo);
                        verified_count += 1;
                    } else {
                        println!("MISMATCH: {} (Expected: {}, Actual: {})", relative_path.display(), expected_checksum, actual_checksum);
                        discrepancies += 1;
                    }
                }
                Err(e) => {
                    eprintln!("ERROR: Could not read file {}: {}", relative_path.display(), e);
                    discrepancies += 1;
                }
            }
        } else {
            println!("NEW: {} (Not in checksum file)", relative_path.display());
            discrepancies += 1;
        }
    }

    // Check for missing files if in strict mode
    if strict_mode {
        for (expected_path, _) in &expected_checksums {
            if !actual_files_in_dir.contains_key(expected_path) {
                println!("MISSING: {} (Expected in checksum file, but not found)", expected_path.display());
                discrepancies += 1;
            }
        }
    }

    if discrepancies == 0 {
        println!("\nVerification successful! All {} files are anchored in reality.", verified_count);
        Ok(())
    } else {
        eprintln!("\nVerification failed: {} discrepancies found.", discrepancies);
        Err(io::Error::new(io::ErrorKind::InvalidData, "Checksum verification failed"))
    }
}

fn main() -> io::Result<()> {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Generate { path, output, algorithm } => {
            generate_checksums(path, output, *algorithm)
        }
        Commands::Verify { path, input, strict } => {
            verify_checksums(path, input, *strict)
        }
    }
}
