use std::env;
use std::fs;
use std::path::Path;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() != 3 {
        eprintln!("Usage: {} <file1> <file2>", args[0]);
        process::exit(1);
    }
    
    let file1 = &args[1];
    let file2 = &args[2];
    
    match check_quantum_entanglement(file1, file2) {
        Ok(result) => {
            println!("{}
{}
{}
{}
{}",
                format!("📁 Files: {} and {}", file1, file2),
                format!("🔬 Hash A: {}", result.hash_a),
                format!("🔬 Hash B: {}", result.hash_b),
                format!("🎲 Quantum randomness: {:.6}", result.randomness),
                if result.entangled {
                    "✨ Quantum entanglement detected!"
                } else {
                    "❌ No quantum entanglement found."
                }
            );
        }
        Err(e) => {
            eprintln!("Error: {}", e);
            process::exit(1);
        }
    }
}

struct EntanglementResult {
    hash_a: String,
    hash_b: String,
    randomness: f64,
    entangled: bool,
}

fn check_quantum_entanglement(file1: &str, file2: &str) -> Result<EntanglementResult, String> {
    // Read files
    let content1 = fs::read(file1)
        .map_err(|e| format!("Failed to read file {}: {}", file1, e))?;
    let content2 = fs::read(file2)
        .map_err(|e| format!("Failed to read file {}: {}", file2, e))?;
    
    // Calculate hashes
    let hash_a = calculate_hash(&content1);
    let hash_b = calculate_hash(&content2);
    
    // Check if entangled (hashes match)
    let entangled = hash_a == hash_b;
    
    // Add quantum randomness
    let randomness = quantum_randomness();
    
    Ok(EntanglementResult {
        hash_a,
        hash_b,
        randomness,
        entangled,
    })
}

fn calculate_hash(content: &[u8]) -> String {
    use std::collections::hash_map::DefaultHasher;
    use std::hash::{Hash, Hasher};
    
    let mut hasher = DefaultHasher::new();
    content.hash(&mut hasher);
    let hash = hasher.finish();
    
    // Convert to hex string (first 16 chars for readability)
    format!("{:016x}", hash)
}

fn quantum_randomness() -> f64 {
    // A touch of quantum randomness
    // Using a deterministic pseudo-random for testing purposes
    use std::time::{SystemTime, UNIX_EPOCH};
    
    let duration = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default();
    
    let seed = duration.as_nanos() as f64;
    (seed * 0.123456789) % 1.0
}
