use std::env;
use std::process;
use std::time::{Duration, Instant};
use std::sync::Arc;
use std::collections::HashMap;

// Simple deterministic RNG for reproducible tests
#[derive(Debug)]
struct DeterministicRng {
    state: u64,
}

impl DeterministicRng {
    fn new(seed: u64) -> Self {
        Self { state: seed }
    }
    
    fn next_f64(&mut self) -> f64 {
        // Linear congruential generator
        self.state = self.state.wrapping_mul(1664525).wrapping_add(1013904223);
        (self.state % 1000) as f64 / 1000.0
    }
}

#[derive(Debug, Clone, PartialEq)]
enum EntanglementStatus {
    Entangled,
    Weak,
    Broken,
}

impl EntanglementStatus {
    fn from_coherence(coherence: f64) -> Self {
        if coherence >= 0.75 {
            EntanglementStatus::Entangled
n        } else if coherence >= 0.5 {
            EntanglementStatus::Weak
        } else {
            EntanglementStatus::Broken
        }
    }
    
    fn emoji(&self) -> &'static str {
        match self {
            EntanglementStatus::Entangled => "✨",
            EntanglementStatus::Weak => "⚠️",
            EntanglementStatus::Broken => "❌",
        }
    }
    
    fn description(&self) -> &'static str {
        match self {
            EntanglementStatus::Entangled => "ENTANGLED",
            EntanglementStatus::Weak => "WEAK",
            EntanglementStatus::Broken => "BROKEN",
        }
    }
}

#[derive(Debug)]
struct QuantumChecker {
    nodes: usize,
    distance: f64,
    threshold: f64,
    rng: DeterministicRng,
}

impl QuantumChecker {
    fn new(nodes: usize, distance: f64, threshold: f64) -> Self {
        Self {
            nodes,
            distance,
            threshold,
            rng: DeterministicRng::new(42), // Deterministic seed
        }
    }
    
    fn calculate_coherence(&mut self, node_a: usize, node_b: usize) -> f64 {
        let distance_between = ((node_b as i32 - node_a as i32).abs() as f64) * self.distance;
        
        // Base coherence decreases with distance
        let base_coherence = 1.0 / (1.0 + distance_between / 1000.0);
        
        // Add some quantum noise
        let noise = self.rng.next_f64() * 0.2 - 0.1; // -0.1 to +0.1
        
        // Ensure coherence stays between 0 and 1
        (base_coherence + noise).max(0.0).min(1.0)
    }
    
    fn verify_entanglement(&mut self) -> Vec<(usize, usize, f64, EntanglementStatus)> {
        let mut results = Vec::new();
        
        for i in 0..self.nodes {
            for j in (i + 1)..self.nodes {
                let coherence = self.calculate_coherence(i, j);
                let status = EntanglementStatus::from_coherence(coherence);
                results.push((i, j, coherence, status));
            }
        }
        
        results
    }
    
    fn calculate_network_health(&self, results: &[(usize, usize, f64, EntanglementStatus)]) -> f64 {
        let total_coherence: f64 = results.iter().map(|(_, _, c, _)| c).sum();
        let max_possible = results.len() as f64;
        
        if max_possible == 0.0 {
            0.0
        } else {
            (total_coherence / max_possible) * 100.0
        }
    }
    
    fn get_recommendation(&self, health: f64) -> String {
        if health >= 75.0 {
            "Quantum network is in excellent condition! 🎉".to_string()
        } else if health >= 50.0 {
            "Deploy quantum repeaters for better coherence! 🔭".to_string()
        } else if health >= 25.0 {
            "Consider recalibrating quantum entanglers! 🔧".to_string()
        } else {
            "Emergency protocol: Quantum network severely degraded! 🚨".to_string()
        }
    }
    
    fn run(&mut self) -> Duration {
        println!("🔬 Quantum Entanglement Checker Initializing...\n");
        
        println!("📡 Establishing quantum links between {} nodes...", self.nodes);
        
        // Show node positions
        let positions: Vec<String> = (0..self.nodes)
            .map(|i| format!("{}km", i as f64 * self.distance))
            .collect();
        println!("📍 Node positions: [{}]", positions.join(", "));
        println!("\n🧪 Running entanglement verification...\n");
        
        let start_time = Instant::now();
        let results = self.verify_entanglement();
        let duration = start_time.elapsed();
        
        // Display results
        for (i, j, coherence, status) in &results {
            println!(
                "Node {} ↔ Node {}: {} {} (coherence: {:.2})",
                i, j, status.emoji(), status.description(), coherence
            );
        }
        
        println!("\n".to_string());
        
        // Calculate and display network health
        let health = self.calculate_network_health(&results);
        println!("Overall quantum network health: {:.0}% {}", health, "✨");
        
        // Provide recommendation
        let recommendation = self.get_recommendation(health);
        println!("Recommendation: {}", recommendation);
        
        duration
    }
}

fn parse_args() -> (usize, f64, f64) {
    let args: Vec<String> = env::args().collect();
    
    let mut nodes = 5;
    let mut distance = 1000.0;
    let mut threshold = 0.7;
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "-n" | "--nodes" => {
                if i + 1 < args.len() {
                    nodes = args[i + 1].parse().unwrap_or(5);
                    i += 1;
                }
            },
            "-d" | "--distance" => {
                if i + 1 < args.len() {
                    distance = args[i + 1].parse().unwrap_or(1000.0);
                    i += 1;
                }
            },
            "-t" | "--threshold" => {
                if i + 1 < args.len() {
                    threshold = args[i + 1].parse().unwrap_or(0.7);
                    i += 1;
                }
            },
            "-h" | "--help" => {
                print_help();
                process::exit(0);
            },
            _ => {},
        }
        i += 1;
    }
    
    // Validate inputs
    if nodes < 2 {
        eprintln!("Error: Number of nodes must be at least 2");
        process::exit(1);
    }
    
    if distance <= 0.0 {
        eprintln!("Error: Distance must be positive");
        process::exit(1);
    }
    
    if threshold < 0.0 || threshold > 1.0 {
        eprintln!("Error: Threshold must be between 0.0 and 1.0");
        process::exit(1);
    }
    
    (nodes, distance, threshold)
}

fn print_help() {
    println!("\nQuantum Entanglement Checker\n");
    println!("Usage: quantum_checker [OPTIONS]\n");
    println!("Options:");
    println!("  -n, --nodes <NUM>      Number of simulated nodes (default: 5)");
    println!("  -d, --distance <KM>    Distance between nodes in kilometers (default: 1000)");
    println!("  -t, --threshold <VAL>  Entanglement threshold (0.0-1.0, default: 0.7)");
    println!("  -h, --help             Show this help message\n");
    println!("Examples:");
    println!("  quantum_checker");
    println!("  quantum_checker --nodes 10 --distance 5000 --threshold 0.8");
}

fn main() {
    let (nodes, distance, threshold) = parse_args();
    
    let mut checker = QuantumChecker::new(nodes, distance, threshold);
    let duration = checker.run();
    
    println!("\n⏱️  Verification completed in {:.2?}", duration);
}
