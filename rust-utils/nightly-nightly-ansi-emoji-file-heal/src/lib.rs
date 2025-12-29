use std::fs::{self, File};
use std::io::{self, BufRead};
use std::path::{Path, PathBuf};

pub struct FileHealth {
    pub path: PathBuf,
    pub size: u64,
    pub lines: usize,
    pub healthy: bool,
}

pub fn analyze_path<P: AsRef<Path>>(root: P) -> io::Result<Vec<FileHealth>> {
    let mut results = Vec::new();
    walk_dir(root.as_ref(), &mut results)?;
    Ok(results)
}

fn walk_dir(dir: &Path, results: &mut Vec<FileHealth>) -> io::Result<()> {
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            walk_dir(&path, results)?;
        } else if path.is_file() {
            let metadata = fs::metadata(&path)?;
            let size = metadata.len();
            let file = File::open(&path)?;
            let lines = io::BufReader::new(file).lines().count();
            let healthy = size < 1_048_576 && lines < 1000;
            results.push(FileHealth {
                path: path.clone(),
                size,
                lines,
                healthy,
            });
        }
    }
    Ok(())
}
