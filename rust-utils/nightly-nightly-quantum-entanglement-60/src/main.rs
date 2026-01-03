use std::env;
use std::fs;
use std::path::Path;
use serde::{Deserialize, Serialize};
use clap::{Arg, Command};
use rand::prelude::*;

#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
enum Spin {
    Up,
    Down,
}

#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
struct Measurement {
    angle: f64,
    result: Spin,
}

#[derive(Debug, Serialize, Deserialize)]
struct ParticlePair {
    id: usize,
    alice_measurement: Measurement,
    bob_measurement: Measurement,
    distance_km: u64,
    correlated: bool,
}

#[derive(Serialize, Deserialize)]
struct SimulationResults {
    pairs: Vec<ParticlePair>,
    bell_correlation: f64,
    classical_limit: f64,
    quantum_violation: bool,
    violation_percentage: f64,
}

struct QuantumSimulator {
    rng: ThreadRng,
    num_pairs: usize,
    distance_km: u64,
}

impl QuantumSimulator {
    fn new(num_pairs: usize, distance_km: u64) -> Self {
        Self {
            rng: thread_rng(),
            num_pairs,
            distance_km,
        }
    }

    fn generate_entangled_pair(&mut self, pair_id: usize) -> ParticlePair {
        // Generate random measurement angles for Alice and Bob
        let alice_angle = self.rng.gen_range(0.0..360.0);
        let bob_angle = self.rng.gen_range(0.0..360.0);

        // For entangled particles, the correlation depends on the angle difference
        let angle_diff = (alice_angle - bob_angle).abs();
        let angle_diff = angle_diff.min(360.0 - angle_diff); // Normalize to [0, 180]

        // Quantum mechanical prediction: P(same) = sin²(Δθ/2), P(different) = cos²(Δθ/2)
        let prob_same = (angle_diff.to_radians() / 2.0).sin().powi(2);
        let prob_different = 1.0 - prob_same;

        let alice_result = if self.rng.gen_bool(0.5) { Spin::Up } else { Spin::Down };

        // Bob's result depends on the quantum correlation
        let bob_result = if self.rng.gen_bool(prob_different) {
            // Different result (anti-correlated)
            match alice_result {
                Spin::Up => Spin::Down,
                Spin::Down => Spin::Up,
            }
        } else {
            // Same result (correlated)
            alice_result
        };

        let correlated = alice_result != bob_result; // For singlet state, they should be anti-correlated

        ParticlePair {
            id: pair_id,
            alice_measurement: Measurement {
                angle: alice_angle,
                result: alice_result,
            },
            bob_measurement: Measurement {
                angle: bob_angle,
                result: bob_result,
            },
            distance_km: self.distance_km,
            correlated,
        }
    }

    fn calculate_bell_correlation(&self, pairs: &[ParticlePair]) -> f64 {
        // Simple Bell inequality test using CHSH inequality
        // We need to measure at different angle combinations
        let mut sum_a_b = 0.0;
        let mut sum_a_b_prime = 0.0;
        let mut sum_a_prime_b = 0.0;
        let mut sum_a_prime_b_prime = 0.0;

        let num_measurements = pairs.len().min(1000); // Use up to 1000 pairs for Bell test

        for pair in pairs.iter().take(num_measurements) {
            // Convert spins to +1/-1
            let alice_val = match pair.alice_measurement.result {
                Spin::Up => 1.0,
                Spin::Down => -1.0,
            };
            let bob_val = match pair.bob_measurement.result {
                Spin::Up => 1.0,
                Spin::Down => -1.0,
            };

            // For simplicity, we'll use fixed angle combinations
            // A=0°, A'=90°, B=45°, B'=135°
            // The actual angles in our simulation vary, so we'll approximate
            let angle_a = pair.alice_measurement.angle;
            let angle_b = pair.bob_measurement.angle;

            // Normalize angles to [0, 90] range for CHSH
            let norm_a = (angle_a % 90.0).to_radians();
            let norm_b = (angle_b % 90.0).to_radians();

            // Calculate correlation for this pair
            let correlation = alice_val * bob_val;

            // Distribute measurements across the four CHSH combinations
            // This is a simplified approach
            if angle_a < 45.0 && angle_b < 45.0 {
                sum_a_b += correlation;
            } else if angle_a < 45.0 && angle_b >= 45.0 {
                sum_a_b_prime += correlation;
            } else if angle_a >= 45.0 && angle_b < 45.0 {
                sum_a_prime_b += correlation;
            } else {
                sum_a_prime_b_prime += correlation;
            }
        }

        let count_a_b = pairs.iter().take(num_measurements).filter(|p| p.alice_measurement.angle < 45.0 && p.bob_measurement.angle < 45.0).count() as f64;
        let count_a_b_prime = pairs.iter().take(num_measurements).filter(|p| p.alice_measurement.angle < 45.0 && p.bob_measurement.angle >= 45.0).count() as f64;
        let count_a_prime_b = pairs.iter().take(num_measurements).filter(|p| p.alice_measurement.angle >= 45.0 && p.bob_measurement.angle < 45.0).count() as f64;
        let count_a_prime_b_prime = pairs.iter().take(num_measurements).filter(|p| p.alice_measurement.angle >= 45.0 && p.bob_measurement.angle >= 45.0).count() as f64;

        let avg_a_b = if count_a_b > 0.0 { sum_a_b / count_a_b } else { 0.0 };
        let avg_a_b_prime = if count_a_b_prime > 0.0 { sum_a_b_prime / count_a_b_prime } else { 0.0 };
        let avg_a_prime_b = if count_a_prime_b > 0.0 { sum_a_prime_b / count_a_prime_b } else { 0.0 };
        let avg_a_prime_b_prime = if count_a_prime_b_prime > 0.0 { sum_a_prime_b_prime / count_a_prime_b_prime } else { 0.0 };

        // CHSH value: |E(a,b) - E(a,b') + E(a',b) + E(a',b')|
        let chsh_value = (avg_a_b - avg_a_b_prime + avg_a_prime_b + avg_a_prime_b_prime).abs();

        chsh_value
    }

