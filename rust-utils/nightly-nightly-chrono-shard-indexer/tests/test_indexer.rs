#![allow(unused_imports)]
use super::*;
use std::fs::{self, File};
use std::io::Write;
use tempfile::tempdir;

// Mock rationale: We create temporary directories and files to simulate a file system
// for testing. This ensures tests are deterministic and offline, as they don't rely
// on actual system files or network access.

#[test]
fn test_index_shards_basic() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    fs::write(path.join("shard1.txt"), "Hello world\nLine 2")?;
    fs::write(path.join("shard2.log"), "Another log entry")?;
    fs::write(path.join("binary.bin"), &[0x01, 0x02, 0x03])?;

    index_shards(path, &index_file)?;

    assert!(index_file.exists());
    let shards = load_index(&index_file)?;
    assert_eq!(shards.len(), 2); // binary.bin should be skipped

    let shard1 = shards.iter().find(|s| s.path.ends_with("shard1.txt")).unwrap();
    assert_eq!(shard1.first_line_snippet, "Hello world");
    assert_eq!(shard1.hash, format!("{:x}", Sha256::digest(b"Hello world\nLine 2")));

    let shard2 = shards.iter().find(|s| s.path.ends_with("shard2.log")).unwrap();
    assert_eq!(shard2.first_line_snippet, "Another log entry");

    Ok(())
}

#[test]
fn test_index_shards_subdirectories() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    let sub_dir = path.join("sub");
    fs::create_dir(&sub_dir)?;
    fs::write(sub_dir.join("sub_shard.txt"), "Subdirectory content")?;

    index_shards(path, &index_file)?;

    let shards = load_index(&index_file)?;
    assert_eq!(shards.len(), 1);
    assert!(shards[0].path.ends_with("sub/sub_shard.txt"));

    Ok(())
}

#[test]
fn test_search_shards_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    fs::write(path.join("note1.txt"), "Found important data here.")?;
    fs::write(path.join("log.txt"), "No data of interest.")?;
    fs::write(path.join("report.md"), "Summary of important findings.")?;

    index_shards(path, &index_file)?;

    // Capture stdout to check search results
    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout().into_inner(); // Mock rationale: Redirect stdout to capture output

    search_shards("important", &index_file)?;

    let output = _guard.into_inner().unwrap().read_to_string().unwrap();
    assert!(output.contains("Found in: "));
    assert!(output.contains("note1.txt"));
    assert!(output.contains("report.md"));
    assert!(!output.contains("log.txt"));
    assert!(output.contains("Found 2 shards matching 'important'."));

    Ok(())
}

#[test]
fn test_search_shards_not_found() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    fs::write(path.join("note1.txt"), "Hello world.")?;

    index_shards(path, &index_file)?;

    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout().into_inner(); // Mock rationale: Redirect stdout to capture output

    search_shards("nonexistent", &index_file)?;

    let output = _guard.into_inner().unwrap().read_to_string().unwrap();
    assert!(!output.contains("Found in: "));
    assert!(output.contains("Found 0 shards matching 'nonexistent'."));

    Ok(())
}

#[test]
fn test_deduplicate_shards_no_delete() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    fs::write(path.join("unique.txt"), "Unique content")?;
    fs::write(path.join("duplicate1.txt"), "Shared content")?;
    fs::write(path.join("duplicate2.log"), "Shared content")?;

    index_shards(path, &index_file)?;

    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout().into_inner(); // Mock rationale: Redirect stdout to capture output

    deduplicate_shards(&index_file, false)?;

    let output = _guard.into_inner().unwrap().read_to_string().unwrap();
    assert!(output.contains("Duplicate content"));
    assert!(output.contains("duplicate1.txt"));
    assert!(output.contains("duplicate2.log"));
    assert!(output.contains("Found 1 duplicate shards."));
    assert!(path.join("duplicate1.txt").exists()); // Should not be deleted
    assert!(path.join("duplicate2.log").exists()); // Should not be deleted

    Ok(()) 
}

