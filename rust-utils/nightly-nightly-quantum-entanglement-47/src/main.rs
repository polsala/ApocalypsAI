use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::{self, Write};
use std::time::{Duration, Instant};
use rand::Rng;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum SpinState {
    Up,
    Down,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum Polarization {
    Horizontal,
    Vertical,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum ColorState {
    Red,
    Green,
    Blue,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
enum PositionState {
    Dimension1,
    Dimension2,
    Dimension3,
    Dimension4,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct QuantumParticle {
    id: u32,
    spin: SpinState,
    polarization: Polarization,
    color: ColorState,
    position: PositionState,
    is_observed: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct EntangledPair {
    particle_a: QuantumParticle,
    particle_b: QuantumParticle,
    entanglement_strength: f64,
}

#[derive(Debug, Serialize, Deserialize)]
struct SimulationResult {
    timestamp: String,
    pairs_generated: usize,
    observations: Vec<Observation>,
    teleportations: Vec<Teleportation>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Observation {
    pair_id: u32,
    observed_particle: u32,
    observed_state: String,
    collapsed_state: String,
    spooky_action: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct Teleportation {
    source_particle: u32,
    target_particle: u32,
    success: bool,
    fidelity: f64,
}

struct QuantumSimulator {
    rng: rand::rngs::ThreadRng,
    pairs: Vec<EntangledPair>,
    results: SimulationResult,
}

impl QuantumSimulator {
    fn new() -> Self {
        Self {
            rng: rand::thread_rng(),
            pairs: Vec::new(),
            results: SimulationResult {
                timestamp: chrono::Utc::now().to_rfc3339(),
                pairs_generated: 0,
                observations: Vec::new(),
                teleportations: Vec::new(),
            },
        }
    }

    fn generate_entangled_pair(&mut self) -> EntangledPair {
        let id = self.pairs.len() as u32 + 1;
        
        // Generate random quantum states
        let spin_a = if self.rng.gen_bool(0.5) { SpinState::Up } else { SpinState::Down };
        let polarization_a = if self.rng.gen_bool(0.5) { Polarization::Horizontal } else { Polarization::Vertical };
        let color_a = match self.rng.gen_range(0..3) {
            0 => ColorState::Red,
            1 => ColorState::Green,
            _ => ColorState::Blue,
        };
        let position_a = match self.rng.gen_range(0..4) {
            0 => PositionState::Dimension1,
            1 => PositionState::Dimension2,
            2 => PositionState::Dimension3,
            _ => PositionState::Dimension4,
        };

        // Create entangled partner with opposite states
        let spin_b = match spin_a {
            SpinState::Up => SpinState::Down,
            SpinState::Down => SpinState::Up,
        };
        let polarization_b = match polarization_a {
            Polarization::Horizontal => Polarization::Vertical,
            Polarization::Vertical => Polarization::Horizontal,
        };
        let color_b = match color_a {
            ColorState::Red => ColorState::Blue,
            ColorState::Green => ColorState::Red,
            ColorState::Blue => ColorState::Green,
        };
        let position_b = match position_a {
            PositionState::Dimension1 => PositionState::Dimension4,
            PositionState::Dimension2 => PositionState::Dimension3,
            PositionState::Dimension3 => PositionState::Dimension2,
            PositionState::Dimension4 => PositionState::Dimension1,
        };

        let pair = EntangledPair {
            particle_a: QuantumParticle {
                id: id * 2 - 1,
                spin: spin_a,
                polarization: polarization_a,
                color: color_a,
                position: position_a,
                is_observed: false,
            },
            particle_b: QuantumParticle {
                id: id * 2,
                spin: spin_b,
                polarization: polarization_b,
                color: color_b,
                position: position_b,
                is_observed: false,
            },
            entanglement_strength: self.rng.gen_range(0.8..=1.0),
        };

        self.pairs.push(pair.clone());
        self.results.pairs_generated += 1;
        
        pair
    }

    fn observe_particle(&mut self, pair_index: usize, observe_a: bool) -> Option<Observation> {
        let pair = self.pairs.get_mut(pair_index)?;
        
        let (observed_particle, other_particle) = if observe_a {
            (&mut pair.particle_a, &mut pair.particle_b)
        } else {
            (&mut pair.particle_b, &mut pair.particle_a)
        };

        if observed_particle.is_observed {
            return None;
        }

        observed_particle.is_observed = true;
        
        // Collapse the entangled partner
        if !other_particle.is_observed {
            other_particle.is_observed = true;
        }

        let observed_state = format!(
            "Particle {} [Spin: {:?}, Pol: {:?}, Color: {:?}, Pos: {:?}]",
            observed_particle.id, observed_particle.spin, observed_particle.polarization,
            observed_particle.color, observed_particle.position
        );

        let collapsed_state = format!(
            "Particle {} [Spin: {:?}, Pol: {:?}, Color: {:?}, Pos: {:?}]",
            other_particle.id, other_particle.spin, other_particle.polarization,
            other_particle.color, other_particle.position
        );

        let observation = Observation {
            pair_id: (pair_index as u32) + 1,
            observed_particle: observed_particle.id,
            observed_state,
            collapsed_state,
            spooky_action: true,
        };

        self.results.observations.push(observation.clone());
        Some(observation)
    }

    fn quantum_teleportation(&mut self, source_id: u32, target_id: u32) -> Option<Teleportation> {
        let source_pair = self.pairs.iter_mut().find(|p| {
            p.particle_a.id == source_id || p.particle_b.id == source_id
        })?;

        let target_pair = self.pairs.iter_mut().find(|p| {
            p.particle_a.id == target_id || p.particle_b.id == target_id
        })?;

        let source_particle = if source_pair.particle_a.id == source_id {
            &source_pair.particle_a
        } else {
            &source_pair.particle_b
        };

        let target_particle = if target_pair.particle_a.id == target_id {
            &mut target_pair.particle_a
        } else {
            &mut target_pair.particle_b
        };

        // Calculate teleportation fidelity based on entanglement strength
        let fidelity = (source_pair.entanglement_strength + target_pair.entanglement_strength) / 2.0;
        let success = self.rng.gen_bool(fidelity);

        if success {
            // Teleport the quantum state
            target_particle.spin = source_particle.spin;
            target_particle.polarization = source_particle.polarization;
            target_particle.color = source_particle.color;
            target_particle.position = source_particle.position;
        }

        let teleportation = Teleportation {
            source_particle: source_id,
            target_particle: target_id,
            success,
            fidelity,
        };

        self.results.teleportations.push(teleportation.clone());
        Some(teleportation)
    }

    fn display_pair(&self, pair: &EntangledPair, index: usize) {
        println!("\n=== Entangled Pair #{} ===", index + 1);
        println!("Entanglement Strength: {:.2}%", pair.entanglement_strength * 100.0);
        
        println!("Particle A (ID: {}):", pair.particle_a.id);
        println!("  Spin: {:?}", pair.particle_a.spin);
        println!("  Polarization: {:?}", pair.particle_a.polarization);
        println!("  Color: {:?}", pair.particle_a.color);
        println!("  Position: {:?}", pair.particle_a.position);
        println!("  Observed: {}", if pair.particle_a.is_observed { "✓" } else { "✗" });
        
        println!("Particle B (ID: {}):", pair.particle_b.id);
        println!("  Spin: {:?}", pair.particle_b.spin);
        println!("  Polarization: {:?}", pair.particle_b.polarization);
        println!("  Color: {:?}", pair.particle_b.color);
        println!("  Position: {:?}", pair.particle_b.position);
        println!("  Observed: {}", if pair.particle_b.is_observed { "✓" } else { "✗" });
    }

    fn run_simulation(&mut self, num_pairs: usize, verbose: bool, export_file: Option<String>) {
        println!("🔬 Initializing Quantum Entanglement Simulator...");
        println!("⏳ Generating {} entangled particle pairs...", num_pairs);

        let start_time = Instant::now();

        // Generate entangled pairs
        for i in 0..num_pairs {
            let pair = self.generate_entangled_pair();
            if verbose {
                self.display_pair(&pair, i);
            }
        }

        let generation_time = start_time.elapsed();
        println!("\n✅ Generated {} pairs in {:?}", num_pairs, generation_time);

        // Simulate observations
        println!("\n👀 Simulating quantum observations...");
        for i in 0..num_pairs {
            // Randomly observe one particle from each pair
            let observe_a = self.rng.gen_bool(0.5);
            if let Some(observation) = self.observe_particle(i, observe_a) {
                if verbose {
                    println!("\n✨ Spooky action detected!");
                    println!("Observed: {}", observation.observed_state);
                    println!("Collapsed: {}", observation.collapsed_state);
                }
            }
        }

        // Simulate quantum teleportations
        println!("\n🚀 Simulating quantum teleportations...");
        for _ in 0..(num_pairs / 2) {
            let source_id = self.rng.gen_range(1..=(num_pairs * 2) as u32);
            let target_id = self.rng.gen_range(1..=(num_pairs * 2) as u32);
            
            if let Some(teleportation) = self.quantum_teleportation(source_id, target_id) {
                if verbose {
                    println!("\n📡 Teleportation attempt:");
                    println!("  Source: Particle {}, Target: Particle {}", 
                             teleportation.source_particle, teleportation.target_particle);
                    println!("  Success: {}, Fidelity: {:.2}%", 
                             if teleportation.success { "✓" } else { "✗" }, 
                             teleportation.fidelity * 100.0);
                }
            }
        }

        let total_time = start_time.elapsed();
        println!("\n⏱️  Simulation completed in {:?}", total_time);

        // Display summary
        println!("\n📊 Simulation Summary:");
        println!("  Pairs Generated: {}", self.results.pairs_generated);
        println!("  Observations: {}", self.results.observations.len());
        println!("  Teleportations: {}", self.results.teleportations.len());
        
        let successful_teleportations = self.results.teleportations.iter()
            .filter(|t| t.success).count();
        println!("  Successful Teleportations: {}", successful_teleportations);

        // Export results if requested
        if let Some(filename) = export_file {
            match serde_json::to_string_pretty(&self.results) {
                Ok(json) => {
                    match fs::write(&filename, json) {
                        Ok(_) => println!("\n💾 Results exported to: {}", filename),
                        Err(e) => println!("❌ Failed to write export file: {}", e),
                    }
                }
                Err(e) => println!("❌ Failed to serialize results: {}", e),
            }
        }
    }
}

fn print_usage() {
    println!("Usage: nightly-quantum-entanglement-simulator [OPTIONS]");
    println!("\nOptions:");
    println!("  --pairs N        Number of entangled pairs to generate (default: 5)");
    println!("  --verbose        Enable verbose output with detailed particle states");
    println!("  --export FILE    Export simulation results to JSON file");
    println!("  --help           Show this help message");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    let mut num_pairs = 5;
    let mut verbose = false;
    let mut export_file = None;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--pairs" => {
                if i + 1 < args.len() {
                    match args[i + 1].parse::<usize>() {
                        Ok(n) => num_pairs = n,
                        Err(_) => {
                            eprintln!("❌ Invalid number for --pairs");
                            std::process::exit(1);
                        }
                    }
                    i += 2;
                } else {
                    eprintln!("❌ --pairs requires a number");
                    std::process::exit(1);
                }
            }
            "--verbose" => {
                verbose = true;
                i += 1;
            }
            "--export" => {
                if i + 1 < args.len() {
                    export_file = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("❌ --export requires a filename");
                    std::process::exit(1);
                }
            }
            "--help" => {
                print_usage();
                return;
            }
            _ => {
                eprintln!("❌ Unknown option: {}", args[i]);
                print_usage();
                std::process::exit(1);
            }
        }
    }

    if num_pairs == 0 {
        eprintln!("❌ Number of pairs must be greater than 0");
        std::process::exit(1);
    }

    let mut simulator = QuantumSimulator::new();
    simulator.run_simulation(num_pairs, verbose, export_file);
}
