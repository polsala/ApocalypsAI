use std::env;
use std::fs;
use std::path::Path;
use sha2::{Sha256, Digest};
use clap::{Arg, Command};

/// Generate a SHA-256 hash for the given content
fn generate_hash(content: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content);
    format!("{:x}", hasher.finalize())
}

/// Check if two hashes are identical (quantum entangled)
fn are_entangled(hash_a: &str, hash_b: &str) -> bool {
    hash_a == hash_b
}

/// Generate a whimsical quantum entanglement report
fn generate_entanglement_report(file_a: &str, file_b: &str, entangled: bool) -> String {
    let header = "🔬 Quantum Entanglement Analysis Report 🔬\n";
    let separator = "==========================================\n\n";
    
    let file_info = format!("File A: {}\nFile B: {}\n\n", file_a, file_b);
    
    let result = if entangled {
        "✅ ENTANGLEMENT CONFIRMED!\n\n".to_string() +
        "Both particles (files) share identical quantum states.\n" +
        "The universe has spoken: these code snippets are entangled.\n\n" +
        "Quantum Coherence Level: MAXIMUM\n" +
        "Spooky Action at Distance: DETECTED\n\n" +
        "Recommendation: Keep these particles together for optimal quantum computing performance."
    } else {
        "❌ ENTANGLEMENT REJECTED!\n\n".to_string() +
        "These particles (files) exist in separate quantum states.\n" +
        "No spooky action detected at this time.\n\n" +
        "Quantum Coherence Level: NONE\n" +
        "Spooky Action at Distance: NOT DETECTED\n\n" +
        "Recommendation: These particles may benefit from quantum tunneling or a good compiler."    };
    
    header.to_string() + separator + &file_info + &result
}

/// Read file content and return its hash
fn get_file_hash<P: AsRef<Path>>(path: P) -> Result<String, Box<dyn std::error::Error>> {
    let content = fs::read(path.as_ref())?;
    Ok(generate_hash(&content))
}

/// Get hash for a string
fn get_string_hash(content: &str) -> String {
    generate_hash(content.as_bytes())
}

fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("A whimsical utility that checks if two code snippets are 'quantum entangled'")
        .arg(
            Arg::new("file_a")
                .help("First file to compare")
                .required_unless_present("string")
                .conflicts_with("string")
        )
        .arg(
            Arg::new("file_b")
                .help("Second file to compare")
                .required_unless_present("string")
                .conflicts_with("string")
        )
        .arg(
            Arg::new("string")
                .help("Strings to compare (use twice)")
                .short('s')
                .long("string")
                .action(clap::ArgAction::Append)
                .required(false)
                .number_of_values(2)
        )
        .arg(
            Arg::new("report")
                .help("Generate a detailed quantum entanglement report")
                .short('r')
                .long("report")
                .action(clap::ArgAction::SetTrue)
        )
        .get_matches();

    let result = if matches.contains_id("string") {
        let strings: Vec<String> = matches
            .get_many::<String>("string")
            .unwrap()
            .cloned()
            .collect();
        
        if strings.len() != 2 {
            eprintln!("Error: You must provide exactly 2 strings to compare");
            std::process::exit(1);
        }
        
        let hash_a = get_string_hash(&strings[0]);
        let hash_b = get_string_hash(&strings[1]);
        let entangled = are_entangled(&hash_a, &hash_b);
        
        if matches.get_flag("report") {
            println!("{}", generate_entanglement_report(&strings[0], &strings[1], entangled));
        } else {
            println!("String A: '{}' (hash: {})", strings[0], hash_a);
            println!("String B: '{}' (hash: {})", strings[1], hash_b);
            println!("Entangled: {}", entangled);
        }
        
        entangled
    } else {
        let file_a = matches.get_one::<String>("file_a").unwrap();
        let file_b = matches.get_one::<String>("file_b").unwrap();
        
        let hash_a = match get_file_hash(file_a) {
            Ok(hash) => hash,
            Err(e) => {
                eprintln!("Error reading file {}: {}", file_a, e);
                std::process::exit(1);
            }
        };
        
        let hash_b = match get_file_hash(file_b) {
            Ok(hash) => hash,
            Err(e) => {
                eprintln!("Error reading file {}: {}", file_b, e);
                std::process::exit(1);
            }
        };
        
        let entangled = are_entangled(&hash_a, &hash_b);
        
        if matches.get_flag("report") {
            println!("{}", generate_entanglement_report(file_a, file_b, entangled));
        } else {
            println!("File A: {} (hash: {})", file_a, hash_a);
            println!("File B: {} (hash: {})", file_b, hash_b);
            println!("Entangled: {}", entangled);
        }
        
        entangled
    };
    
    // Exit with appropriate code
    if result {
        std::process::exit(0);
    } else {
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::NamedTempFile;

    #[test]
    fn test_generate_hash() {
        let content = b"Hello, World!";
        let hash = generate_hash(content);
        assert_eq!(hash.len(), 64); // SHA-256 produces 64 hex characters
        assert!(hash.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_are_entangled_identical() {
        let hash = "a1b2c3d4e5f6".to_string();
        assert!(are_entangled(&hash, &hash));
    }

    #[test]
    fn test_are_entangled_different() {
        let hash_a = "a1b2c3d4e5f6".to_string();
        let hash_b = "f6e5d4c3b2a1".to_string();
        assert!(!are_entangled(&hash_a, &hash_b));
    }

    #[test]
    fn test_generate_entanglement_report_entangled() {
        let report = generate_entanglement_report("file1.rs", "file2.rs", true);
        assert!(report.contains("ENTANGLEMENT CONFIRMED"));
        assert!(report.contains("MAXIMUM"));
        assert!(report.contains("DETECTED"));
    }

    #[test]
    fn test_generate_entanglement_report_not_entangled() {
        let report = generate_entanglement_report("file1.rs", "file2.rs", false);
        assert!(report.contains("ENTANGLEMENT REJECTED"));
        assert!(report.contains("NONE"));
        assert!(report.contains("NOT DETECTED"));
    }

    #[test]
    fn test_get_file_hash() {
        let temp_file = NamedTempFile::new().unwrap();
        let content = b"Test content for hashing";
        fs::write(temp_file.path(), content).unwrap();
        
        let hash = get_file_hash(temp_file.path()).unwrap();
        assert_eq!(hash.len(), 64);
        assert!(hash.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_get_file_hash_nonexistent() {
        let result = get_file_hash("/nonexistent/file.txt");
        assert!(result.is_err());
    }

    #[test]
    fn test_get_string_hash() {
        let content = "Test string for hashing";
        let hash = get_string_hash(content);
        assert_eq!(hash.len(), 64);
        assert!(hash.chars().all(|c| c.is_ascii_hexdigit()));
    }

    #[test]
    fn test_identical_files_entangled() {
        let temp_file_a = NamedTempFile::new().unwrap();
        let temp_file_b = NamedTempFile::new().unwrap();
        let content = b"Identical content";
        
        fs::write(temp_file_a.path(), content).unwrap();
        fs::write(temp_file_b.path(), content).unwrap();
        
        let hash_a = get_file_hash(temp_file_a.path()).unwrap();
        let hash_b = get_file_hash(temp_file_b.path()).unwrap();
        
        assert!(are_entangled(&hash_a, &hash_b));
    }

    #[test]
    fn test_different_files_not_entangled() {
        let temp_file_a = NamedTempFile::new().unwrap();
        let temp_file_b = NamedTempFile::new().unwrap();
        
        fs::write(temp_file_a.path(), b"Different content A").unwrap();
        fs::write(temp_file_b.path(), b"Different content B").unwrap();
        
        let hash_a = get_file_hash(temp_file_a.path()).unwrap();
        let hash_b = get_file_hash(temp_file_b.path()).unwrap();
        
        assert!(!are_entangled(&hash_a, &hash_b));
    }
}
