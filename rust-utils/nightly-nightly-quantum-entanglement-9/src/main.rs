use std::env;
use std::process;
use rand::Rng;
use structopt::StructOpt;

/// Quantum Entanglement Checker - Simulates quantum entanglement verification
#[derive(StructOpt, Debug)]
struct Args {
    /// Number of quantum particles to simulate
    #[structopt(short, long, default_value = "4")]
    particles: usize,
    
    /// Number of measurement iterations
    #[structopt(short, long, default_value = "1000")]
    measurements: usize,
    
    /// Minimum fidelity threshold for entanglement verification
    #[structopt(short, long, default_value = "0.8")]
    fidelity_threshold: f64,
    
    /// Enable verbose output
    #[structopt(short, long)]
    verbose: bool,
}

/// Represents a quantum state (simplified)
#[derive(Debug, Clone)]
struct QuantumState {
    amplitudes: Vec<Complex>,
}

/// Complex number representation
#[derive(Debug, Clone, Copy)]
struct Complex {
    real: f64,
    imag: f64,
}

impl Complex {
    fn new(real: f64, imag: f64) -> Self {
        Complex { real, imag }
    }
    
    fn magnitude_squared(&self) -> f64 {
        self.real * self.real + self.imag * self.imag
    }
    
    fn conjugate(&self) -> Self {
        Complex::new(self.real, -self.imag)
    }
    
    fn multiply(&self, other: &Complex) -> Self {
        Complex::new(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )
    }
}

impl QuantumState {
    fn new_random(n: usize) -> Self {
        let mut rng = rand::thread_rng();
        let mut amplitudes = Vec::with_capacity(1 << n);
        
        // Generate random amplitudes
        for _ in 0..(1 << n) {
            let real: f64 = rng.gen_range(-1.0..1.0);
            let imag: f64 = rng.gen_range(-1.0..1.0);
            amplitudes.push(Complex::new(real, imag));
        }
        
        // Normalize
        Self::normalize(&mut amplitudes);
        
        QuantumState { amplitudes }
    }
    
    fn normalize(amplitudes: &mut Vec<Complex>) {
        let norm_squared: f64 = amplitudes.iter().map(|a| a.magnitude_squared()).sum();
        let norm = norm_squared.sqrt();
        
        if norm > 0.0 {
            for amp in amplitudes.iter_mut() {
                amp.real /= norm;
                amp.imag /= norm;
            }
        }
    }
    
    fn measure_bell_state(&self, measurements: usize) -> Vec<f64> {
        let mut rng = rand::thread_rng();
        let mut results = Vec::with_capacity(measurements);
        
        for _ in 0..measurements {
            // Simulate Bell state measurement
            let index = rng.gen_range(0..self.amplitudes.len());
            let probability = self.amplitudes[index].magnitude_squared();
            results.push(probability);
        }
        
        results
    }
    
    fn calculate_fidelity(&self, other: &QuantumState) -> f64 {
        if self.amplitudes.len() != other.amplitudes.len() {
            return 0.0;
        }
        
        let mut fidelity = 0.0;
        for (a, b) in self.amplitudes.iter().zip(other.amplitudes.iter()) {
            let overlap = a.multiply(&b.conjugate());
            fidelity += overlap.magnitude_squared();
        }
        
        fidelity.sqrt()
    }
    
    fn print_state(&self, verbose: bool) {
        if verbose {
            println!("Generated quantum state amplitudes:");
            for (i, amp) in self.amplitudes.iter().enumerate() {
                println!("  |{}⟩: {:.4} + {:.4}i", i, amp.real, amp.imag);
            }
        } else {
            println!("Generated quantum state with {} amplitudes", self.amplitudes.len());
        }
    }
}

fn analyze_measurements(results: &[f64]) -> (f64, f64) {
    let mean = results.iter().sum::<f64>() / results.len() as f64;
    let variance = results.iter().map(|&x| (x - mean).powi(2)).sum::<f64>() / results.len() as f64;
    let std_dev = variance.sqrt();
    
    (mean, std_dev)
}

fn main() {
    let args = Args::from_args();
    
    if args.particles == 0 {
        eprintln!("Error: Number of particles must be greater than 0");
        process::exit(1);
    }
    
    if args.measurements == 0 {
        eprintln!("Error: Number of measurements must be greater than 0");
        process::exit(1);
    }
    
    println!("🧪 Quantum Entanglement Checker v1.0");
    println!("=====================================");
    println!("Particles: {}", args.particles);
    println!("Measurements: {}", args.measurements);
    println!("Fidelity threshold: {:.2}", args.fidelity_threshold);
    println!();
    
    // Generate two entangled quantum states
    let state1 = QuantumState::new_random(args.particles);
    let state2 = QuantumState::new_random(args.particles);
    
    // Print states if verbose
    state1.print_state(args.verbose);
    state2.print_state(args.verbose);
    
    println!();
    
    // Perform Bell state measurements
    println!("🔬 Performing Bell state measurements...");
    let measurements1 = state1.measure_bell_state(args.measurements);
    let measurements2 = state2.measure_bell_state(args.measurements);
    
    // Analyze results
    let (mean1, std_dev1) = analyze_measurements(&measurements1);
    let (mean2, std_dev2) = analyze_measurements(&measurements2);
    
    println!();
    println!("📊 Measurement Statistics:");
    println!("  State 1 - Mean: {:.4}, Std Dev: {:.4}", mean1, std_dev1);
    println!("  State 2 - Mean: {:.4}, Std Dev: {:.4}", mean2, std_dev2);
    
    // Calculate entanglement fidelity
    let fidelity = state1.calculate_fidelity(&state2);
    println!();
    println!("🔗 Entanglement Fidelity: {:.4}", fidelity);
    
    // Verify entanglement
    let is_entangled = fidelity >= args.fidelity_threshold;
    println!();
    println!("🎯 Verification Result:");
    if is_entangled {
        println!("  ✅ States are entangled! (Fidelity >= {:.2})", args.fidelity_threshold);
    } else {
        println!("  ❌ States are not sufficiently entangled. (Fidelity < {:.2})", args.fidelity_threshold);
    }
    
    // Quantum computing facts
    println!();
    println!("🧠 Quantum Computing Facts:");
    println!("  • Bell states are maximally entangled quantum states of two qubits");
    println!("  • Quantum entanglement enables phenomena like quantum teleportation");
    println!("  • Fidelity measures how close two quantum states are to each other");
    println!("  • This simulation uses simplified quantum mechanics principles");
}
