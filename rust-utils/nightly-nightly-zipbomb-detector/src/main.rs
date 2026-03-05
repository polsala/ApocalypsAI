use std::env;
use std::fs::File;
use std::path::Path;
use std::process;

use zip::read::ZipArchive;

fn analyze_zip<P: AsRef<Path>>(path: P) -> Result<bool, Box<dyn std::error::Error>> {
    let file = File::open(&path)?;
    let mut archive = ZipArchive::new(file)?;
    let mut total_compressed: u64 = 0;
    let mut total_uncompressed: u64 = 0;

    for i in 0..archive.len() {
        let file = archive.by_index(i)?;
        total_compressed += file.compressed_size();
        total_uncompressed += file.size();
    }

    // Avoid division by zero
    if total_compressed == 0 {
        return Ok(false);
    }

    let ratio = total_uncompressed as f64 / total_compressed as f64;
    Ok(ratio > 100.0)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        eprintln!("Usage: {} <zip-file>", args[0]);
        process::exit(2);
    }

    match analyze_zip(&args[1]) {
        Ok(true) => {
            eprintln!("Warning: Potential zip bomb detected (compression ratio > 100)");
            process::exit(1);
        }
        Ok(false) => {
            println!("OK: No zip bomb detected");
            process::exit(0);
        }
        Err(e) => {
            eprintln!("Error analyzing zip: {}", e);
            process::exit(3);
        }
    }
}
