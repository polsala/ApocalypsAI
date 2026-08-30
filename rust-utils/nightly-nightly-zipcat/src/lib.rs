use std::fs::File;
use std::io::{Read, Seek};
use std::path::Path;
use anyhow::{Result, Context};
use zip::read::ZipArchive;

/// Represents a file entry preview.
pub struct FilePreview {
    pub name: String,
    pub preview_bytes: Vec<u8>,
}

/// List entries in a zip archive and return previews of the first `preview_len` bytes.
///
/// * `zip_path` – Path to the zip file.
/// * `preview_len` – Number of bytes to read from each file (max 1024).
/// * `filter` – Optional substring filter for entry names.
///
/// Returns a vector of `FilePreview` sorted by entry name.
pub fn list_zip<P: AsRef<Path>>(
    zip_path: P,
    preview_len: usize,
    filter: Option<&str>,
) -> Result<Vec<FilePreview>> {
    let file = File::open(&zip_path)
        .with_context(|| format!("Failed to open zip file {:?}", zip_path.as_ref()))?;
    let mut archive = ZipArchive::new(file)
        .with_context(|| "Failed to read zip archive")?;

    let mut previews = Vec::new();
    let max_len = preview_len.min(1024);

    for i in 0..archive.len() {
        let mut entry = archive.by_index(i)
            .with_context(|| format!("Failed to access entry {}", i))?;
        let name = entry.name().to_string();

        if let Some(f) = filter {
            if !name.contains(f) {
                continue;
            }
        }

        let mut buf = Vec::new();
        let mut limited = entry.take(max_len as u64);
        limited.read_to_end(&mut buf)
            .with_context(|| format!("Failed to read entry {}", name))?;

        previews.push(FilePreview {
            name,
            preview_bytes: buf,
        });
    }

    previews.sort_by(|a, b| a.name.cmp(&b.name));
    Ok(previews)
}
