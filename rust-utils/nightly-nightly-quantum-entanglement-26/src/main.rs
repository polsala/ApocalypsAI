use std::env;
use std::process;

/// Quantum entanglement threshold (0.0 to 1.0)
const DEFAULT_THRESHOLD: f64 = 0.7;

/// Calculate quantum hash using a playful algorithm
fn quantum_hash(input: &str) -> u64 {
    let mut hash = 0u64;
    for (i, ch) in input.chars().enumerate() {
        let char_val = ch as u64;
        // Quantum-inspired hash: mix position, character, and cosmic constants
        let quantum_factor = (i as u64 + 1) * 17 + char_val * 31;
        let cosmic_constant = 42; // The answer to everything
        hash = hash.wrapping_add(quantum_factor.wrapping_mul(cosmic_constant));
    }
    
    // Add some quantum randomness (deterministic but looks random)
    let length_factor = input.len() as u64 * 1337;
    hash.wrapping_add(length_factor)
}

/// Calculate entanglement strength between two hashes
fn calculate_entanglement_strength(hash1: u64, hash2: u64) -> f64 {
    if hash1 == hash2 {
        return 1.0; // Perfect entanglement
    }
    
    // Calculate Hamming distance
    let xor_result = hash1 ^ hash2;
    let bit_difference = xor_result.count_ones() as f64;
    let total_bits = 64.0;
    
    // Convert to similarity score (0.0 to 1.0)
    let similarity = 1.0 - (bit_difference / total_bits);
    
    // Apply quantum wave function (make it more dramatic)
    similarity.powf(2.0)
}

/// Get whimsical quantum metaphor based on entanglement strength
fn get_quantum_metaphor(strength: f64) -> &'static str {
    match strength {
        s if s >= 0.9 => "These strings are perfectly entangled across all quantum states!",
        s if s >= 0.7 => "Strong quantum connection detected! Spooky action at a distance confirmed.",
        s if s >= 0.5 => "Moderate entanglement. The quantum fields are in partial harmony.",
        s if s >= 0.3 => "Weak quantum link. Proceed with caution through the quantum foam.",
        _ => "Quantum decoherence detected. These strings exist in separate realities.",
    }
}

/// Display quantum entanglement results
fn display_results(str1: &str, str2: &str, strength: f64, threshold: f64) {
    println!("\n🔬 Quantum Entanglement Analysis Results:\n");
    println!("String 1: \"{}\"", str1);
    println!("String 2: \"{}\"", str2);
    println!("\n📊 Entanglement Strength: {:.1}/1.0", strength);
    
    if strength >= threshold {
        println!("\n✨ Quantum Entanglement Confirmed! ✨");
        println!("{}
", get_quantum_metaphor(strength));
        
        if strength < 1.0 {
            println!("💡 Tip: For perfect entanglement, ensure strings are identical!");
        }
    } else {
        println!("\n⚠️  Quantum Decoherence Detected!");
        println!("{}
", get_quantum_metaphor(strength));
        println!("💡 Tip: Try strings with more similarities for stronger entanglement!");
    }
    
    println!("\n🌌 Remember: Quantum physics is weird, but this tool makes it fun!");
}

/// Interactive mode for user input
fn interactive_mode() {
    println!("\n🚀 Welcome to Quantum Entanglement Checker (Interactive Mode)!");
    println!("Enter two strings to check their quantum connection:\n");
    
    let mut input1 = String::new();
    let mut input2 = String::new();
    
    println!("Enter first string:");
    std::io::stdin().read_line(&mut input1).expect("Failed to read input");
    let input1 = input1.trim();
    
    println!("Enter second string:");
    std::io::stdin().read_line(&mut input2).expect("Failed to read input");
    let input2 = input2.trim();
    
    let threshold = DEFAULT_THRESHOLD;
    run_entanglement_check(input1, input2, threshold);
}

/// Run the entanglement check
fn run_entanglement_check(str1: &str, str2: &str, threshold: f64) {
    let hash1 = quantum_hash(str1);
    let hash2 = quantum_hash(str2);
    let strength = calculate_entanglement_strength(hash1, hash2);
    
    display_results(str1, str2, strength, threshold);
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // Parse command line arguments
    if args.len() < 2 {
        println!("Usage:");
        println!("  cargo run -- <string1> <string2> [options]");
        println!("  cargo run -- --interactive");
        println!("  cargo run -- --help");
        process::exit(1);
    }
    
    // Check for help
    if args.contains(&"--help".to_string()) {
        println!("\n🌌 Quantum Entanglement Checker Help:\n");
        println!("Usage: cargo run -- [OPTIONS] <string1> <string2>");
        println!("\nOptions:");
        println!("  --threshold <value>    Set entanglement threshold (0.0-1.0, default: {:.1})", DEFAULT_THRESHOLD);
        println!("  --interactive         Run in interactive mode");
        println!("  --help                Show this help message");
        println!("\nExamples:");
        println!("  cargo run -- \"Hello\" \"Hello\"");
        println!("  cargo run -- \"Hello\" \"World\" --threshold 0.8");
        println!("  cargo run -- --interactive");
        process::exit(0);
    }
    
    // Check for interactive mode
    if args.contains(&"--interactive".to_string()) {
        interactive_mode();
        return;
    }
    
    // Parse arguments
    if args.len() < 3 {
        eprintln!("Error: Please provide two strings to compare");
        process::exit(1);
    }
    
    let str1 = &args[1];
    let str2 = &args[2];
    
    // Parse threshold if provided
    let mut threshold = DEFAULT_THRESHOLD;
    if args.contains(&"--threshold".to_string()) {
        let threshold_index = args.iter().position(|x| x == "--threshold").unwrap();
        if threshold_index + 1 < args.len() {
            match args[threshold_index + 1].parse::<f64>() {
                Ok(val) if val >= 0.0 && val <= 1.0 => threshold = val,
                _ => {
                    eprintln!("Error: Threshold must be between 0.0 and 1.0");
                    process::exit(1);
                }
            }
        } else {
            eprintln!("Error: --threshold requires a value between 0.0 and 1.0");
            process::exit(1);
        }
    }
    
    // Run the entanglement check
    run_entanglement_check(str1, str2, threshold);
}
