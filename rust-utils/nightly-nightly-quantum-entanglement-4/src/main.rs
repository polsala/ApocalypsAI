use std::collections::{HashMap, HashSet};
use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;
use clap::{Arg, Command};
use rayon::prelude::*;

/// Quantum entanglement coefficient calculation
/// Uses a combination of Jaccard similarity and Levenshtein distance
fn calculate_entanglement_coefficient(text1: &str, text2: &str) -> f64 {
    if text1.is_empty() && text2.is_empty() {
        return 1.0;
    }
    if text1.is_empty() || text2.is_empty() {
        return 0.0;
    }

    // Normalize text (remove whitespace, convert to lowercase)
    let norm1 = normalize_text(text1);
    let norm2 = normalize_text(text2);

    // Calculate Jaccard similarity on character sets
    let jaccard = calculate_jaccard_similarity(&norm1, &norm2);

    // Calculate character frequency similarity
    let freq_sim = calculate_frequency_similarity(&norm1, &norm2);

    // Combine metrics with weighted average
    (jaccard * 0.6) + (freq_sim * 0.4)
}

/// Normalize text for comparison
fn normalize_text(text: &str) -> String {
    text.chars()
        .filter(|c| c.is_alphanumeric() || c.is_whitespace())
        .map(|c| c.to_ascii_lowercase())
        .collect()
}

/// Calculate Jaccard similarity between two strings
fn calculate_jaccard_similarity(text1: &str, text2: &str) -> f64 {
    let set1: HashSet<char> = text1.chars().collect();
    let set2: HashSet<char> = text2.chars().collect();
    
    let intersection = set1.intersection(&set2).count();
    let union = set1.union(&set2).count();
    
    if union == 0 {
        0.0
    } else {
        intersection as f64 / union as f64
    }
}

/// Calculate frequency-based similarity
fn calculate_frequency_similarity(text1: &str, text2: &str) -> f64 {
    let freq1 = calculate_char_frequency(text1);
    let freq2 = calculate_char_frequency(text2);
    
    // Calculate cosine similarity between frequency vectors
    let mut dot_product = 0.0;
    let mut norm1 = 0.0;
    let mut norm2 = 0.0;
    
    let all_chars: HashSet<char> = freq1.keys().chain(freq2.keys()).cloned().collect();
    
    for ch in all_chars {
        let f1 = *freq1.get(&ch).unwrap_or(&0.0);
        let f2 = *freq2.get(&ch).unwrap_or(&0.0);
        
        dot_product += f1 * f2;
        norm1 += f1 * f1;
        norm2 += f2 * f2;
    }
    
    if norm1 == 0.0 || norm2 == 0.0 {
        0.0
    } else {
        dot_product / (norm1.sqrt() * norm2.sqrt())
    }
}

/// Calculate character frequency distribution
fn calculate_char_frequency(text: &str) -> HashMap<char, f64> {
    let mut freq: HashMap<char, u32> = HashMap::new();
    let total_chars = text.len() as f64;
    
    for ch in text.chars() {
        *freq.entry(ch).or_insert(0) += 1;
    }
    
    // Convert to relative frequencies
    freq.into_iter()
        .map(|(ch, count)| (ch, count as f64 / total_chars))
        .collect()
}

/// Find all files matching pattern in directory
fn find_files(dir: &Path, pattern: &str, max_depth: usize) -> Result<Vec<PathBuf>, Box<dyn std::error::Error>> {
    let mut files = Vec::new();
    find_files_recursive(dir, pattern, max_depth, 0, &mut files)?;
    Ok(files)
}

fn find_files_recursive(
    dir: &Path,
    pattern: &str,
    max_depth: usize,
    current_depth: usize,
    files: &mut Vec<PathBuf>,
) -> Result<(), Box<dyn std::error::Error>> {
    if current_depth > max_depth {
        return Ok(());
    }

    if !dir.is_dir() {
        return Ok(());
    }

    let entries = fs::read_dir(dir)?;
    for entry in entries {
        let entry = entry?;
        let path = entry.path();
        
        if path.is_dir() {
            find_files_recursive(&path, pattern, max_depth, current_depth + 1, files)?;
        } else if path.is_file() {
            if matches_pattern(&path, pattern) {
                files.push(path);
            }
        }
    }
    
    Ok(())
}

