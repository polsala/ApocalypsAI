use clap::Parser;
use walkdir::WalkDir;
use std::path::PathBuf;
use std::io::{self, Write};

/// A blazing-fast fuzzy file and directory locator, echoing paths that resonate with your search.
#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Args {
    /// The fuzzy pattern to search for
    pattern: String,

    /// The directory to start searching from (defaults to current directory)
    #[clap(default_value = ".")]
    path: PathBuf,
}

fn main() -> io::Result<()> {
    let args = Args::parse();

    let mut stdout = io::stdout().lock();

    for entry in WalkDir::new(&args.path)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if let Some(name) = path.file_name().and_then(|s| s.to_str()) {
            if fuzzy_match(name, &args.pattern) {
                writeln!(stdout, "{}", path.display())?;
            }
        }
    }
    Ok(())
}

/// Performs a simple fuzzy match.
/// Returns true if all characters of the pattern are found in the target string
/// in the correct order, not necessarily contiguously.
fn fuzzy_match(target: &str, pattern: &str) -> bool {
    if pattern.is_empty() {
        return true;
    }
    if target.is_empty() {
        return false;
    }

    let mut pattern_chars = pattern.chars().peekable();
    let mut target_chars = target.chars();

    while let Some(p_char) = pattern_chars.peek() {
        let mut found_char = false;
        while let Some(t_char) = target_chars.next() {
            if t_char.to_ascii_lowercase() == p_char.to_ascii_lowercase() {
                pattern_chars.next(); // Consume pattern char
                found_char = true;
                break;
            }
        }
        if !found_char {
            return false; // Pattern char not found in target
        }
    }
    true // All pattern chars found in order
}

#[cfg(test)]
mod unit_tests {
    use super::fuzzy_match;

    #[test]
    fn test_fuzzy_match_basic() {
        assert!(fuzzy_match("hello_world", "h_w"));
        assert!(fuzzy_match("fuzzy_match", "fzy"));
        assert!(fuzzy_match("document.pdf", "doc.pdf"));
        assert!(fuzzy_match("Report_2023.txt", "rpt23"));
        assert!(fuzzy_match("ConfigurationFile", "confgfile"));
        assert!(fuzzy_match("test", "test"));
        assert!(fuzzy_match("Test", "test")); // Case-insensitive
        assert!(fuzzy_match("test", "Test")); // Case-insensitive
    }

    #[test]
    fn test_fuzzy_match_no_match() {
        assert!(!fuzzy_match("hello_world", "h_x_w"));
        assert!(!fuzzy_match("fuzzy_match", "fzmchx"));
        assert!(!fuzzy_match("document.pdf", "docx.pdf"));
        assert!(!fuzzy_match("Report_2023.txt", "rpt2024"));
        assert!(!fuzzy_match("ConfigurationFile", "configfilex"));
        assert!(!fuzzy_match("test", "tset")); // Order matters
    }

    #[test]
    fn test_fuzzy_match_empty_pattern() {
        assert!(fuzzy_match("hello", ""));
        assert!(fuzzy_match("", ""));
    }

    #[test]
    fn test_fuzzy_match_empty_target() {
        assert!(!fuzzy_match("", "a"));
    }
}
