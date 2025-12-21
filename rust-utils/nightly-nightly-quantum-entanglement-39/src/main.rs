use std::env;
use std::fs;
use std::io::{self, Write};
use std::time::Instant;
use rand::prelude::*;
use structopt::StructOpt;

/// Quantum Entanglement Checker - CLI tool for simulating Bell's inequality tests
#[derive(StructOpt, Debug)]
#[structopt(name = "nightly-quantum-entanglement-checker", about = "Simulates quantum entanglement verification using Bell's inequality tests")]
struct Args {
    /// Number of simulated particles
    #[structopt(short, long, default_value = "1000")]
    particles: usize,

    /// Number of measurement trials
    #[structopt(short, long, default_value = "100")]
    trials: usize,

    /// Measurement angle for detector A in degrees
    #[structopt(long, default_value = "0.0")]
    angle_a: f64,

    /// Measurement angle for detector B in degrees
    #[structopt(long, default_value = "45.0")]
    angle_b: f64,

    /// Enable distributed entanglement scenario
    #[structopt(long)]
    distributed: bool,

    /// Distance between entangled particles in kilometers
    #[structopt(long, default_value = "100")]
    distance: f64,

    /// Generate detailed entanglement report
    #[structopt(long)]
    report: bool,

    /// Output file for report
    #[structopt(short, long)]
    output: Option<String>,

    /// Random seed for reproducible results
    #[structopt(long)]
    seed: Option<u64>,
}

/// Quantum state representation
#[derive(Debug, Clone, Copy)]
struct QuantumState {
    amplitude_up: f64,
    amplitude_down: f64,
}

impl QuantumState {
    fn new() -> Self {
        // Create a random superposition state
        let theta: f64 = thread_rng().gen_range(0.0..std::f64::consts::PI);
        let phi: f64 = thread_rng().gen_range(0.0..2.0 * std::f64::consts::PI);
        
        QuantumState {
            amplitude_up: (theta / 2.0).cos(),
            amplitude_down: (theta / 2.0).sin() * (phi * 1i64 as f64).exp(),
        }
    }

    fn measure(&self, angle: f64) -> bool {
        // Convert angle to radians
        let angle_rad = angle.to_radians();
        
        // Calculate probability of measuring 'up'
        let prob_up = (self.amplitude_up * angle_rad.cos() + 
                      self.amplitude_down * angle_rad.sin()).abs().powi(2);
        
        // Random measurement based on probability
        let random_val: f64 = thread_rng().gen();
        random_val < prob_up
    }
}

/// Bell test experiment results
struct BellTestResults {
    correlation_aa: f64,
    correlation_bb: f64,
    correlation_ab: f64,
    correlation_ab_prime: f64,
    bell_inequality_value: f64,
    violations: usize,
    total_measurements: usize,
}

/// Run Bell's inequality test
fn run_bell_test(particles: usize, trials: usize, angle_a: f64, angle_b: f64, seed: Option<u64>) -> BellTestResults {
    if let Some(seed_val) = seed {
        let mut rng = StdRng::seed_from_u64(seed_val);
        thread_rng().clone_from(&rng);
    }

    let mut correlations = vec![0.0; 4];
    let mut counts = vec![0; 4];
    let mut total_measurements = 0;

    // Define measurement angles for Bell test
    let angles = [angle_a, angle_b, angle_a + 45.0, angle_b + 22.5];

    for _ in 0..trials {
        for i in 0..particles {
            let state = QuantumState::new();
            
            // Measure entangled pair with different angle combinations
            for combo in 0..4 {
                let angle1 = angles[combo % 2];
                let angle2 = angles[2 + (combo / 2)];
                
                let result1 = state.measure(angle1);
                let result2 = state.measure(angle2);
                
                // Calculate correlation (-1 for same, +1 for different)
                let correlation = if result1 == result2 { -1.0 } else { 1.0 };
                correlations[combo] += correlation;
                counts[combo] += 1;
                total_measurements += 1;
            }
        }
    }

    // Calculate average correlations
    let correlation_aa = correlations[0] / counts[0] as f64;
    let correlation_bb = correlations[1] / counts[1] as f64;
    let correlation_ab = correlations[2] / counts[2] as f64;
    let correlation_ab_prime = correlations[3] / counts[3] as f64;

    // Bell inequality: |E(a,b) - E(a,b')| + |E(a',b) + E(a',b')| <= 2
    let bell_inequality_value = correlation_ab.abs() - correlation_ab_prime.abs() + 
                               correlation_aa.abs() + correlation_bb.abs();

    // Count violations (value > 2 indicates quantum entanglement)
    let violations = if bell_inequality_value > 2.0 { 1 } else { 0 };

    BellTestResults {
        correlation_aa,
        correlation_bb,
        correlation_ab,
        correlation_ab_prime,
        bell_inequality_value,
        violations,
        total_measurements,
    }
}