/// Simple pattern matching (supports * wildcard)
fn matches_pattern(path: &Path, pattern: &str) -> bool {
    if pattern == "*" {
        return true;
    }
    
    let file_name = path.file_name()
        .and_then(|n| n.to_str())
        .unwrap_or("");
    
    if pattern.starts_with("*") && pattern.ends_with("*") {
        let inner = &pattern[1..pattern.len()-1];
        file_name.contains(inner)
    } else if pattern.starts_with("*") {
        let suffix = &pattern[1..];
        file_name.ends_with(suffix)
    } else if pattern.ends_with("*") {
        let prefix = &pattern[..pattern.len()-1];
        file_name.starts_with(prefix)
    } else {
        file_name == pattern
    }
}

/// Read file content with error handling
fn read_file_content(path: &Path) -> Result<String, Box<dyn std::error::Error>> {
    let content = fs::read_to_string(path)?;
    Ok(content)
}

/// Quantum entanglement analysis result
#[derive(Debug)]
struct EntanglementResult {
    coefficient: f64,
    file1: PathBuf,
    file2: PathBuf,
}

/// Main analysis function
fn analyze_entanglement(
    dir1: &Path,
    dir2: &Path,
    pattern: &str,
    threshold: f64,
    max_depth: usize,
    verbose: bool,
) -> Result<Vec<EntanglementResult>, Box<dyn std::error::Error>> {
    println!("📡 Scanning directories for quantum signatures...");
    
    let files1 = find_files(dir1, pattern, max_depth)?;
    let files2 = find_files(dir2, pattern, max_depth)?;
    
    if verbose {
        println!("📁 Found {} files in dir1", files1.len());
        println!("📁 Found {} files in dir2", files2.len());
    }
    
    println!("⚛️  Computing quantum wave functions...");
    
    // Read all file contents
    let contents1: HashMap<PathBuf, String> = files1
        .into_par_iter()
        .filter_map(|path| {
            read_file_content(&path)
                .map(|content| (path, content))
                .ok()
        })
        .collect();
    
    let contents2: HashMap<PathBuf, String> = files2
        .into_par_iter()
        .filter_map(|path| {
            read_file_content(&path)
                .map(|content| (path, content))
                .ok()
        })
        .collect();
    
    if verbose {
        println!("📄 Loaded {} files from dir1", contents1.len());
        println!("📄 Loaded {} files from dir2", contents2.len());
    }
    
    // Calculate entanglement coefficients
    let results: Vec<EntanglementResult> = contents1
        .par_iter()
        .flat_map(|(path1, content1)| {
            contents2
                .par_iter()
                .filter_map(|(path2, content2)| {
                    let coefficient = calculate_entanglement_coefficient(content1, content2);
                    if coefficient >= threshold {
                        Some(EntanglementResult {
                            coefficient,
                            file1: path1.clone(),
                            file2: path2.clone(),
                        })
                    } else {
                        None
                    }
                })
                .collect::<Vec<_>>()
        })
        .collect();
    
    Ok(results)
}

/// Format entanglement coefficient as quantum level
fn format_quantum_level(coefficient: f64) -> String {
    if coefficient >= 0.9 {
        format!("{:.2} (ULTRA-STRONG) ⚛️", coefficient)
    } else if coefficient >= 0.7 {
        format!("{:.2} (STRONG) 🚀", coefficient)
    } else if coefficient >= 0.5 {
        format!("{:.2} (MODERATE) 🌀", coefficient)
    } else if coefficient >= 0.3 {
        format!("{:.2} (WEAK) 💫", coefficient)
    } else {
        format!("{:.2} (TRACE) ✨", coefficient)
    }
}

