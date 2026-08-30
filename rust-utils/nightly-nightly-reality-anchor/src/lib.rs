use sha256::digest_file;
use std::fs;
use std::path::{Path, PathBuf};
use std::io;

pub fn get_anchor_path(file_path: &Path) -> PathBuf {
    let mut anchor_path = file_path.to_path_buf();
    let file_name = anchor_path.file_name().unwrap().to_str().unwrap();
    anchor_path.set_file_name(format!("{}.anchor", file_name));
    anchor_path
}

pub fn calculate_file_hash(file_path: &Path) -> Result<String, io::Error> {
    digest_file(file_path)
}

pub fn store_anchor(file_path: &Path, hash: &str) -> Result<(), io::Error> {
    let anchor_path = get_anchor_path(file_path);
    fs::write(&anchor_path, hash)?;
    Ok(())
}

pub fn load_anchor(file_path: &Path) -> Result<String, io::Error> {
    let anchor_path = get_anchor_path(file_path);
    if !anchor_path.exists() {
        return Err(io::Error::new(io::ErrorKind::NotFound, "Anchor file not found."));
    }
    fs::read_to_string(&anchor_path)
}
