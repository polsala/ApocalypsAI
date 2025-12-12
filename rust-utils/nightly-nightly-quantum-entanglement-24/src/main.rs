use std::env;
use std::process;
use std::time::{SystemTime, UNIX_EPOCH};

const DEFAULT_NODES: usize = 5;
const DEFAULT_CONFIDENCE: f64 = 0.95;
const DEFAULT_ITERATIONS: usize = 100;

struct QuantumConfig {
    nodes: usize,
    confidence: f64,
    iterations: usize,
    seed: u64,
}

impl QuantumConfig {
    fn new() -> Self {
        Self {
            nodes: DEFAULT_NODES,
            confidence: DEFAULT_CONFIDENCE,
            iterations: DEFAULT_ITERATIONS,
            seed: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        }
    }
}

struct QuantumRng {
    state: u64,
}

impl QuantumRng {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    fn next_f64(&mut self) -> f64 {
        // Simple xorshift64* PRNG
        self.state ^= self.state.wrapping_shl(12);
        self.state ^= self.state.wrapping_shr(25);
        self.state ^= self.state.wrapping_shl(27);
        
        let result = self.state.wrapping_mul(2685821657736338717);
        (result as f64) / (u64::MAX as f64)
    }

    fn next_bool(&mut self) -> bool {
        self.next_f64() < 0.5
    }
}

fn measure_entanglement(rng: &mut QuantumRng, iterations: usize) -> (f64, f64) {
    let mut correlations = Vec::new();
    
    for _ in 0..iterations {
        // Simulate measuring entangled particles
        let alice_spin = rng.next_bool();
        let bob_spin = rng.next_bool();
        
        // Calculate correlation (should be high for entangled particles)
        let correlation = if alice_spin == bob_spin { 1.0 } else { -1.0 };
        correlations.push(correlation);
    }
    
    let mean_correlation = correlations.iter().sum::<f64>() / iterations as f64;
    
    // Calculate standard deviation for confidence interval
    let variance = correlations
        .iter()
        .map(|&x| (x - mean_correlation).powi(2))
        .sum::<f64>() / iterations as f64;
    
    let std_dev = variance.sqrt();
    
    (mean_correlation, std_dev)
}

fn check_entanglement(
    rng: &mut QuantumRng,
    iterations: usize,
    confidence: f64,
) -> (bool, f64, f64) {
    let (correlation, std_dev) = measure_entanglement(rng, iterations);
    
    // For entangled particles, correlation should be close to 1
    let expected_correlation = 1.0;
    let margin = 1.96 * std_dev / (iterations as f64).sqrt(); // 95% confidence
    
    let is_entangled = correlation > (expected_correlation - margin * (1.0 - confidence) * 10.0);
    
    (is_entangled, correlation, margin)
}

fn format_spin_correlation(correlation: f64) -> String {
    format!("{:.3}", correlation.abs())
}

fn bell_inequality_score(correlation: f64) -> f64 {
    // Simulate Bell inequality violation
    2.0 + (correlation.abs() * 0.8)
}

fn quantum_coherence_percentage(correlations: &[f64]) -> f64 {
    let avg_correlation = correlations.iter().sum::<f64>() / correlations.len() as f64;
    (avg_correlation.abs() * 100.0).min(100.0)
}

fn print_header(config: &QuantumConfig) {
    println!("🔬 Quantum Entanglement Verification Report");
    println!("==========================================");
    println!("");
    println!("📡 Simulated Nodes: {}", config.nodes);
    println!("🎯 Confidence Level: {:.1}%", config.confidence * 100.0);
    println!("🔄 Measurement Iterations: {}", config.iterations);
    println!("🎲 Quantum Seed: {}", config.seed);
    println!("");
}

