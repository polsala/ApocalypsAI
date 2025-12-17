use clap::{Parser, ValueEnum};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::Path;
use std::time::Instant;

/// Quantum-inspired code entanglement checker
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// First file to compare
    #[arg(short, long)]
    file1: Option<String>,

    /// Second file to compare
    #[arg(short, long)]
    file2: Option<String>,

    /// First text string to compare
    #[arg(short, long, conflicts_with = "file1")]
    text1: Option<String>,

    /// Second text string to compare
    #[arg(short, long, conflicts_with = "file2")]
    text2: Option<String>,

    /// Quantum uncertainty factor (0.0 to 1.0)
    #[arg(short, long, default_value = "0.1", value_parser = clap::value_parser!(f64).range(0.0..=1.0))]
    uncertainty: f64,

    /// Output detailed report to JSON file
    #[arg(short, long)]
    report: Option<String>,

    /// Output format
    #[arg(short, long, value_enum, default_value_t = OutputFormat::Text)]
    format: OutputFormat,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}

#[derive(ValueEnum, Clone, Debug)]
enum OutputFormat {
    Text,
    Json,
}

#[derive(Serialize, Deserialize)]
struct QuantumReport {
    source_a: String,
    source_b: String,
    hash_a: String,
    hash_b: String,
    hamming_distance: u32,
    similarity_score: f64,
    quantum_threshold: f64,
    entangled: bool,
    confidence: String,
    recommendation: String,
    processing_time_ms: u128,
}

fn main() {
    let args = Args::parse();

    // Validate arguments
    if args.file1.is_none() && args.text1.is_none() {
        eprintln!("Error: Must specify either --file1 or --text1");
        std::process::exit(1);
    }
    if args.file2.is_none() && args.text2.is_none() {
        eprintln!("Error: Must specify either --file2 or --text2");
        std::process::exit(1);
    }

    let start_time = Instant::now();

    // Get source content
    let (source_a, content_a) = match &args.file1 {
        Some(file_path) => {
            let path = Path::new(file_path);
            if !path.exists() {
                eprintln!("Error: File {} does not exist", file_path);
                std::process::exit(1);
            }
            let content = fs::read_to_string(path).expect("Failed to read file");
            (file_path.clone(), content)
        }
        None => ("<text_input>".to_string(), args.text1.clone().unwrap_or_default()),
    };

    let (source_b, content_b) = match &args.file2 {
        Some(file_path) => {
            let path = Path::new(file_path);
            if !path.exists() {
                eprintln!("Error: File {} does not exist", file_path);
                std::process::exit(1);
            }
            let content = fs::read_to_string(path).expect("Failed to read file");
            (file_path.clone(), content)
        }
        None => ("<text_input>".to_string(), args.text2.clone().unwrap_or_default()),
    };

    // Generate hashes
    let hash_a = generate_hash(&content_a);
    let hash_b = generate_hash(&content_b);

    // Calculate quantum metrics
    let hamming_distance = calculate_hamming_distance(&hash_a, &hash_b);
    let similarity_score = calculate_similarity_score(hamming_distance);
    let quantum_threshold = (1.0 - args.uncertainty) * 100.0;
    let entangled = similarity_score >= quantum_threshold;

    let confidence = determine_confidence(similarity_score);
    let recommendation = generate_recommendation(entangled, similarity_score);

    let processing_time = start_time.elapsed().as_millis();

    // Create quantum report
    let report = QuantumReport {
        source_a: source_a.clone(),
        source_b: source_b.clone(),
        hash_a: format_hash(&hash_a),
        hash_b: format_hash(&hash_b),
        hamming_distance,
        similarity_score,
        quantum_threshold,
        entangled,
        confidence: confidence.clone(),
        recommendation: recommendation.clone(),
        processing_time_ms: processing_time,
    };

    // Output results
    match args.format {
        OutputFormat::Text => print_text_report(&report, args.verbose),
        OutputFormat::Json => print_json_report(&report),
    }

    // Save report if requested
    if let Some(report_path) = args.report {
        save_report(&report, &report_path);
        if args.verbose {
            println!("\n📄 Report saved to: {}", report_path);
        }
    }

    // Exit with appropriate code
    std::process::exit(if entangled { 0 } else { 1 });
}

