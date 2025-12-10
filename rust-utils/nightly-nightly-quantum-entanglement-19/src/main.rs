use std::env;
use std::time::Instant;
use clap::{Arg, Command};

/// Quantum state representation
#[derive(Debug, Clone)]
struct QuantumState {
    amplitude_a: f64,
    amplitude_b: f64,
    phase: f64,
}

impl QuantumState {
    fn new(amplitude_a: f64, amplitude_b: f64, phase: f64) -> Self {
        Self {
            amplitude_a,
            amplitude_b,
            phase,
        }
    }

    /// Calculate entanglement fidelity
    fn entanglement_fidelity(&self) -> f64 {
        let norm_sq = self.amplitude_a.powi(2) + self.amplitude_b.powi(2);
        if norm_sq == 0.0 {
            0.0
        } else {
            (2.0 * self.amplitude_a * self.amplitude_b).abs() / norm_sq
        }
    }

    /// Calculate concurrence (measure of entanglement)
    fn concurrence(&self) -> f64 {
        let c = 2.0 * self.amplitude_a * self.amplitude_b;
        c.abs().min(1.0)
    }

    /// Calculate tangle
    fn tangle(&self) -> f64 {
        self.concurrence().powi(2)
    }
}

/// Bell state types
#[derive(Debug, Clone, PartialEq)]
enum BellState {
    PhiPlus,
    PhiMinus,
    PsiPlus,
    PsiMinus,
}

impl BellState {
    fn from_str(s: &str) -> Option<Self> {
        match s.to_lowercase().as_str() {
            "phi_plus" | "phi+" => Some(BellState::PhiPlus),
            "phi_minus" | "phi-" => Some(BellState::PhiMinus),
            "psi_plus" | "psi+" => Some(BellState::PsiPlus),
            "psi_minus" | "psi-" => Some(BellState::PsiMinus),
            _ => None,
        }
    }

    fn ideal_state(&self) -> QuantumState {
        match self {
            BellState::PhiPlus => QuantumState::new(1.0 / 2.0_f64.sqrt(), 1.0 / 2.0_f64.sqrt(), 0.0),
            BellState::PhiMinus => QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt(), 0.0),
            BellState::PsiPlus => QuantumState::new(0.0, 1.0 / 2.0_f64.sqrt(), std::f64::consts::PI / 2.0),
            BellState::PsiMinus => QuantumState::new(1.0 / 2.0_f64.sqrt(), -1.0 / 2.0_f64.sqrt(), std::f64::consts::PI / 2.0),
        }
    }
}

/// Check if a quantum state is entangled
fn check_entanglement(amplitude_a: f64, amplitude_b: f64) -> Result<(), String> {
    let state = QuantumState::new(amplitude_a, amplitude_b, 0.0);
    
    let fidelity = state.entanglement_fidelity();
    let concurrence = state.concurrence();
    let tangle = state.tangle();
    
    println!("\n=== Quantum Entanglement Analysis ===");
    println!("Amplitude A: {:.6}", state.amplitude_a);
    println!("Amplitude B: {:.6}", state.amplitude_b);
    println!("\n--- Entanglement Metrics ---");
    println!("Entanglement Fidelity: {:.4}", fidelity);
    println!("Concurrence: {:.4}", concurrence);
    println!("Tangle: {:.4}", tangle);
    
    if fidelity > 0.5 {
        println!("\n✅ STATE IS ENTANGLED (Fidelity > 0.5)");
        println!("   This state exhibits quantum entanglement!");
    } else if fidelity > 0.0 {
        println!("\n⚠️  PARTIALLY ENTANGLED (0 < Fidelity ≤ 0.5)");
        println!("   Weak entanglement detected");
    } else {
        println!("\n❌ NOT ENTANGLED (Fidelity = 0)");
        println!("   This is a separable state");
    }
    
    Ok(())
}