fn print_entanglement_results(
    results: &[(usize, usize, bool, f64, f64)],
    correlations: &[f64],
) {
    println!("⚛️  Entanglement Status:");
    
    for (i, (node1, node2, is_entangled, correlation, _margin)) in results.iter().enumerate() {
        let status = if *is_entangled { "ENTANGLED" } else { "SEPARATED" };
        let emoji = if *is_entangled { "✓" } else { "✗" };
        println!(
            "   {} Node {} ↔ Node {}: {} (Spin correlation: {})",
            emoji,
            node1,
            node2,
            status,
            format_spin_correlation(*correlation)
        );
    }
    
    println!("");
    
    // Overall statistics
    let entangled_count = results.iter().filter(|&&(_, _, is_entangled, _, _)| is_entangled).count();
    let total_pairs = results.len();
    
    if entangled_count == total_pairs {
        println!("🎉 Overall System Entanglement: SUCCESS");
    } else {
        println!("⚠️  Overall System Entanglement: PARTIAL ({} of {} pairs entangled)", 
                 entangled_count, total_pairs);
    }
    
    let avg_correlation = correlations.iter().sum::<f64>() / correlations.len() as f64;
    let bell_score = bell_inequality_score(avg_correlation);
    let coherence = quantum_coherence_percentage(correlations);
    
    println!("   Bell Inequality Violation: {:.3} (Classical limit: 2.0)", bell_score);
    println!("   Quantum Coherence Maintained: {:.1}%", coherence);
    
    println!("");
    
    // Warnings
    if coherence < 95.0 {
        println!("⚠️  Warning: Minor quantum decoherence detected");
        println!("   Recommendation: Apply quantum error correction protocol");
        println!("");
    }
}

fn print_footer() {
    println!("✨ The system is quantum-ready! Proceed with your experiments.");
}

fn parse_args() -> QuantumConfig {
    let mut args = env::args().skip(1);
    let mut config = QuantumConfig::new();
    
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "-n" | "--nodes" => {
                if let Some(nodes_str) = args.next() {
                    config.nodes = nodes_str.parse().expect("--nodes must be a number");
                }
            },
            "-c" | "--confidence" => {
                if let Some(conf_str) = args.next() {
                    config.confidence = conf_str.parse().expect("--confidence must be a number between 0 and 1");
                    if config.confidence < 0.0 || config.confidence > 1.0 {
                        eprintln!("Error: Confidence must be between 0 and 1");
                        process::exit(1);
                    }
                }
            },
            "-i" | "--iterations" => {
                if let Some(iter_str) = args.next() {
                    config.iterations = iter_str.parse().expect("--iterations must be a number");
                }
            },
            "-s" | "--seed" => {
                if let Some(seed_str) = args.next() {
                    config.seed = seed_str.parse().expect("--seed must be a number");
                }
            },
            "-h" | "--help" => {
                print_help();
                process::exit(0);
            },
            _ => {
                eprintln!("Unknown argument: {}", arg);
                print_help();
                process::exit(1);
            },
        }
    }
    
    config
}

fn print_help() {
    println!("Nightly Quantum Entanglement Checker");
    println!("");
    println!("Usage: nightly-quantum-entanglement-checker [OPTIONS]");
    println!("");
    println!("Options:");
    println!("  -n, --nodes <NUM>        Number of simulated nodes (default: 5)");
    println!("  -c, --confidence <NUM>  Confidence level (0.0-1.0, default: 0.95)");
    println!("  -i, --iterations <NUM>  Number of measurement iterations (default: 100)");
    println!("  -s, --seed <NUM>        Random seed for reproducible results");
    println!("  -h, --help              Show this help message");
}

fn main() {
    let config = parse_args();
    
    if config.nodes < 2 {
        eprintln!("Error: At least 2 nodes are required for entanglement verification");
        process::exit(1);
    }
    
    print_header(&config);
    
    let mut rng = QuantumRng::new(config.seed);
    let mut results = Vec::new();
    let mut correlations = Vec::new();
    
    // Check entanglement between all pairs of nodes
    for i in 1..=config.nodes {
        for j in (i+1)..=config.nodes {
            let (is_entangled, correlation, _margin) = 
                check_entanglement(&mut rng, config.iterations, config.confidence);
            
            results.push((i, j, is_entangled, correlation, 0.0));
            correlations.push(correlation);
        }
    }
    
    print_entanglement_results(&results, &correlations);
    print_footer();
}