fn generate_hash(content: &str) -> [u8; 32] {
    let mut hasher = Sha256::new();
    hasher.update(content.as_bytes());
    let result = hasher.finalize();
    let mut hash = [0u8; 32];
    hash.copy_from_slice(&result);
    hash
}

fn calculate_hamming_distance(hash_a: &[u8; 32], hash_b: &[u8; 32]) -> u32 {
    let mut distance = 0;
    for i in 0..32 {
        let xor = hash_a[i] ^ hash_b[i];
        distance += xor.count_ones();
    }
    distance
}

fn calculate_similarity_score(hamming_distance: u32) -> f64 {
    let max_distance = 32 * 8; // 256 bits total
    let dissimilarity = hamming_distance as f64 / max_distance as f64;
    (1.0 - dissimilarity) * 100.0
}

fn determine_confidence(similarity_score: f64) -> String {
    if similarity_score >= 95.0 {
        "VERY_HIGH".to_string()
    } else if similarity_score >= 85.0 {
        "HIGH".to_string()
    } else if similarity_score >= 70.0 {
        "MEDIUM".to_string()
    } else if similarity_score >= 50.0 {
        "LOW".to_string()
    } else {
        "VERY_LOW".to_string()
    }
}

fn generate_recommendation(entangled: bool, similarity_score: f64) -> String {
    if entangled {
        if similarity_score >= 95.0 {
            "These code snippets are quantumly entangled with near-perfect similarity. They are likely identical or differ only in insignificant ways (whitespace, comments, etc.).".to_string()
        } else if similarity_score >= 85.0 {
            "Quantum entanglement detected with high confidence. These snippets share substantial similarities and may represent the same logic with minor variations.".to_string()
        } else {
            "Weak quantum entanglement detected. These snippets show some similarity but may represent different implementations of similar concepts.".to_string()
        }
    } else {
        "No quantum entanglement detected. These code snippets are sufficiently different and likely represent distinct implementations or unrelated code.".to_string()
    }
}

fn format_hash(hash: &[u8; 32]) -> String {
    hash.iter().map(|b| format!("{:02x}", b)).collect()
}

fn print_text_report(report: &QuantumReport, verbose: bool) {
    println!("🔬 Quantum Entanglement Analysis Report");
    println!("==========================================");
    println!("");
    
    if verbose {
        println!("Source A: {}", report.source_a);
        println!("Source B: {}", report.source_b);
        println!("");
    }
    
    println!("Hash A: {}", &report.hash_a[..16]);
    println!("Hash B: {}", &report.hash_b[..16]);
    println!("");
    
    println!("Hamming Distance: {}", report.hamming_distance);
    println!("Similarity Score: {:.3}%", report.similarity_score);
    println!("Quantum Threshold: {:.1}%", report.quantum_threshold);
    println!("");
    
    if report.entangled {
        println!("✅ QUANTUM ENTANGLEMENT DETECTED!");
    } else {
        println!("❌ NO QUANTUM ENTANGLEMENT");
    }
    
    println!("Confidence Level: {} ({:.1}%)", report.confidence, report.similarity_score);
    println!("");
    println!("Recommendation: {}");
    println!("{}", report.recommendation);
    
    if verbose {
        println!("");
        println!("⏱️  Processing Time: {} ms", report.processing_time_ms);
    }
}

fn print_json_report(report: &QuantumReport) {
    println!("{}", serde_json::to_string_pretty(report).unwrap());
}

fn save_report(report: &QuantumReport, path: &str) {
    let json = serde_json::to_string_pretty(report).unwrap();
    fs::write(path, json).expect("Failed to write report file");
}
