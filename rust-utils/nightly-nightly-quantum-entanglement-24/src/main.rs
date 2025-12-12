use std::env;
use std::time::{SystemTime, UNIX_EPOCH};
use std::collections::HashMap;

/// Quantum state representation
#[derive(Debug, Clone, PartialEq)]
enum QuantumState {
    SpinUp,
    SpinDown,
}

/// Quantum particle with entanglement properties
#[derive(Debug, Clone)]
struct QuantumParticle {
    id: String,
    state: QuantumState,
    entangled_with: Option<String>,
}

impl QuantumParticle {
    fn new(id: String) -> Self {
        Self {
            id,
            state: QuantumState::SpinUp, // Default state
            entangled_with: None,
        }
    }

    fn entangle_with(&mut self, other_id: String) {
        self.entangled_with = Some(other_id);
    }

    fn measure(&mut self) -> QuantumState {
        // Quantum measurement collapses the wave function
        // If entangled, ensure opposite spin to partner
        self.state = if self.state == QuantumState::SpinUp {
            QuantumState::SpinDown
        } else {
            QuantumState::SpinUp
        };
        self.state.clone()
    }
}

/// Quantum entanglement simulator
struct QuantumEntanglementSimulator {
    particles: HashMap<String, QuantumParticle>,
}

impl QuantumEntanglementSimulator {
    fn new() -> Self {
        Self {
            particles: HashMap::new(),
        }
    }

    fn create_particle(&mut self, id: String) {
        self.particles.insert(id.clone(), QuantumParticle::new(id));
    }

    fn entangle_particles(&mut self, id_a: &str, id_b: &str) -> Result<(), String> {
        if !self.particles.contains_key(id_a) || !self.particles.contains_key(id_b) {
            return Err("One or both particles do not exist".to_string());
        }

        self.particles.get_mut(id_a).unwrap().entangle_with(id_b.to_string());
        self.particles.get_mut(id_b).unwrap().entangle_with(id_a.to_string());
        Ok(())
    }

    fn measure_correlation(&mut self, id_a: &str, id_b: &str, iterations: usize) -> Result<f64, String> {
        if !self.particles.contains_key(id_a) || !self.particles.contains_key(id_b) {
            return Err("One or both particles do not exist".to_string());
        }

        let mut correlations = 0;
        let mut measurements_a = Vec::new();
        let mut measurements_b = Vec::new();

        for _ in 0..iterations {
            // Measure both particles
            let measurement_a = self.particles.get_mut(id_a).unwrap().measure();
            let measurement_b = self.particles.get_mut(id_b).unwrap().measure();
            
            measurements_a.push(measurement_a);
            measurements_b.push(measurement_b);
        }

        // Count anti-correlations (entangled particles should have opposite spins)
        for i in 0..iterations {
            if measurements_a[i] != measurements_b[i] {
                correlations += 1;
            }
        }

        Ok(correlations as f64 / iterations as f64)
    }

    fn generate_quantum_random(&self, count: usize) -> Vec<u64> {
        let mut random_numbers = Vec::new();
        
        for i in 0..count {
            // Use system time as a quantum-like random source
            let now = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_nanos();
            
            // Mix with particle states for extra quantumness
            let mut hash = now;
            for (j, particle) in self.particles.iter().enumerate() {
                hash ^= particle.1.id.len() as u128 * (j + 1) as u128;
            }
            
            // Convert to u64 and add some quantum noise
            let quantum_noise = (hash ^ (hash >> 32)) as u64;
            random_numbers.push(quantum_noise ^ (i as u64 * 1337));
        }
        
        random_numbers
    }
}

