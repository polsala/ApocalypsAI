use std::env;
use std::fs;
use std::io::{self, Read};
use std::path::Path;
use sha2::{Sha256, Digest};
use clap::{Arg, Command};

/// Calculate SHA-256 hash of given content
fn calculate_hash(content: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content);
    format!("{:x}", hasher.finalize())
}

/// Calculate similarity percentage between two hashes
fn calculate_similarity(hash1: &str, hash2: &str) -> f64 {
    if hash1.len() != hash2.len() {
        return 0.0;
    }
    
    let mut matching_chars = 0;
    for (c1, c2) in hash1.chars().zip(hash2.chars()) {
        if c1 == c2 {
            matching_chars += 1;
        }
    }
    
    (matching_chars as f64 / hash1.len() as f64) * 100.0
}

/// Get entanglement level description
fn get_entanglement_level(probability: f64) -> (&'static str, &'static str) {
    if probability < 21.0 {
        ("Cosmic Background Radiation", "No meaningful connection")
    } else if probability < 41.0 {
        ("Stellar Drift", "Slight similarities, likely coincidental")
    } else if probability < 61.0 {
        ("Orbital Resonance", "Noticeable patterns, worth investigating")
    } else if probability < 81.0 {
        ("Gravitational Pull", "Strong similarities, likely related")
    } else {
        ("Quantum Entanglement", "Nearly identical, definitely related")
    }
}

/// Get whimsical status message
fn get_status_message(probability: f64) -> String {
    match probability as u8 {
        0..=20 => "The quantum fields are incoherent. These files exist in separate realities.".to_string(),
        21..=40 => "Faint quantum echoes suggest a distant relationship.".to_string(),
        41..=60 => "The wave functions show intriguing patterns of similarity.".to_string(),
        61..=80 => "Quantum signatures align strongly. A significant connection is probable.".to_string(),
        81..=100 => "Quantum entanglement confirmed! These code snippets share a fundamental connection.".to_string(),
        _ => "Quantum uncertainty prevents further analysis.".to_string(),
    }
}

/// Get recommendation based on similarity
fn get_recommendation(probability: f64) -> String {
    match probability as u8 {
        0..=20 => "No action needed. These files are unrelated.".to_string(),
        21..=40 => "Monitor for future changes that might reveal a connection.".to_string(),
        41..=60 => "Consider investigating the relationship between these files.".to_string(),
        61..=80 => "Strong recommendation to document the relationship or merge if appropriate.".to_string(),
        81..=100 => "These files are practically identical. Consider merging or clearly documenting their purpose.".to_string(),
        _ => "Consult a quantum computing expert.".to_string(),
    }
}

/// Read file content, handling special case for stdin ('-')
fn read_content(path: &str) -> io::Result<String> {
    if path == "-" {
        let mut buffer = String::new();
        io::stdin().read_to_string(&mut buffer)?;
        Ok(buffer)
    } else {
        fs::read_to_string(path)
    }
}

/// Generate detailed report
fn generate_report(
    file_a: &str,
    file_b: &str,
    hash_a: &str,
    hash_b: &str,
    probability: f64,
    detailed: bool,
) {
    println!("Quantum Entanglement Analysis Report");
    println!("==================================");
    println!("");
    println!("File A: {}", file_a);
    println!("File B: {}", file_b);
    println!("");
    
    if detailed {
        println!("Hash A: {}", hash_a);
        println!("Hash B: {}", hash_b);
        println!("");
    }
    
    println!("Entanglement Probability: {:.1}%", probability);
    println!("");
    
    let (level, description) = get_entanglement_level(probability);
    
    // Add whimsical emoji based on level
    let emoji = match probability as u8 {
        0..=20 => "🌌",
        21..=40 => "⭐",
        41..=60 => "🪐",
        61..=80 => "🪄",
        81..=100 => "🌀",
        _ => "❓",
    };
    
    println!("Status: {} {}!", emoji, level);
    println!("");
    println!("{}", get_status_message(probability));
    println!("");
    println!("Recommendation: {}", get_recommendation(probability));
}

fn main() {
    let matches = Command::new("nightly-quantum-entanglement-checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("Checks if two code snippets are quantum entangled")
        .arg(
            Arg::new("file_a")
                .help("First file to compare (use '-' for stdin)")
                .required(true)
                .index(1),
        )
        .arg(
            Arg::new("file_b")
                .help("Second file to compare (use '-' for stdin)")
                .required(true)
                .index(2),
        )
        .arg(
            Arg::new("report")
                .short('r')
                .long("report")
                .help("Generate detailed report with hashes")
                .action(clap::ArgAction::SetTrue),
        )
        .get_matches();

    let file_a_path = matches.get_one::<String>("file_a").unwrap();
    let file_b_path = matches.get_one::<String>("file_b").unwrap();
    let detailed = matches.get_flag("report");

    // Read file contents
    let content_a = match read_content(file_a_path) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file '{}': {}", file_a_path, e);
            std::process::exit(1);
        }
    };

    let content_b = match read_content(file_b_path) {
        Ok(content) => content,
        Err(e) => {
            eprintln!("Error reading file '{}': {}", file_b_path, e);
            std::process::exit(1);
        }
    };

    // Calculate hashes
    let hash_a = calculate_hash(content_a.as_bytes());
    let hash_b = calculate_hash(content_b.as_bytes());

    // Calculate similarity
    let probability = calculate_similarity(&hash_a, &hash_b);

    // Generate report
    generate_report(file_a_path, file_b_path, &hash_a, &hash_b, probability, detailed);
}
