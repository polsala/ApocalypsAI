use std::fs;
use std::path::{Path, PathBuf};
use chrono::{Utc, Duration};
use walkdir::WalkDir;

pub fn find_stale_files(root_path: &Path, stale_days: u64) -> Result<Vec<PathBuf>, Box<dyn std::error::Error>> {
    let mut stale_files = Vec::new();
    let now = Utc::now();
    let cutoff_duration = Duration::days(stale_days as i64);

    for entry in WalkDir::new(root_path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if path.is_file() {
            if let Ok(metadata) = fs::metadata(path) {
                if let Ok(accessed_time) = metadata.accessed() {
                    let accessed_utc: chrono::DateTime<Utc> = accessed_time.into();
                    if now.signed_duration_since(accessed_utc) > cutoff_duration {
                        stale_files.push(path.to_path_buf());
                    }
                }
            }
        }
    }
    Ok(stale_files)
}
