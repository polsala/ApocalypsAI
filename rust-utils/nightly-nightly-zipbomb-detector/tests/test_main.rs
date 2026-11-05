use std::fs::File;
use std::io::Write;
use std::path::PathBuf;

use zip::write::FileOptions;
use zip::CompressionMethod;

// Import the library function from the crate (crate name uses underscores)
use nightly_zipbomb_detector::analyze_zip;

fn create_zip(path: &PathBuf, entries: Vec<(&[u8], &str, CompressionMethod)>) {
    let file = File::create(path).unwrap();
    let mut zip = zip::ZipWriter::new(file);
    for (data, name, method) in entries {
        let options = FileOptions::default().compression_method(method);
        zip.start_file(name, options).unwrap();
        zip.write_all(data).unwrap();
    }
    zip.finish().unwrap();
}

// Mock rationale: create a normal zip with modest compression ratio
#[test]
fn test_normal_zip() {
    let mut tmp = std::env::temp_dir();
    tmp.push("normal.zip");
    let data = b"Hello world!";
    create_zip(&tmp, vec![(data, "hello.txt", CompressionMethod::Deflated)]);
    let result = analyze_zip(&tmp).unwrap();
    assert!(!result, "Normal zip should not be flagged as bomb");
    std::fs::remove_file(tmp).unwrap();
}

// Mock rationale: create a zip with huge uncompressed data but tiny compressed size
#[test]
fn test_zip_bomb() {
    let mut tmp = std::env::temp_dir();
    tmp.push("bomb.zip");
    // 1 MB of repetitive data compresses extremely well
    let data = vec![b'A'; 1_000_000];
    create_zip(&tmp, vec![( &data, "big.txt", CompressionMethod::Deflated)]);
    let result = analyze_zip(&tmp).unwrap();
    // Expect ratio > 100, thus flagged as bomb
    assert!(result, "High compression ratio zip should be flagged as bomb");
    std::fs::remove_file(tmp).unwrap();
}
