use std::env;
use std::fs;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};
use sha2::{Sha256, Digest};
use std::io::{self, Read};

/// Format bytes into human-readable format
fn format_bytes(bytes: u64) -> String {
    const UNITS: &[&str] = &["B", "KB", "MB", "GB", "TB"];
    let mut size = bytes as f64;
    let mut unit_index = 0;
    
    while size >= 1024.0 && unit_index < UNITS.len() - 1 {
        size /= 1024.0;
        unit_index += 1;
    }
    
    format!("{:.1} {}", size, UNITS[unit_index])
}

/// Format timestamp into readable format
fn format_timestamp(timestamp: u64) -> String {
    // Simple timestamp formatting - in a real app, you might use chrono
    format!("{} seconds since Unix epoch", timestamp)
}

/// Calculate SHA-256 hash of a file
fn calculate_sha256<P: AsRef<Path>>(path: P) -> io::Result<String> {
    let mut file = fs::File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0; 8192];
    
    loop {
        let bytes_read = file.read(&mut buffer)?;
        if bytes_read == 0 {
            break;
        }
        hasher.update(&buffer[..bytes_read]);
    }
    
    let result = hasher.finalize();
    Ok(format!("{:x}", result)[..12].to_string() + "...")
}

/// Get file metadata
fn get_file_info<P: AsRef<Path>>(path: P) -> io::Result<(u64, u64, String)> {
    let metadata = fs::metadata(&path)?;
    let size = metadata.len();
    
    let modified = metadata.modified()
        .unwrap_or(SystemTime::UNIX_EPOCH)
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_secs();
    
    let hash = calculate_sha256(&path)?;
    
    Ok((size, modified, hash))
}

/// Compare two files and check if they're identical
fn compare_files<P1: AsRef<Path>, P2: AsRef<Path>>(
    file1: P1,
    file2: P2,
    verbose: bool
) -> io::Result<bool> {
    let path1 = file1.as_ref();
    let path2 = file2.as_ref();
    
    // Check if files exist
    if !path1.exists() {
        return Err(io::Error::new(
            io::ErrorKind::NotFound,
            format!("File not found: {}", path1.display())
        ));
    }
    
    if !path2.exists() {
        return Err(io::Error::new(
            io::ErrorKind::NotFound,
            format!("File not found: {}", path2.display())
        ));
    }
    
    // Get file info
    let (size1, modified1, hash1) = get_file_info(&path1)?;
    let (size2, modified2, hash2) = get_file_info(&path2)?;
    
    // Print file information
    println!("🔬 Quantum Entanglement Checker 🧪\n");
    
    println!("File 1: {}", path1.display());
    println!("  📏 Size: {}", format_bytes(size1));
    println!("  🕐 Modified: {}", format_timestamp(modified1));
    println!("  🔍 SHA-256: {}", hash1);
    
    println!("\nFile 2: {}", path2.display());
    println!("  📏 Size: {}", format_bytes(size2));
    println!("  🕐 Modified: {}", format_timestamp(modified2));
    println!("  🔍 SHA-256: {}", hash2);
    
    // Compare files
    let are_identical = hash1 == hash2;
    
    if are_identical {
        println!("\n🎉 QUANTUM ENTANGLEMENT DETECTED! 🎉\n");
        println!("The files are quantum-entangled (identical)!");
        println!("Spooky action at a distance confirmed. ✨");
    } else {
        println!("\n❌ QUANTUM ENTANGLEMENT NOT FOUND");
        println!("\nThe files are not quantum-entangled (different).");
        println!("No spooky action detected today. 👻");
    }
    
    if verbose {
        println!("\n--- Verbose Details ---");
        println!("File 1 hash: {}", calculate_sha256(&path1)?);
        println!("File 2 hash: {}", calculate_sha256(&path2)?);
        println!("Identical: {}", are_identical);
    }
    
    Ok(are_identical)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // Check for help
    if args.len() == 1 || args.contains(&"--help".to_string()) || args.contains(&"-h".to_string()) {
        println!("Nightly Quantum Entanglement Checker 🧪\n");
        println!("Usage:");
        println!("  {} <file1> <file2> [options]", args[0]);
        println!("\nOptions:");
        println!("  --help, -h     Show this help message");
        println!("  --verbose, -v  Show verbose output");
        println!("\nDescription:");
        println!("  Checks if two files are quantum-entangled (identical)");
        println!("  and provides a whimsical quantum-themed report.");
        return;
    }
    
    // Check for minimum arguments
    if args.len() < 3 {
        eprintln!("Error: Please provide two file paths to compare");
        eprintln!("Usage: {} <file1> <file2>", args[0]);
        std::process::exit(1);
    }
    
    let file1 = &args[1];
    let file2 = &args[2];
    let verbose = args.contains(&"--verbose".to_string()) || args.contains(&"-v".to_string());
    
    match compare_files(file1, file2, verbose) {
        Ok(_) => {
            // Exit with appropriate code
            std::process::exit(0);
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