/// Print results in quantum-themed format
fn print_results(results: &[EntanglementResult]) {
    println!("\nResults:");
    println!("--------\n");
    
    if results.is_empty() {
        println!("❌ No Quantum Entanglement Detected!");
        println!("\n✨ The codebases appear to be quantumly isolated.");
        println!("💡 This is actually good - no code duplication detected!");
        return;
    }
    
    // Calculate average coefficient
    let avg_coefficient: f64 = results.iter().map(|r| r.coefficient).sum::<f64>() / results.len() as f64;
    
    println!("✅ Quantum Entanglement Detected!");
    println!("\nEntanglement Coefficient: {}", format_quantum_level(avg_coefficient));
    
    // Sort by coefficient descending
    let mut sorted_results = results.to_vec();
    sorted_results.sort_by(|a, b| b.coefficient.partial_cmp(&a.coefficient).unwrap());
    
    println!("\nMost entangled files:");
    for result in sorted_results.iter().take(5) {
        let file1_name = result.file1.file_name().unwrap_or_default().to_string_lossy();
        let file2_name = result.file2.file_name().unwrap_or_default().to_string_lossy();
        println!("- {} ↔ {} ({:.0}%)", file1_name, file2_name, result.coefficient * 100.0);
    }
    
    if avg_coefficient > 0.8 {
        println!("\n⚠️  Warning: Ultra-high probability of code duplication detected!");
        println!("💡 Recommendation: Consider refactoring shared logic into a common module.");
    } else if avg_coefficient > 0.6 {
        println!("\n⚠️  Warning: High probability of code duplication detected!");
        println!("💡 Recommendation: Consider refactoring shared logic into a common module.");
    } else if avg_coefficient > 0.4 {
        println!("\n⚠️  Notice: Moderate similarity detected.");
        println!("💡 Consider reviewing for potential refactoring opportunities.");
    }
    
    println!("\n✨ Quantum analysis complete!");
}

fn main() {
    println!("🔬 Quantum Entanglement Detector v1.0");
    println!("========================================\n");
    
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0")
        .author("ApocalypsAI")
        .about("Checks for quantum entanglement between two codebases")
        .arg(
            Arg::new("dir1")
                .short('1')
                .long("dir1")
                .value_name("DIR")
                .help("First directory to compare")
                .required(true)
        )
        .arg(
            Arg::new("dir2")
                .short('2')
                .long("dir2")
                .value_name("DIR")
                .help("Second directory to compare")
                .required(true)
        )
        .arg(
            Arg::new("pattern")
                .short('p')
                .long("pattern")
                .value_name("PATTERN")
                .help("File pattern to match (e.g., \"*.rs\")")
                .default_value("*")
        )
        .arg(
            Arg::new("threshold")
                .short('t')
                .long("threshold")
                .value_name("THRESHOLD")
                .help("Minimum entanglement threshold (0.0-1.0)")
                .default_value("0.5")
        )
        .arg(
            Arg::new("max-depth")
                .short('d')
                .long("max-depth")
                .value_name("DEPTH")
                .help("Maximum directory depth to scan")
                .default_value("10")
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose logging")
                .action(clap::ArgAction::SetTrue)
        )
        .get_matches();
    
    let dir1 = Path::new(matches.get_one::<String>("dir1").unwrap());
    let dir2 = Path::new(matches.get_one::<String>("dir2").unwrap());
    let pattern = matches.get_one::<String>("pattern").unwrap();
    let threshold: f64 = matches.get_one::<String>("threshold").unwrap().parse()
        .expect("Threshold must be a valid number between 0.0 and 1.0");
    let max_depth: usize = matches.get_one::<String>("max-depth").unwrap().parse()
        .expect("Max depth must be a valid integer");
    let verbose = matches.get_flag("verbose");
    
    if threshold < 0.0 || threshold > 1.0 {
        eprintln!("❌ Error: Threshold must be between 0.0 and 1.0");
        std::process::exit(1);
    }
    
    let start_time = Instant::now();
    
    match analyze_entanglement(dir1, dir2, pattern, threshold, max_depth, verbose) {
        Ok(results) => {
            let duration = start_time.elapsed();
            print_results(&results);
            println!("\n⏱️  Analysis completed in {:.2?}", duration);
            println!("📊 Found {} entangled file pairs", results.len());
        }
        Err(e) => {
            eprintln!("❌ Error during analysis: {}", e);
            std::process::exit(1);
        }
    }
}
