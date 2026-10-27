use chrono::{Duration, Utc};
use walkdir::WalkDir;
use std::path::{Path, PathBuf};
use std::io::{self, Write};
use regex::Regex;

pub struct Scrubber {
    path: PathBuf,
    min_age: Duration,
    exclude_patterns: Vec<Regex>,
    dry_run: bool,
    force: bool,
    verbose: bool,
}

impl Scrubber {
    pub fn new(
        path: PathBuf,
        duration_str: String,
        exclude_patterns_str: Vec<String>,
        dry_run: bool,
        force: bool,
        verbose: bool,
    ) -> Result<Self, String> {
        if !path.exists() {
            return Err(format!("Path '{}' does not exist.", path.display()));
        }
        if !path.is_dir() {
            return Err(format!("Path '{}' is not a directory.", path.display()));
        }

        let min_age = Self::parse_duration(&duration_str)?;
        let exclude_patterns = Self::compile_exclude_patterns(exclude_patterns_str)?;

        Ok(Scrubber {
            path,
            min_age,
            exclude_patterns,
            dry_run,
            force,
            verbose,
        })
    }

    pub fn path(&self) -> &Path {
        &self.path
    }

    pub fn dry_run(&self) -> bool {
        self.dry_run
    }

    fn parse_duration(s: &str) -> Result<Duration, String> {
        let s = s.trim();
        let (num_str, unit_str) = s.chars().partition::<String, _>(|c| c.is_ascii_digit());

        let num: i64 = num_str.parse().map_err(|_| format!("Invalid duration format: '{}'. Expected a number.", s))?;

        match unit_str.to_lowercase().as_str() {
            "d" | "" => Ok(Duration::days(num)),
            "w" => Ok(Duration::weeks(num)),
            "m" => Ok(Duration::days(num * 30)), // Approximate months as 30 days
            "y" => Ok(Duration::days(num * 365)), // Approximate years as 365 days
            _ => Err(format!("Invalid duration unit: '{}'. Expected d, w, M, or y.", unit_str)),
        }
    }

    fn compile_exclude_patterns(patterns: Vec<String>) -> Result<Vec<Regex>, String> {
        patterns.into_iter().map(|p| {
            // Convert glob to regex. This is a basic conversion and might not cover all glob features.
            let regex_pattern = p.replace('.', "\\.").replace('*', ".*").replace('?', ".");
            Regex::new(&format!("^{}$", regex_pattern))
                .map_err(|e| format!("Invalid exclude pattern '{}': {}", p, e))
        }).collect()
    }

    fn is_excluded(&self, path: &Path) -> bool {
        let path_str = path.to_string_lossy();
        self.exclude_patterns.iter().any(|re| re.is_match(&path_str))
    }

    pub fn scan_for_decayed_files(&self) -> Result<Vec<PathBuf>, String> {
        let now = Utc::now();
        let mut decayed_files = Vec::new();

        for entry in WalkDir::new(&self.path).into_iter().filter_map(|e| e.ok()) {
            let path = entry.path();

            if path.is_dir() {
                if self.is_excluded(path) {
                    if self.verbose { eprintln!("Verbose: Skipping excluded directory: {}", path.display()); }
                    // If a directory is excluded, skip its contents too
                    entry.into_path(); // Consume the entry to prevent re-processing
                    continue;
                }
                continue; // Skip directories themselves, we only care about files
            }

            if self.is_excluded(path) {
                if self.verbose { eprintln!("Verbose: Skipping excluded file: {}", path.display()); }
                continue;
            }

            if let Ok(metadata) = path.metadata() {
                if let Ok(modified_time) = metadata.modified() {
                    let modified_utc: chrono::DateTime<Utc> = modified_time.into();
                    if now - modified_utc > self.min_age {
                        decayed_files.push(path.to_path_buf());
                    }
                } else if self.verbose {
                    eprintln!("Verbose: Could not get modified time for {}. Skipping.", path.display());
                }
            } else if self.verbose {
                eprintln!("Verbose: Could not get metadata for {}. Skipping.", path.display());
            }
        }
        Ok(decayed_files)
    }

