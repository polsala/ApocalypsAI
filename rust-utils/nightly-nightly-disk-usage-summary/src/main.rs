use std::env;
use std::fs;
use std::io;
use std::path::{Path, PathBuf};

fn get_dir_size(path: &Path) -> io::Result<u64> {
    let mut size = 0;
    for entry in fs::read_dir(path)? {
        let entry = entry?;
        let metadata = entry.metadata()?;
        if metadata.is_file() {
            size += metadata.len();
        } else if metadata.is_dir() {
            size += get_dir_size(&entry.path())?;
        }
    }
    Ok(size)
}

fn human_readable(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;
    if bytes >= GB {
        format!("{:.2} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.2} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.2} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

fn commentary(size: u64) -> &'static str {
    const ONE_MB: u64 = 1024 * 1024;
    const ONE_GB: u64 = ONE_MB * 1024;
    if size >= ONE_GB {
        "This folder is a treasure trove!"
    } else if size < ONE_MB {
        "This folder is a barren wasteland!"
    } else {
        "This folder is moderately populated."
    }
}

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let target = if args.len() > 1 {
        PathBuf::from(&args[1])
    } else {
        env::current_dir()?
    };
    if !target.is_dir() {
        eprintln!("Provided path is not a directory");
        std::process::exit(1);
    }
    println!("Disk usage summary for: {}", target.display());
    println!("{:<30} {:>10} {}", "Folder", "Size", "Commentary");
    println!("{:-<30} {:-<10} {:-<30}", "", "", "");
    for entry in fs::read_dir(&target)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() {
            let size = get_dir_size(&path)?;
            println!(
                "{:<30} {:>10} {}",
                path.file_name().unwrap().to_string_lossy(),
                human_readable(size),
                commentary(size)
            );
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs::{self, File};
    use std::io::Write;
    use std::path::PathBuf;
    use std::time::{SystemTime, UNIX_EPOCH};

    fn unique_temp_dir() -> PathBuf {
        let base = std::env::temp_dir();
        let pid = std::process::id();
        let nanos = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos();
        base.join(format!("nightly_disk_test_{}_{}", pid, nanos))
    }

    #[test]
    fn test_human_readable() {
        assert_eq!(human_readable(500), "500 B");
        assert_eq!(human_readable(2048), "2.00 KB");
        assert_eq!(human_readable(5_242_880), "5.00 MB");
        assert_eq!(human_readable(10_737_418_240), "10.00 GB");
    }

    #[test]
    fn test_get_dir_size() {
        let dir = unique_temp_dir();
        fs::create_dir_all(&dir).unwrap();
        let sub = dir.join("sub");
        fs::create_dir(&sub).unwrap();
        let file1 = sub.join("small.txt");
        let mut f1 = File::create(&file1).unwrap();
        f1.write_all(&vec![0u8; 500]).unwrap();
        let file2 = sub.join("medium.txt");
        let mut f2 = File::create(&file2).unwrap();
        f2.write_all(&vec![0u8; 2_000_000]).unwrap();
        let size = get_dir_size(&sub).unwrap();
        assert_eq!(size, 500 + 2_000_000);
        // Clean up
        fs::remove_dir_all(&dir).unwrap();
    }
}