#[test]
fn test_deduplicate_shards_with_delete() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    fs::write(path.join("unique.txt"), "Unique content")?;
    fs::write(path.join("duplicate_a.txt"), "Shared content")?;
    fs::write(path.join("duplicate_b.log"), "Shared content")?;
    fs::write(path.join("duplicate_c.md"), "Shared content")?;

    index_shards(path, &index_file)?;

    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout().into_inner(); // Mock rationale: Redirect stdout to capture output

    deduplicate_shards(&index_file, true)?;

    let output = _guard.into_inner().unwrap().read_to_string().unwrap();
    assert!(output.contains("Deleted 2 duplicate files."));
    assert!(path.join("unique.txt").exists());
    // One of the duplicates should remain, the others deleted
    let remaining_duplicates: Vec<_> = ["duplicate_a.txt", "duplicate_b.log", "duplicate_c.md"]
        .iter()
        .filter(|&f| path.join(f).exists())
        .collect();
    assert_eq!(remaining_duplicates.len(), 1);

    // Verify index is re-created and reflects deletions
    let updated_shards = load_index(&index_file)?;
    assert_eq!(updated_shards.len(), 2); // unique.txt + 1 remaining duplicate

    Ok(())
}

#[test]
fn test_deduplicate_shards_no_duplicates() -> Result<(), Box<dyn std::error::Error>> {
    let dir = tempdir()?;
    let path = dir.path();
    let index_file = path.join(".chrono_index.json");

    fs::write(path.join("file1.txt"), "Content A")?;
    fs::write(path.join("file2.txt"), "Content B")?;

    index_shards(path, &index_file)?;

    let mut buffer = Vec::new();
    let stdout = std::io::stdout();
    let _guard = gag::BufferRedirect::stdout().into_inner(); // Mock rationale: Redirect stdout to capture output

    deduplicate_shards(&index_file, false)?;

    let output = _guard.into_inner().unwrap().read_to_string().unwrap();
    assert!(output.contains("No duplicate shards found."));

    Ok()
}

// Helper to capture stdout for testing CLI output
mod gag {
    use std::io::{self, Read};
    use std::os::fd::{AsRawFd, FromRawFd};
    use std::sync::Mutex;

    static STDOUT_LOCK: Mutex<()> = Mutex::new(());

    pub struct BufferRedirect {
        original_stdout: Option<std::fs::File>,
        pipe_read: Option<std::fs::File>,
        _lock: std::sync::MutexGuard<'static, ()>,
    }

    impl BufferRedirect {
        pub fn stdout() -> io::Result<Self> {
            let _lock = STDOUT_LOCK.lock().unwrap();
            let (pipe_read, pipe_write) = os_pipe::pipe()?;
            let original_stdout = Some(dup_stdout()?);

            // Redirect stdout to the write end of the pipe
            libc::dup2(pipe_write.as_raw_fd(), io::stdout().as_raw_fd());

            Ok(BufferRedirect {
                original_stdout,
                pipe_read: Some(pipe_read),
                _lock,
            })
        }

        pub fn into_inner(mut self) -> io::Result<std::fs::File> {
            // Restore original stdout
            if let Some(original) = self.original_stdout.take() {
                libc::dup2(original.as_raw_fd(), io::stdout().as_raw_fd());
            }
            self.pipe_read.take().ok_or_else(|| io::Error::new(io::ErrorKind::Other, "Pipe already taken"))
        }
    }

    impl Drop for BufferRedirect {
        fn drop(&mut self) {
            if let Some(original) = self.original_stdout.take() {
                // Restore original stdout if not already done
                libc::dup2(original.as_raw_fd(), io::stdout().as_raw_fd());
            }
        }
    }

    fn dup_stdout() -> io::Result<std::fs::File> {
        let fd = io::stdout().as_raw_fd();
        let new_fd = libc::dup(fd);
        if new_fd == -1 {
            Err(io::Error::last_os_error())
        } else {
            Ok(unsafe { std::fs::File::from_raw_fd(new_fd) })
        }
    }
}