fn print_usage() {
    println!("🔮 Quantum Entanglement Checker v1.0.0");
    println!("");
    println!("Usage:");
    println!("  nightly-quantum-entanglement-checker --node-a <NODE_A> --node-b <NODE_B>");
    println!("  nightly-quantum-entanglement-checker --generate-random --count <COUNT>");
    println!("  nightly-quantum-entanglement-checker --spooky-test --iterations <ITERATIONS>");
    println!("  nightly-quantum-entanglement-checker --help");
    println!("");
    println!("Commands:");
    println!("  --node-a <NODE_A>        First node for entanglement check");
    println!("  --node-b <NODE_B>        Second node for entanglement check");
    println!("  --generate-random        Generate quantum-safe random numbers");
    println!("  --count <COUNT>          Number of random numbers to generate");
    println!("  --spooky-test            Run spooky correlation test");
    println!("  --iterations <ITERATIONS> Number of iterations for spooky test");
    println!("  --help                   Show this help message");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 || args.contains(&"--help".to_string()) {
        print_usage();
        return;
    }

    let mut simulator = QuantumEntanglementSimulator::new();
    
    // Create some default particles
    simulator.create_particle("node1".to_string());
    simulator.create_particle("node2".to_string());
    simulator.create_particle("node3".to_string());
    simulator.create_particle("node4".to_string());
    
    // Entangle default particles
    simulator.entangle_particles("node1", "node2").unwrap();
    simulator.entangle_particles("node3", "node4").unwrap();

    // Parse command line arguments
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--node-a" => {
                if i + 1 < args.len() {
                    let node_a = &args[i + 1];
                    i += 1;
                    
                    if i + 1 < args.len() && args[i + 1] == "--node-b" {
                        i += 2;
                        if i < args.len() {
                            let node_b = &args[i];
                            
                            // Check if nodes exist, create if needed
                            if !simulator.particles.contains_key(node_a) {
                                simulator.create_particle(node_a.clone());
                            }
                            if !simulator.particles.contains_key(node_b) {
                                simulator.create_particle(node_b.clone());
                            }
                            
                            // Entangle nodes if not already entangled
                            if simulator.entangle_particles(node_a, node_b).is_ok() {
                                println!("🔮 Quantum Entanglement Checker v1.0.0");
                                println!("");
                                println!("Node A: {}", node_a);
                                println!("Node B: {}", node_b);
                                
                                // Measure correlation
                                match simulator.measure_correlation(node_a, node_b, 1000) {
                                    Ok(correlation) => {
                                        if correlation > 0.9 {
                                            println!("Entanglement Status: ✨ SPOOKILY CORRELATED ✨");
                                        } else {
                                            println!("Entanglement Status: ❌ NOT ENTANGLED ❌");
                                        }
                                        println!("Correlation Coefficient: {:.3} (spooky af)", correlation);
                                        println!("Measurement Consistency: {:.0}%", correlation * 100.0);
                                    }
                                    Err(e) => {
                                        println!("Error: {}", e);
                                    }
                                }
                                
                                println!("");
                                println!("\"The universe is under no obligation to make sense to you.\" - Neil deGrasse Tyson");
                            }
                        }
                    }
                }
            }
            "--generate-random" => {
                i += 1;
                if i < args.len() && args[i] == "--count" {
                    i += 1;
                    if i < args.len() {
                        if let Ok(count) = args[i].parse::<usize>() {
                            let random_numbers = simulator.generate_quantum_random(count);
                            println!("🔮 Generated {} quantum-safe random numbers:", count);
                            for (idx, num) in random_numbers.iter().enumerate() {
                                println!("  {}: {}", idx + 1, num);
                            }
                        } else {
                            println!("Error: Count must be a number");
                        }
                    }
                }
            }
            "--spooky-test" => {
                i += 1;
                if i < args.len() && args[i] == "--iterations" {
                    i += 1;
                    if i < args.len() {
                        if let Ok(iterations) = args[i].parse::<usize>() {
                            println!("🔮 Running spooky correlation test with {} iterations...", iterations);
                            
                            match simulator.measure_correlation("node1", "node2", iterations) {
                                Ok(correlation) => {
                                    println!("Spooky Test Result:");
                                    println!("  Correlation: {:.4}", correlation);
                                    if correlation > 0.95 {
                                        println!("  Status: ✨ QUANTUMLY ENTANGLED ✨");
                                    } else {
                                        println!("  Status: ❌ CLASSICALLY CORRELATED ❌");
                                    }
                                }
                                Err(e) => {
                                    println!("Error: {}", e);
                                }
                            }
                        } else {
                            println!("Error: Iterations must be a number");
                        }
                    }
                }
            }
            _ => {
                println!("Unknown option: {}", args[i]);
                print_usage();
                return;
            }
        }
        i += 1;
    }
}
