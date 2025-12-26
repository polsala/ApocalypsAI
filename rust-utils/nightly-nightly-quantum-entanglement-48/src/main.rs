use std::env;
use std::collections::HashMap;
use std::time::{SystemTime, UNIX_EPOCH};

const QUANTUM_PREFIX: &str = "Q-ENT";
const WHIMSY_MESSAGES: &[&str] = &[
    "Quantum fluctuations detected in sector 7G",
    "Entanglement field stabilizing...",
    "Reality matrix integrity: nominal",
    "Temporal coherence at optimal levels",
    "Spooky action at a distance confirmed",
    "Heisenberg uncertainty principle: respected",
    "Schrödinger's cat approves this entanglement",
    "Quantum foam density: acceptable",
    "Multiverse alignment: synchronized",
    "Wave function collapse: controlled"
];

#[derive(Debug, Clone)]
struct QuantumParticle {
    id: String,
    timestamp: u64,
    coherence: f64,
}

impl QuantumParticle {
    fn new(base_id: &str) -> Self {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let coherence = calculate_coherence(base_id, timestamp);
        
        QuantumParticle {
            id: format!("{}-{}", base_id, timestamp % 10000),
            timestamp,
            coherence,
        }
    }
}

fn calculate_coherence(base_id: &str, timestamp: u64) -> f64 {
    let mut hash = 0u64;
    for byte in base_id.bytes() {
        hash = hash.wrapping_mul(31).wrapping_add(byte as u64);
    }
    hash = hash.wrapping_mul(timestamp);
    
    // Generate deterministic but "quantum" coherence value
    let quantum_factor = (hash % 1000) as f64 / 1000.0;
    90.0 + (quantum_factor * 10.0)
}

fn generate_entanglement_pair() -> (QuantumParticle, QuantumParticle) {
    let base_id = generate_base_id();
    let particle_a = QuantumParticle::new(&base_id);
    let particle_b = QuantumParticle::new(&base_id);
    (particle_a, particle_b)
}

fn generate_base_id() -> String {
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    
    let random_component = (timestamp % 1000000).to_string();
    let checksum = calculate_checksum(&random_component);
    
    format!("{}-{}-{}", QUANTUM_PREFIX, random_component, checksum)
}

fn calculate_checksum(input: &str) -> String {
    let mut sum = 0u32;
    for byte in input.bytes() {
        sum = sum.wrapping_add(byte as u32);
    }
    format!("{:04X}", sum % 65536)
}

fn verify_entanglement(particle_a: &str, particle_b: &str) -> Option<f64> {
    // Extract base IDs for comparison
    let base_a = extract_base_id(particle_a);
    let base_b = extract_base_id(particle_b);
    
    if base_a == base_b && base_a.starts_with(QUANTUM_PREFIX) {
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        Some(calculate_coherence(&base_a, timestamp))
    } else {
        None
    }
}

fn extract_base_id(particle_id: &str) -> String {
    // Extract the base ID without timestamp suffix
    if let Some(pos) = particle_id.rfind('-') {
        particle_id[..pos].to_string()
    } else {
        particle_id.to_string()
    }
}

fn get_whimsical_message() -> &'static str {
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
    WHIMSY_MESSAGES[(timestamp as usize) % WHIMSY_MESSAGES.len()]
}

fn print_usage() {
    println!("Nightly Quantum Entanglement Checker");
    println!("");
    println!("Usage:");
    println!("  nightly-quantum-entanglement-checker generate    Generate a new entanglement pair");
    println!("  nightly-quantum-entanglement-checker verify <A> <B>  Verify two particles are entangled");
    println!("  nightly-quantum-entanglement-checker status      Check quantum field status");
    println!("");
    println!("Examples:");
    println!("  nightly-quantum-entanglement-checker generate");
    println!("  nightly-quantum-entanglement-checker verify Q-ENT-123456-ABCD Q-ENT-123456-ABCD");
    println!("  nightly-quantum-entanglement-checker status");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_usage();
        return;
    }
    
    match args[1].as_str() {
        "generate" => {
            println!("{}");
            let (particle_a, particle_b) = generate_entanglement_pair();
            println!("Quantum Entanglement Generated!");
            println!("Particle A: {}", particle_a.id);
            println!("Particle B: {}", particle_b.id);
            println!("Coherence level: {:.1}%", particle_a.coherence);
        }
        
        "verify" => {
            if args.len() != 4 {
                println!("Error: verify command requires exactly 2 particle IDs");
                println!("");
                print_usage();
                return;
            }
            
            let particle_a = &args[2];
            let particle_b = &args[3];
            
            if let Some(coherence) = verify_entanglement(particle_a, particle_b) {
                println!("✓ Particles are quantumly entangled!");
                println!("Coherence level: {:.1}%", coherence);
                println!("{}");
            } else {
                println!("✗ Particles are not entangled or invalid format");
                println!("Ensure both particles share the same base ID (e.g., Q-ENT-123456-ABCD)");
            }
        }
        
        "status" => {
            println!("Quantum Field Status: Stable");
            println!("Entanglement Pairs: 42");
            println!("Temporal Coherence: Optimal");
            println!("Reality Integrity: Maintained");
            println!("{}");
        }
        
        _ => {
            println!("Unknown command: {}", args[1]);
            println!("");
            print_usage();
        }
    }
}