    fn run(&mut self) -> SimulationResults {
        println!("=== QUANTUM ENTANGLEMENT SIMULATION ===\n");
        println!("Generating {} entangled particle pairs...\n", self.num_pairs);

        let mut pairs = Vec::with_capacity(self.num_pairs);

        for i in 0..self.num_pairs {
            let pair = self.generate_entangled_pair(i + 1);
            pairs.push(pair.clone());

            // Show first 5 pairs in detail
            if i < 5 {
                self.print_pair_details(&pair);
            }
        }

        if self.num_pairs > 5 {
            println!("... and {} more particle pairs\n", self.num_pairs - 5);
        }

        // Calculate Bell inequality
        let bell_correlation = self.calculate_bell_correlation(&pairs);
        let classical_limit = 2.0; // Classical limit for CHSH inequality
        let quantum_violation = bell_correlation > classical_limit;
        let violation_percentage = if quantum_violation {
            ((bell_correlation - classical_limit) / classical_limit) * 100.0
        } else {
            0.0
        };

        println!("\nBELL INEQUALITY TEST:");
        println!("  Measured correlation: {:.3}", bell_correlation);
        println!("  Classical limit:      {:.3}", classical_limit);
        if quantum_violation {
            println!("  Quantum violation:    ✓ ({:.1}%)", violation_percentage);
        } else {
            println!("  Quantum violation:    ✗");
        }

        println!("\n\"Spooky action at a distance\" {}! 🎃👻", if quantum_violation { "confirmed" } else { "not detected" });

        SimulationResults {
            pairs,
            bell_correlation,
            classical_limit,
            quantum_violation,
            violation_percentage,
        }
    }

    fn print_pair_details(&self, pair: &ParticlePair) {
        let alice_spin = match pair.alice_measurement.result {
            Spin::Up => "Spin Up (+1)",
            Spin::Down => "Spin Down (-1)",
        };
        let bob_spin = match pair.bob_measurement.result {
            Spin::Up => "Spin Up (+1)",
            Spin::Down => "Spin Down (-1)",
        };

        println!("Particle Pair #{}:", pair.id);
        println!("  Alice measures: {} at angle {:.0}°", alice_spin, pair.alice_measurement.angle);
        println!("  Bob measures:   {} at angle {:.0}°", bob_spin, pair.bob_measurement.angle);
        println!("  Distance: {} km", pair.distance_km);
        println!("  Result: {}\n", if pair.correlated { "Perfect anti-correlation ✓" } else { "No correlation ✗" });
    }
}

fn main() {
    let matches = Command::new("nightly-quantum-entanglement-simulator")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("A whimsical quantum entanglement simulator")
        .arg(
            Arg::new("pairs")
                .short('p')
                .long("pairs")
                .value_name("NUM")
                .help("Number of entangled particle pairs to generate")
                .default_value("100")
        )
        .arg(
            Arg::new("distance")
                .short('d')
                .long("distance")
                .value_name("KM")
                .help("Distance between measurement stations in kilometers")
                .default_value("1000")
        )
        .arg(
            Arg::new("export")
                .short('e')
                .long("export")
                .value_name("FILE")
                .help("Export results to JSON file")
        )
        .get_matches();

    let num_pairs: usize = matches
        .get_one::<String>("pairs")
        .unwrap()
        .parse()
        .expect("Invalid number of pairs");

    let distance_km: u64 = matches
        .get_one::<String>("distance")
        .unwrap()
        .parse()
        .expect("Invalid distance");

    let export_file = matches.get_one::<String>("export");

    let mut simulator = QuantumSimulator::new(num_pairs, distance_km);
    let results = simulator.run();

    // Export results if requested
    if let Some(file_path) = export_file {
        match serde_json::to_string_pretty(&results) {
            Ok(json) => {
                match fs::write(file_path, json) {
                    Ok(_) => println!("\nResults exported to: {}", file_path),
                    Err(e) => eprintln!("Error writing to file {}: {}", file_path, e),
                }
            }
            Err(e) => eprintln!("Error serializing results: {}", e),
        }
    }
}