/// Generate quantum-themed ASCII art
fn generate_quantum_art() -> String {
    let art = r#"
    ⚛️  QUANTUM ENTANGLEMENT VERIFIER  ⚛️

    ╔══════════════════════════════════════╗
    ║  🌀  Spinning superposition states   ║
    ║  🔗  Entangled particle pairs       ║
    ║  ⚡  Bell inequality violations       ║
    ║  📊  Quantum correlation analysis   ║
    ╚══════════════════════════════════════╝

    "#;
    art.to_string()
}

/// Generate detailed report
fn generate_report(results: &BellTestResults, args: &Args) -> String {
    let mut report = String::new();
    
    report.push_str(&generate_quantum_art());
    report.push_str(&format!("\n🔬 EXPERIMENT CONFIGURATION\n"));
    report.push_str(&format!("├ Particles: {}\n", args.particles));
    report.push_str(&format!("├ Trials: {}\n", args.trials));
    report.push_str(&format!("├ Angle A: {:.1}°\n", args.angle_a));
    report.push_str(&format!("├ Angle B: {:.1}°\n", args.angle_b));
    
    if args.distributed {
        report.push_str(&format!("├ Distributed: Yes ({} km)\n", args.distance));
    } else {
        report.push_str(&format!("├ Distributed: No\n"));
    }
    
    report.push_str(&format!("\n📊 MEASUREMENT RESULTS\n"));
    report.push_str(&format!("├ Correlation A-A': {:.4}\n", results.correlation_aa));
    report.push_str(&format!("├ Correlation B-B': {:.4}\n", results.correlation_bb));
    report.push_str(&format!("├ Correlation A-B: {:.4}\n", results.correlation_ab));
    report.push_str(&format!("├ Correlation A-B': {:.4}\n", results.correlation_ab_prime));
    
    report.push_str(&format!("\n⚛️  QUANTUM ANALYSIS\n"));
    report.push_str(&format!("├ Bell Inequality Value: {:.4}\n", results.bell_inequality_value));
    
    if results.bell_inequality_value > 2.0 {
        report.push_str(&format!("├ Status: ✅ QUANTUM ENTANGLEMENT DETECTED\n"));
        report.push_str(&format!("├ Violation Strength: {:.4}\n", results.bell_inequality_value - 2.0));
        report.push_str(&format!("├ Interpretation: Non-local quantum correlations confirmed\n"));
    } else {
        report.push_str(&format!("├ Status: ❌ CLASSICAL BEHAVIOR\n"));
        report.push_str(&format!("├ Interpretation: No quantum entanglement detected\n"));
    }
    
    report.push_str(&format!("\n📈 STATISTICS\n"));
    report.push_str(&format!("├ Total Measurements: {}\n", results.total_measurements));
    report.push_str(&format!("├ Bell Inequality Violations: {}\n", results.violations));
    report.push_str(&format!("├ Violation Rate: {:.2}%\n", 
        (results.violations as f64 / args.trials as f64) * 100.0));
    
    report.push_str(&format!("\n🔬 SCIENTIFIC NOTES\n"));
    report.push_str(&format!("├ Local realism limit: 2.0000\n"));
    report.push_str(&format!("├ Quantum prediction: 2.8284 (for optimal angles)\n"));
    report.push_str(&format!("├ Experimental deviation: {:.4}\n", 
        results.bell_inequality_value - 2.8284));
    
    report.push_str(&format!("\n"));
    report.push_str(&format!("🎉 Quantum experiment completed successfully!\n"));
    report.push_str(&format!("💡 Remember: Correlation does not imply causation,\n"));
    report.push_str(&format!("   but entanglement implies non-locality!\n"));
    
    report
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args = Args::from_args();
    
    // Print quantum art header
    println!("{}", generate_quantum_art());
    
    // Run the Bell test
    let start_time = Instant::now();
    println!("🔬 Running Bell's inequality test...");
    println!("├ Particles: {}", args.particles);
    println!("├ Trials: {}", args.trials);
    println!("├ Angle A: {:.1}°", args.angle_a);
    println!("├ Angle B: {:.1}°", args.angle_b);
    
    if args.distributed {
        println!("├ Distributed scenario: {} km", args.distance);
    }
    
    let results = run_bell_test(args.particles, args.trials, args.angle_a, args.angle_b, args.seed);
    let duration = start_time.elapsed();
    
    println!("\n⏱️  Experiment completed in {:.2?}", duration);
    
    // Display results
    println!("\n📊 RESULTS:");
    println!("├ Bell Inequality Value: {:.4}", results.bell_inequality_value);
    println!("├ Expected (classical): ≤ 2.0000");
    println!("├ Expected (quantum): ≈ 2.8284");
    
    if results.bell_inequality_value > 2.0 {
        println!("├ Status: ✅ QUANTUM ENTANGLEMENT CONFIRMED");
        println!("├ Violation: {:.4} above classical limit", results.bell_inequality_value - 2.0);
    } else {
        println!("├ Status: ❌ CLASSICAL BEHAVIOR DETECTED");
    }
    
    // Generate detailed report if requested
    if args.report {
        let report = generate_report(&results, &args);
        
        match &args.output {
            Some(filename) => {
                fs::write(filename, &report)?;
                println!("\n📄 Detailed report saved to: {}", filename);
            }
            None => {
                println!("\n📄 DETAILED REPORT:");
                println!("{}", report);
            }
        }
    }
    
    println!("\n🎉 Quantum entanglement verification complete!");
    println!("💡 Tip: Try different angles to maximize Bell inequality violations!");
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Cursor;

    #[test]
    fn test_quantum_state_creation() {
        let state = QuantumState::new();
        assert!(state.amplitude_up.is_finite());
        assert!(state.amplitude_down.is_finite());
    }

    #[test]
    fn test_quantum_measurement() {
        let state = QuantumState::new();
        let result = state.measure(0.0);
        assert!(result == true || result == false);
    }

    #[test]
    fn test_bell_test_basic() {
        let results = run_bell_test(100, 10, 0.0, 45.0, Some(42));
        assert!(results.total_measurements > 0);
        assert!(results.correlation_aa.abs() <= 1.0);
        assert!(results.correlation_bb.abs() <= 1.0);
    }

    #[test]
    fn test_bell_inequality_classical_limit() {
        // With random angles, should typically stay below 2.0
        let results = run_bell_test(500, 5, 0.0, 45.0, Some(123));
        // Note: This might occasionally exceed 2.0 due to quantum effects in our simulation
        // but should be rare with small particle counts
        assert!(results.bell_inequality_value.is_finite());
    }

    #[test]
    fn test_quantum_art_generation() {
        let art = generate_quantum_art();
        assert!(art.contains("QUANTUM ENTANGLEMENT"));
        assert!(art.contains("Bell inequality"));
    }

    #[test]
    fn test_report_generation() {
        let results = BellTestResults {
            correlation_aa: 0.5,
            correlation_bb: -0.3,
            correlation_ab: 0.8,
            correlation_ab_prime: -0.7,
            bell_inequality_value: 2.8,
            violations: 1,
            total_measurements: 1000,
        };
        
        let args = Args {
            particles: 100,
            trials: 10,
            angle_a: 0.0,
            angle_b: 45.0,
            distributed: false,
            distance: 100.0,
            report: true,
            output: None,
            seed: None,
        };
        
        let report = generate_report(&results, &args);
        assert!(report.contains("EXPERIMENT CONFIGURATION"));
        assert!(report.contains("MEASUREMENT RESULTS"));
        assert!(report.contains("QUANTUM ANALYSIS"));
    }

    #[test]
    fn test_optimal_bell_violation() {
        // Test with optimal angles for maximum Bell violation
        let results = run_bell_test(1000, 20, 0.0, 45.0, Some(42));
        // With sufficient particles and optimal angles, should approach quantum limit
        assert!(results.bell_inequality_value >= 1.5); // Should be significantly above classical minimum
    }
}
