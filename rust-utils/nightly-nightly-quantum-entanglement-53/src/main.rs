use std::time::{Duration, Instant};
use std::thread;
use std::sync::{Arc, Mutex};
use clap::{Arg, App};
use rand::Rng;

#[derive(Debug, Clone, PartialEq)]
enum QuantumState {
    Up,
    Down,
    Superposition,
}

impl QuantumState {
    fn to_symbol(&self) -> &'static str {
        match self {
            QuantumState::Up => "↑",
            QuantumState::Down => "↓",
            QuantumState::Superposition => "?",
        }
    }
}

#[derive(Debug, Clone)]
struct EntangledPair {
    id: usize,
    particle_a: Arc<Mutex<QuantumState>>,
    particle_b: Arc<Mutex<QuantumState>>,
    is_measured: Arc<Mutex<bool>>,
}

impl EntangledPair {
    fn new(id: usize) -> Self {
        let initial_state = if rand::random() { QuantumState::Up } else { QuantumState::Down };
        
        EntangledPair {
            id,
            particle_a: Arc::new(Mutex::new(QuantumState::Superposition)),
            particle_b: Arc::new(Mutex::new(QuantumState::Superposition)),
            is_measured: Arc::new(Mutex::new(false)),
        }
    }

    fn measure(&self, entanglement_strength: f64) -> (QuantumState, QuantumState) {
        let mut rng = rand::thread_rng();
        let mut measured_a = false;
        let mut measured_b = false;
        
        // Determine which particle to measure first (random)
        let measure_a_first = rng.gen_bool(0.5);
        
        let result_a;
        let result_b;
        
        if measure_a_first {
            // Measure particle A
            let mut a_guard = self.particle_a.lock().unwrap();
            if *a_guard == QuantumState::Superposition {
                *a_guard = if rng.gen_bool(0.5) { QuantumState::Up } else { QuantumState::Down };
                measured_a = true;
            }
            result_a = a_guard.clone();
            drop(a_guard);
            
            // Entanglement effect on particle B
            let mut b_guard = self.particle_b.lock().unwrap();
            if *b_guard == QuantumState::Superposition {
                // With entanglement strength probability, correlate with A
                if rng.gen_bool(entanglement_strength) {
                    *b_guard = if result_a == QuantumState::Up { QuantumState::Down } else { QuantumState::Up };
                    measured_b = true;
                } else {
                    // Break entanglement - random state
                    *b_guard = if rng.gen_bool(0.5) { QuantumState::Up } else { QuantumState::Down };
                    measured_b = true;
                }
            }
            result_b = b_guard.clone();
        } else {
            // Measure particle B first
            let mut b_guard = self.particle_b.lock().unwrap();
            if *b_guard == QuantumState::Superposition {
                *b_guard = if rng.gen_bool(0.5) { QuantumState::Up } else { QuantumState::Down };
                measured_b = true;
            }
            result_b = b_guard.clone();
            drop(b_guard);
            
            // Entanglement effect on particle A
            let mut a_guard = self.particle_a.lock().unwrap();
            if *a_guard == QuantumState::Superposition {
                // With entanglement strength probability, correlate with B
                if rng.gen_bool(entanglement_strength) {
                    *a_guard = if result_b == QuantumState::Up { QuantumState::Down } else { QuantumState::Up };
                    measured_a = true;
                } else {
                    // Break entanglement - random state
                    *a_guard = if rng.gen_bool(0.5) { QuantumState::Up } else { QuantumState::Down };
                    measured_a = true;
                }
            }
            result_a = a_guard.clone();
        }
        
        if measured_a || measured_b {
            *self.is_measured.lock().unwrap() = true;
        }
        
        (result_a, result_b)
    }

    fn display(&self) -> String {
        let a_state = *self.particle_a.lock().unwrap();
        let b_state = *self.particle_b.lock().unwrap();
        let is_measured = *self.is_measured.lock().unwrap();
        
        let status = if is_measured { "(Measured)" } else { "(Entangled)" };
        
        format!("Particle Pair {}: [{}] ⟷ [{}]  {}",
                self.id, a_state.to_symbol(), b_state.to_symbol(), status)
    }
}

