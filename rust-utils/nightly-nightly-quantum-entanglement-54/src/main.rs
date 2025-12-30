use clap::{Arg, Command};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::io;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Serialize, Deserialize)]
enum QuantumState {
    Up,
    Down,
    Left,
    Right,
    Diagonal,
    AntiDiagonal,
}

impl QuantumState {
    fn to_symbol(&self) -> &'static str {
        match self {
            QuantumState::Up => "|↑⟩",
            QuantumState::Down => "|↓⟩",
            QuantumState::Left => "|←⟩",
            QuantumState::Right => "|→⟩",
            QuantumState::Diagonal => "|↗⟩",
            QuantumState::AntiDiagonal => "|↖⟩",
        }
    }

    fn to_ascii_art(&self) -> &'static str {
        match self {
            QuantumState::Up => "  /\  \n  ||  ",
            QuantumState::Down => "  ||  \n  \\\/  ",
            QuantumState::Left => "  <<  ",
            QuantumState::Right => "  >>  ",
            QuantumState::Diagonal => "  /   \n /    ",
            QuantumState::AntiDiagonal => "    \  \n   /   ",
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct QuantumParticle {
    id: u32,
    state: QuantumState,
    is_entangled: bool,
}

#[derive(Debug, Serialize, Deserialize)]
struct QuantumSystem {
    particles: Vec<QuantumParticle>,
    entanglement_pairs: Vec<(u32, u32)>,
    timestamp: String,
}

impl QuantumSystem {
    fn new(particle_count: u32) -> Self {
        let particles: Vec<QuantumParticle> = (0..particle_count)
            .map(|i| QuantumParticle {
                id: i,
                state: QuantumState::Up,
                is_entangled: false,
            })
            .collect();

        QuantumSystem {
            particles,
            entanglement_pairs: Vec::new(),
            timestamp: chrono::Utc::now().to_rfc3339(),
        }
    }

    fn entangle_particles(&mut self, id1: u32, id2: u32) {
        if let (Some(p1), Some(p2)) = (
            self.particles.iter_mut().find(|p| p.id == id1),
            self.particles.iter_mut().find(|p| p.id == id2),
        ) {
            p1.is_entangled = true;
            p2.is_entangled = true;
            self.entanglement_pairs.push((id1, id2));
        }
    }

    fn simulate_measurement(&mut self) -> Vec<(u32, QuantumState)> {
        let mut results = Vec::new();
        let mut rng = rand::thread_rng();

        for particle in &mut self.particles {
            // If entangled, we need to handle the entanglement rules
            if particle.is_entangled {
                // For simplicity, we'll use anti-correlation for entangled particles
                let new_state = match particle.state {
                    QuantumState::Up => QuantumState::Down,
                    QuantumState::Down => QuantumState::Up,
                    QuantumState::Left => QuantumState::Right,
                    QuantumState::Right => QuantumState::Left,
                    QuantumState::Diagonal => QuantumState::AntiDiagonal,
                    QuantumState::AntiDiagonal => QuantumState::Diagonal,
                };
                particle.state = new_state;
            } else {
                // Random measurement for non-entangled particles
                let states = [
                    QuantumState::Up,
                    QuantumState::Down,
                    QuantumState::Left,
                    QuantumState::Right,
                    QuantumState::Diagonal,
                    QuantumState::AntiDiagonal,
                ];
                particle.state = states[rng.gen_range(0..states.len())].clone();
            }
            results.push((particle.id, particle.state.clone()));
        }

        results
    }

    fn display_ascii_art(&self) {
        println!("=== Quantum State Visualization ===");
        for particle in &self.particles {
            println!("Particle {}: {}", particle.id, particle.state.to_symbol());
            println!("{}");
            println!("Entangled: {}", if particle.is_entangled { "✓" } else { "✗" });
            println!("---");
        }
    }
}

fn main() {
    let matches = Command::new("Nightly Quantum Entanglement Simulator")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI Community")
        .about("A whimsical CLI tool that simulates quantum entanglement states")
        .subcommand(
            Command::new("simulate")
                .about("Run a quantum entanglement simulation")
                .arg(
                    Arg::new("particles")
                        .short('p')
                        .long("particles")
                        .value_name("N")
                        .help("Number of entangled particles")
                        .default_value("2")
                )
                .arg(
                    Arg::new("iterations")
                        .short('i')
                        .long("iterations")
                        .value_name("N")
                        .help("Number of simulation iterations")
                        .default_value("1")
                )
        )
        .subcommand(
            Command::new("educate")
                .about("Display educational content about quantum entanglement")
                .arg(
                    Arg::new("topic")
                        .short('t')
                        .long("topic")
                        .value_name("TOPIC")
                        .help("Specific topic to explain")
                        .possible_values(["superposition", "measurement", "nonlocality"])
                )
        )
        .subcommand(
            Command::new("measure")
                .about("Generate random quantum measurements")
                .arg(
                    Arg::new("basis")
                        .short('b')
                        .long("basis")
                        .value_name("BASIS")
                        .help("Measurement basis")
                        .possible_values(["z", "x", "y"])
                        .default_value("z")
                )
                .arg(
                    Arg::new("count")
                        .short('c')
                        .long("count")
                        .value_name("N")
                        .help("Number of measurements to generate")
                        .default_value("10")
                )
        )
        .subcommand(
            Command::new("save")
                .about("Save the current quantum state to a file")
                .arg(
                    Arg::new("file")
                        .short('f')
                        .long("file")
                        .value_name("FILE")
                        .help("Output file path")
                        .default_value("quantum_state.json")
                )
        )
        .subcommand(
            Command::new("load")
                .about("Load a quantum state from a file")
                .arg(
                    Arg::new("file")
                        .short('f')
                        .long("file")
                        .value_name("FILE")
                        .help("Input file path")
                        .default_value("quantum_state.json")
                )
        )
        .get_matches();

    match matches.subcommand() {
        Some(("simulate", sub_matches)) => {
            let particles: u32 = sub_matches
                .get_one::<String>("particles")
                .unwrap()
                .parse()
                .expect("Invalid particle count");
            let iterations: u32 = sub_matches
                .get_one::<String>("iterations")
                .unwrap()
                .parse()
                .expect("Invalid iteration count");

            simulate_quantum_entanglement(particles, iterations);
        }
        Some(("educate", sub_matches)) => {
            if let Some(topic) = sub_matches.get_one::<String>("topic") {
                display_education_content(Some(topic));
            } else {
                display_education_content(None);
            }
        }
        Some(("measure", sub_matches)) => {
            let basis = sub_matches.get_one::<String>("basis").unwrap();
            let count: u32 = sub_matches
                .get_one::<String>("count")
                .unwrap()
                .parse()
                .expect("Invalid count");

            generate_measurements(basis, count);
        }
        Some(("save", sub_matches)) => {
            let file_path = sub_matches.get_one::<String>("file").unwrap();
            save_quantum_state(file_path);
        }
        Some(("load", sub_matches)) => {
            let file_path = sub_matches.get_one::<String>("file").unwrap();
            load_quantum_state(file_path);
        }
        _ => {
            println!("Use --help for usage information");
        }
    }
}

fn simulate_quantum_entanglement(particle_count: u32, iterations: u32) {
    println!("=== Quantum Entanglement Simulation ===");
    println!("Particles: {}, Iterations: {}", particle_count, iterations);
    println!();

    let start_time = Instant::now();

    for i in 0..iterations {
        println!("Iteration {}:", i + 1);

        let mut system = QuantumSystem::new(particle_count);

        // Create entanglement pairs
        for j in (0..particle_count).step_by(2) {
            if j + 1 < particle_count {
                system.entangle_particles(j, j + 1);
            }
        }

        // Display initial state
        system.display_ascii_art();

        // Simulate measurement
        let measurements = system.simulate_measurement();

        println!("\nMeasurement Results:");
        for (id, state) in measurements {
            println!("Particle {}: {}", id, state.to_symbol());
        }

        println!("---\n");
    }

    let duration = start_time.elapsed();
    println!("Simulation completed in {:?}", duration);
}

fn display_education_content(topic: Option<&String>) {
    println!("=== Quantum Entanglement Explained ===\n");

    match topic {
        Some(t) if t == "superposition" => {
            println!("What is Quantum Superposition?\n");
            println!("Quantum superposition is a fundamental principle of quantum mechanics.");
            println!("It states that a quantum system can exist in multiple states simultaneously");
            println!("until it is measured. Only upon measurement does the system 'collapse'");
            println!("into one of the possible states.\n");

            println!("Example:");
            println!("A quantum particle can be in a superposition of |↑⟩ and |↓⟩ states,");
            println!("meaning it's both spin up AND spin down at the same time!\n");
        }
        Some(t) if t == "measurement" => {
            println!("What is Quantum Measurement?\n");
            println!("In quantum mechanics, measurement is the process that forces a quantum");
            println!("system to choose one of its possible states. Before measurement, the");
            println!("system exists in a superposition of states. After measurement, it exists");
            println!("in a single, definite state.\n");

            println!("The Observer Effect:");
            println!("The act of observation fundamentally changes the quantum system.");
            println!("This is different from classical physics where observation doesn't");
            println!("affect the observed object.\n");
        }
        Some(t) if t == "nonlocality" => {
            println!("What is Quantum Non-locality?\n");
            println!("Quantum non-locality refers to the phenomenon where entangled particles");
            println!("affect each other instantaneously, regardless of the distance between them.");
            println!("This seems to violate the principle that nothing can travel faster than");
            println!("the speed of light, but it's a well-established feature of quantum mechanics.\n");

            println!("Spooky Action at a Distance:");
            println!("Einstein famously called this 'spooky action at a distance' because it");
            println!("challenged our classical understanding of how the universe works.\n");
        }
        _ => {
            println!("What is Quantum Entanglement?\n");
            println!("Quantum entanglement is a physical phenomenon that occurs when pairs or");
            println!("groups of particles are generated, interact, or share spatial proximity");
            println!("in ways such that the quantum state of each particle cannot be described");
            println!("independently of the state of the others.\n");

            println!("Key Concepts:");
            println!("• Superposition: Particles can exist in multiple states simultaneously");
            println!("• Measurement: Observing a particle forces it into a definite state");
            println!("• Non-locality: Entangled particles affect each other instantaneously\n");

            println!("Simulation:");
            println!("Particle A: |↑⟩ + |↓⟩ (superposition)");
            println!("Particle B: |↑⟩ + |↓⟩ (superposition)");
            println!("Entanglement: ✓ Active\n");
            println!("When we measure Particle A and find it in state |↑⟩,");
            println!("Particle B instantly becomes |↓⟩!\n");
        }
    }
}

fn generate_measurements(basis: &str, count: u32) {
    println!("=== Random Quantum Measurements ===");
    println!("Basis: {}, Count: {}", basis, count);
    println!();

    let states = [
        "|↑⟩", "|↓⟩", "|←⟩", "|→⟩", "|↗⟩", "|↖⟩",
    ];

    let mut rng = rand::thread_rng();

    for i in 1..=count {
        let state = states[rng.gen_range(0..states.len())];
        println!("Measurement {}: {}", i, state);
    }

    println!();
    println!("Note: These are simulated measurements for educational purposes.");
    println!("Real quantum measurements follow specific probability distributions.");
}

fn save_quantum_state(file_path: &str) {
    let system = QuantumSystem::new(4);

    // Create some entanglement
    system.entangle_particles(0, 1);
    system.entangle_particles(2, 3);

    match serde_json::to_string_pretty(&system) {
        Ok(json) => {
            match fs::write(file_path, json) {
                Ok(_) => println!("Quantum state saved to {}", file_path),
                Err(e) => println!("Error saving file: {}", e),
            }
        }
        Err(e) => println!("Error serializing quantum state: {}", e),
    }
}

fn load_quantum_state(file_path: &str) {
    match fs::read_to_string(file_path) {
        Ok(content) => {
            match serde_json::from_str::<QuantumSystem>(&content) {
                Ok(system) => {
                    println!("Loaded quantum state from {}", file_path);
                    system.display_ascii_art();
                }
                Err(e) => println!("Error parsing quantum state: {}", e),
            }
        }
        Err(e) => println!("Error reading file: {}", e),
    }
}