/// Verify Bell state
fn verify_bell_state(state_name: &str, threshold: f64) -> Result<(), String> {
    let bell_state = BellState::from_str(state_name)
        .ok_or_else(|| format!("Unknown Bell state: {}. Try: phi_plus, phi_minus, psi_plus, psi_minus", state_name))?;
    
    let ideal = bell_state.ideal_state();
    let fidelity = ideal.entanglement_fidelity();
    
    println!("\n=== Bell State Verification ===");
    println!("Target State: {:?}", bell_state);
    println!("Amplitude A: {:.6}", ideal.amplitude_a);
    println!("Amplitude B: {:.6}", ideal.amplitude_b);
    println!("Phase: {:.4} rad", ideal.phase);
    println!("\n--- Verification Results ---");
    println!("Ideal Fidelity: {:.4}", fidelity);
    println!("Threshold: {:.4}", threshold);
    
    if fidelity >= threshold {
        println!("\n✅ BELL STATE VERIFIED");
        println!("   Meets threshold requirement");
    } else {
        println!("\n❌ BELL STATE NOT VERIFIED");
        println!("   Does not meet threshold requirement");
    }
    
    Ok(())
}

/// Analyze noise tolerance
fn analyze_noise_tolerance(iterations: u32, max_noise: f64) -> Result<(), String> {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    
    let mut entangled_count = 0;
    let mut total_fidelity = 0.0;
    
    println!("\n=== Noise Tolerance Analysis ===");
    println!("Iterations: {}", iterations);
    println!("Max Noise: {:.3}", max_noise);
    
    let start = Instant::now();
    
    for i in 0..iterations {
        // Generate random amplitudes with noise
        let noise_a = rng.gen_range(-max_noise..=max_noise);
        let noise_b = rng.gen_range(-max_noise..=max_noise);
        
        let amplitude_a = 1.0 / 2.0_f64.sqrt() + noise_a;
        let amplitude_b = 1.0 / 2.0_f64.sqrt() + noise_b;
        
        let state = QuantumState::new(amplitude_a, amplitude_b, 0.0);
        let fidelity = state.entanglement_fidelity();
        
        total_fidelity += fidelity;
        if fidelity > 0.5 {
            entangled_count += 1;
        }
        
        // Progress indicator
        if (i + 1) % (iterations / 10) == 0 {
            print!("Progress: {:>3}%\r", (i + 1) * 100 / iterations);
        }
    }
    
    let duration = start.elapsed();
    let avg_fidelity = total_fidelity / iterations as f64;
    let survival_rate = entangled_count as f64 / iterations as f64;
    
    println!("\n\n--- Analysis Results ---");
    println!("Average Fidelity: {:.4}", avg_fidelity);
    println!("Entanglement Survival Rate: {:.1}%", survival_rate * 100.0);
    println!("Total Time: {:.2}ms", duration.as_secs_f64() * 1000.0);
    println!("Time per iteration: {:.2}μs", duration.as_secs_f64() * 1_000_000.0 / iterations as f64);
    
    if survival_rate > 0.8 {
        println!("\n✅ HIGH NOISE TOLERANCE");
        println!("   Entanglement persists under noise");
    } else if survival_rate > 0.5 {
        println!("\n⚠️  MODERATE NOISE TOLERANCE");
        println!("   Partial entanglement preservation");
    } else {
        println!("\n❌ LOW NOISE TOLERANCE");
        println!("   Entanglement easily disrupted");
    }
    
    Ok(())
}

/// Performance benchmark
fn benchmark_performance(samples: u32) -> Result<(), String> {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    
    println!("\n=== Performance Benchmark ===");
    println!("Samples: {}", samples);
    
    let start = Instant::now();
    
    // Generate random quantum states and calculate metrics
    for _ in 0..samples {
        let amplitude_a = rng.gen_range(-1.0..=1.0);
        let amplitude_b = rng.gen_range(-1.0..=1.0);
        
        let state = QuantumState::new(amplitude_a, amplitude_b, 0.0);
        let _fidelity = state.entanglement_fidelity();
        let _concurrence = state.concurrence();
        let _tangle = state.tangle();
    }
    
    let duration = start.elapsed();
    let ns_per_calc = duration.as_secs_f64() * 1_000_000_000.0 / samples as f64;
    
    println!("\n--- Benchmark Results ---");
    println!("Total Time: {:.2}ms", duration.as_secs_f64() * 1000.0);
    println!("Time per calculation: {:.1}ns", ns_per_calc);
    println!("Calculations per second: {:.2}M", samples as f64 / duration.as_secs_f64() / 1_000_000.0);
    
    if ns_per_calc < 100.0 {
        println!("\n✅ EXCELLENT PERFORMANCE");
        println!("   Sub-100ns per entanglement check");
    } else if ns_per_calc < 1000.0 {
        println!("\n✅ GOOD PERFORMANCE");
        println!("   Sub-microsecond calculations");
    } else {
        println!("\n⚠️  MODERATE PERFORMANCE");
        println!("   Calculations in microseconds");
    }
    
    Ok(())
}

fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Verify quantum entanglement states with high performance")
        .subcommand(
            Command::new("check")
                .about("Check if a quantum state is entangled")
                .arg(
                    Arg::new("amplitude-a")
                        .short('a')
                        .long("amplitude-a")
                        .value_name("VALUE")
                        .help("Amplitude of first quantum state")
                        .required(true)
                )
                .arg(
                    Arg::new("amplitude-b")
                        .short('b')
                        .long("amplitude-b")
                        .value_name("VALUE")
                        .help("Amplitude of second quantum state")
                        .required(true)
                )
        )
        .subcommand(
            Command::new("bell")
                .about("Verify Bell state entanglement")
                .arg(
                    Arg::new("state")
                        .short('s')
                        .long("state")
                        .value_name("STATE")
                        .help("Bell state to verify (phi_plus, phi_minus, psi_plus, psi_minus)")
                        .required(true)
                )
                .arg(
                    Arg::new("threshold")
                        .short('t')
                        .long("threshold")
                        .value_name("VALUE")
                        .help("Fidelity threshold for verification")
                        .default_value("0.95")
                )
        )
        .subcommand(
            Command::new("noise")
                .about("Analyze noise tolerance of entanglement")
                .arg(
                    Arg::new("iterations")
                        .short('i')
                        .long("iterations")
                        .value_name("COUNT")
                        .help("Number of noise iterations")
                        .default_value("1000")
                )
                .arg(
                    Arg::new("max-noise")
                        .short('n')
                        .long("max-noise")
                        .value_name("VALUE")
                        .help("Maximum noise amplitude")
                        .default_value("0.1")
                )
        )
        .subcommand(
            Command::new("benchmark")
                .about("Benchmark entanglement calculation performance")
                .arg(
                    Arg::new("samples")
                        .short('s')
                        .long("samples")
                        .value_name("COUNT")
                        .help("Number of samples to test")
                        .default_value("10000")
                )
        )
        .get_matches();

    match matches.subcommand() {
        Some(("check", sub_matches)) => {
            let amplitude_a: f64 = sub_matches.get_one::<String>("amplitude-a")
                .unwrap()
                .parse()
                .expect("Amplitude A must be a number");
            let amplitude_b: f64 = sub_matches.get_one::<String>("amplitude-b")
                .unwrap()
                .parse()
                .expect("Amplitude B must be a number");
            
            if let Err(e) = check_entanglement(amplitude_a, amplitude_b) {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        },
        Some(("bell", sub_matches)) => {
            let state_name = sub_matches.get_one::<String>("state").unwrap();
            let threshold: f64 = sub_matches.get_one::<String>("threshold")
                .unwrap()
                .parse()
                .expect("Threshold must be a number");
            
            if let Err(e) = verify_bell_state(state_name, threshold) {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        },
        Some(("noise", sub_matches)) => {
            let iterations: u32 = sub_matches.get_one::<String>("iterations")
                .unwrap()
                .parse()
                .expect("Iterations must be a positive integer");
            let max_noise: f64 = sub_matches.get_one::<String>("max-noise")
                .unwrap()
                .parse()
                .expect("Max noise must be a number");
            
            if let Err(e) = analyze_noise_tolerance(iterations, max_noise) {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        },
        Some(("benchmark", sub_matches)) => {
            let samples: u32 = sub_matches.get_one::<String>("samples")
                .unwrap()
                .parse()
                .expect("Samples must be a positive integer");
            
            if let Err(e) = benchmark_performance(samples) {
                eprintln!("Error: {}", e);
                std::process::exit(1);
            }
        },
        _ => {
            println!("Use --help for usage information");
        }
    }
}