struct QuantumSimulator {
    pairs: Vec<EntangledPair>,
    entanglement_strength: f64,
    measurement_probability: f64,
    duration: u64,
}

impl QuantumSimulator {
    fn new(pairs_count: usize, entanglement_strength: f64, measurement_probability: f64, duration: u64) -> Self {
        let pairs: Vec<EntangledPair> = (1..=pairs_count)
            .map(|id| EntangledPair::new(id))
            .collect();
            
        QuantumSimulator {
            pairs,
            entanglement_strength,
            measurement_probability,
            duration,
        }
    }

    fn run(&self) {
        println!("Quantum Entanglement Simulation Starting...");
        println!("Entanglement Strength: {:.2} | Measurement Probability: {:.2} | Duration: {}s\n",
                 self.entanglement_strength, self.measurement_probability, self.duration);
        
        let start_time = Instant::now();
        let mut rng = rand::thread_rng();
        
        while start_time.elapsed() < Duration::from_secs(self.duration) {
            // Display current state
            for pair in &self.pairs {
                println!("{}", pair.display());
            }
            println!("");
            
            // Random measurement event
            if rng.gen_bool(self.measurement_probability) {
                // Select random pair that hasn't been measured yet
                let unmeasured_pairs: Vec<_> = self.pairs.iter()
                    .filter(|pair| !*pair.is_measured.lock().unwrap())
                    .collect();
                    
                if !unmeasured_pairs.is_empty() {
                    let random_index = rng.gen_range(0..unmeasured_pairs.len());
                    let selected_pair = unmeasured_pairs[random_index];
                    
                    let (state_a, state_b) = selected_pair.measure(self.entanglement_strength);
                    
                    println!("Measurement Event! Particle {}A collapsed to: {}",
                             selected_pair.id, state_a.to_symbol());
                    
                    if state_a != state_b {
                        println!("Spooky action! Particle {}B instantly became: {}",
                                 selected_pair.id, state_b.to_symbol());
                    } else {
                        println!("Entanglement broken! Particle {}B became: {}",
                                 selected_pair.id, state_b.to_symbol());
                    }
                    println!("");
                }
            }
            
            // Clear screen for next iteration (simple approach)
            print!("\x1B[2J\x1B[1;1H"); // ANSI clear screen
            thread::sleep(Duration::from_millis(500));
        }
        
        println!("\nSimulation Complete!");
        println!("Final State:");
        for pair in &self.pairs {
            println!("{}", pair.display());
        }
    }
}

fn main() {
    let matches = App::new("Quantum Entanglement Simulator")
        .version("1.0")
        .author("ApocalypsAI")
        .about("A whimsical quantum entanglement simulator with ASCII visualization")
        .arg(Arg::new("entanglement-strength")
            .short('e')
            .long("entanglement-strength")
            .value_name("STRENGTH")
            .help("Strength of entanglement (0.0 to 1.0)")
            .takes_value(true))
        .arg(Arg::new("measurement-probability")
            .short('m')
            .long("measurement-probability")
            .value_name("PROBABILITY")
            .help("Probability of measuring a particle (0.0 to 1.0)")
            .takes_value(true))
        .arg(Arg::new("duration")
            .short('d')
            .long("duration")
            .value_name("SECONDS")
            .help("Simulation duration in seconds")
            .takes_value(true))
        .arg(Arg::new("particles")
            .short('p')
            .long("particles")
            .value_name("COUNT")
            .help("Number of entangled pairs")
            .takes_value(true))
        .get_matches();

    let entanglement_strength: f64 = matches.value_of("entanglement-strength")
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.7)
        .clamp(0.0, 1.0);
        
    let measurement_probability: f64 = matches.value_of("measurement-probability")
        .and_then(|s| s.parse().ok())
        .unwrap_or(0.5)
        .clamp(0.0, 1.0);
        
    let duration: u64 = matches.value_of("duration")
        .and_then(|s| s.parse().ok())
        .unwrap_or(10);
        
    let particles: usize = matches.value_of("particles")
        .and_then(|s| s.parse().ok())
        .unwrap_or(5)
        .max(1);

    let simulator = QuantumSimulator::new(
        particles,
        entanglement_strength,
        measurement_probability,
        duration,
    );
    
    simulator.run();
}