    pub fn perform_scrub(&self, files: Vec<PathBuf>) -> Result<usize, String> {
        let mut scrubbed_count = 0;
        for file in files {
            if self.dry_run {
                println!("Dry run: Would scrub '{}'.", file.display());
                continue;
            }

            let should_delete = if self.force {
                true
            } else {
                print!("Delete '{}'? (y/N): ", file.display());
                io::stdout().flush().map_err(|e| format!("Failed to flush stdout: {}", e))?;
                let mut input = String::new();
                io::stdin().read_line(&mut input).map_err(|e| format!("Failed to read input: {}", e))?;
                input.trim().to_lowercase() == "y"
            };

            if should_delete {
                match std::fs::remove_file(&file) {
                    Ok(_) => {
                        println!("Reclaiming temporal bandwidth: '{}' scrubbed.", file.display());
                        scrubbed_count += 1;
                    }
                    Err(e) => eprintln!("Error scrubbing '{}': {}", file.display(), e),
                }
            } else {
                println!("Skipping '{}'.", file.display());
            }
        }
        Ok(scrubbed_count)
    }
}

#[cfg(test)]
mod unit_tests {
    use super::*;
    use chrono::Duration;

    #[test]
    fn test_parse_duration_days() {
        assert_eq!(Scrubber::parse_duration("30d").unwrap(), Duration::days(30));
        assert_eq!(Scrubber::parse_duration("90").unwrap(), Duration::days(90));
    }

    #[test]
    fn test_parse_duration_weeks() {
        assert_eq!(Scrubber::parse_duration("2w").unwrap(), Duration::weeks(2));
    }

    #[test]
    fn test_parse_duration_months() {
        // Approximate months as 30 days
        assert_eq!(Scrubber::parse_duration("3M").unwrap(), Duration::days(90));
    }

    #[test]
    fn test_parse_duration_years() {
        // Approximate years as 365 days
        assert_eq!(Scrubber::parse_duration("1y").unwrap(), Duration::days(365));
    }

    #[test]
    fn test_parse_duration_invalid() {
        assert!(Scrubber::parse_duration("abc").is_err());
        assert!(Scrubber::parse_duration("10x").is_err());
        assert!(Scrubber::parse_duration("d").is_err()); // No number
    }

    #[test]
    fn test_compile_exclude_patterns() {
        let patterns = vec!["*.log".to_string(), "temp/**".to_string()];
        let compiled = Scrubber::compile_exclude_patterns(patterns).unwrap();
        assert_eq!(compiled.len(), 2);
        assert!(compiled[0].is_match("my_app.log"));
        assert!(!compiled[0].is_match("my_app.txt"));
        assert!(compiled[1].is_match("temp/file.txt"));
        assert!(compiled[1].is_match("temp/subdir/file.txt"));
        assert!(!compiled[1].is_match("not_temp/file.txt"));
    }

    #[test]
    fn test_is_excluded() {
        let scrubber = Scrubber::new(
            PathBuf::from("."),
            "1d".to_string(),
            vec!["*.tmp".to_string(), "cache/**".to_string()],
            true, false, false
        ).unwrap();

        assert!(scrubber.is_excluded(&PathBuf::from("file.tmp")));
        assert!(scrubber.is_excluded(&PathBuf::from("cache/data.json")));
        assert!(scrubber.is_excluded(&PathBuf::from("cache/subdir/data.json")));
        assert!(!scrubber.is_excluded(&PathBuf::from("file.log")));
    }

    #[test]
    fn test_new_invalid_path() {
        let result = Scrubber::new(
            PathBuf::from("non_existent_dir"),
            "1d".to_string(),
            vec![],
            true, false, false
        );
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("does not exist"));
    }

    #[test]
    fn test_new_file_path() {
        // Mock rationale: Create a temporary file to test path validation.
        let temp_file = tempfile::NamedTempFile::new().unwrap();
        let result = Scrubber::new(
            temp_file.path().to_path_buf(),
            "1d".to_string(),
            vec![],
            true, false, false
        );
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("is not a directory"));
    }
}
