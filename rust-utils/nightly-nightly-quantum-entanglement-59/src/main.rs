use std::env;
use std::time::{Duration, Instant};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
enum Spin {
    Up,
    Down,
}

#[derive(Debug, Clone, PartialEq)]
enum Polarization {
    Horizontal,
    Vertical,
    Diagonal,
    AntiDiagonal,
}

#[derive(Debug, Clone)]
struct Particle {
    id: u64,
    spin: Spin,
    polarization: Polarization,
    decoherence_time: Duration,
}

#[derive(Debug, Clone)]
struct MeasurementResult {
    particle_id: u64,
    basis: f64, // Measurement basis in degrees
n    value: i8,  // +1 or -1
}

#[derive(Debug)]
struct EntangledPair {
    particle_a: Particle,
    particle_b: Particle,
    creation_time: Instant,
}

impl EntangledPair {
    fn new(id: u64) -> Self {
        // Generate entangled particles with opposite properties
        let spin_a = if rand_bool() { Spin::Up } else { Spin::Down };
        let spin_b = match spin_a {
            Spin::Up => Spin::Down,
            Spin::Down => Spin::Up,
        };

        let polarization_a = match rand_range(0, 4) {
            0 => Polarization::Horizontal,
            1 => Polarization::Vertical,
            2 => Polarization::Diagonal,
            _ => Polarization::AntiDiagonal,
        };

        let polarization_b = match polarization_a {
            Polarization::Horizontal => Polarization::Vertical,
            Polarization::Vertical => Polarization::Horizontal,
            Polarization::Diagonal => Polarization::AntiDiagonal,
            Polarization::AntiDiagonal => Polarization::Diagonal,
        };

        EntangledPair {
            particle_a: Particle {
                id: id * 2,
                spin: spin_a,
                polarization: polarization_a,
                decoherence_time: Duration::from_secs_f64(rand_range_f64(0.01, 0.1)),
            },
            particle_b: Particle {
                id: id * 2 + 1,
                spin: spin_b,
                polarization: polarization_b,
                decoherence_time: Duration::from_secs_f64(rand_range_f64(0.01, 0.1)),
            },
            creation_time: Instant::now(),
        }
    }

    fn measure(&self, basis: f64) -> (MeasurementResult, MeasurementResult) {
        // Simulate quantum measurement with potential decoherence
        let decoherence_a = self.creation_time.elapsed() > self.particle_a.decoherence_time;
        let decoherence_b = self.creation_time.elapsed() > self.particle_b.decoherence_time;

        let value_a = if decoherence_a {
            // Decohered - random result
            if rand_bool() { 1 } else { -1 }
        } else {
            // Entangled - correlated result
            measure_spin(&self.particle_a, basis)
        };

        let value_b = if decoherence_b {
            // Decohered - random result
            if rand_bool() { 1 } else { -1 }
        } else {
            // Entangled - anti-correlated result
            -value_a
        };

        (
            MeasurementResult {
                particle_id: self.particle_a.id,
                basis,
                value: value_a,
            },
            MeasurementResult {
                particle_id: self.particle_b.id,
                basis,
                value: value_b,
            },
        )
    }
}

fn measure_spin(particle: &Particle, basis: f64) -> i8 {
    // Simplified quantum measurement simulation
    let angle_diff = match particle.polarization {
        Polarization::Horizontal => (basis % 180.0).abs(),
        Polarization::Vertical => ((basis - 90.0) % 180.0).abs(),
        Polarization::Diagonal => ((basis - 45.0) % 180.0).abs(),
        Polarization::AntiDiagonal => ((basis - 135.0) % 180.0).abs(),
    };

    // Probability of getting +1 based on angle difference
    let probability = (angle_diff.to_radians()).cos().abs();
    
    if rand_range_f64(0.0, 1.0) < probability {
        1
    } else {
        -1
    }
}

// Simple pseudo-random number generator (no external dependencies)
fn rand_range(min: u64, max: u64) -> u64 {
    let seed = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos() as u64;
    
    let mut x = seed;
    x = x.wrapping_mul(6364136223846793005).wrapping_add(1);
    ((x >> 32) % (max - min)) + min
}

fn rand_range_f64(min: f64, max: f64) -> f64 {
    let r = rand_range(0, u64::MAX / 2) as f64 / (u64::MAX as f64 / 2.0);
    min + r * (max - min)
}

fn rand_bool() -> bool {
    rand_range(0, 2) == 1
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    let mut pairs = 100;
    let mut basis = 0.0;
    
    // Parse command line arguments
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--pairs" => {
                if i + 1 < args.len() {
                    pairs = args[i + 1].parse().unwrap_or(100);
                    i += 1;
                }
            },
            "--basis" => {
                if i + 1 < args.len() {
                    basis = args[i + 1].parse().unwrap_or(0.0);
                    i += 1;
                }
            },
            _ => {},
        }
        i += 1;
    }
    
    println!("Generating {} entangled particle pairs...\n", pairs);
    
    let mut perfect_correlations = 0;
    let mut total_decoherence_time = Duration::ZERO;
    
    for i in 0..pairs {
        let pair = EntangledPair::new(i);
        
        let (result_a, result_b) = pair.measure(basis);
        
        // Check for perfect anti-correlation
        let is_perfect = result_a.value == -result_b.value;
        if is_perfect {
            perfect_correlations += 1;
        }
        
        total_decoherence_time += pair.particle_a.decoherence_time;
        total_decoherence_time += pair.particle_b.decoherence_time;
        
        println!("Particle A: Spin={:?}, Polarization={:?}, Measurement={}", 
                 pair.particle_a.spin, pair.particle_a.polarization, result_a.value);
        println!("Particle B: Spin={:?}, Polarization={:?}, Measurement={}", 
                 pair.particle_b.spin, pair.particle_b.polarization, result_b.value);
        
        if is_perfect {
            println!("Correlation: Perfect anti-correlation (spooky!)\n");
        } else {
            println!("Correlation: Imperfect correlation (decoherence detected)\n");
        }
    }
    
    let imperfect_correlations = pairs - perfect_correlations;
    let avg_decoherence = total_decoherence_time / (pairs * 2) as u32;
    
    println!("Summary Statistics:");
    println!("- Total pairs: {}", pairs);
    println!("- Perfect correlations: {} ({}%)", 
             perfect_correlations, (perfect_correlations as f64 / pairs as f64) * 100.0);
    println!("- Imperfect correlations: {} ({}%)", 
             imperfect_correlations, (imperfect_correlations as f64 / pairs as f64) * 100.0);
    println!("- Average decoherence time: {:.3} seconds\n", 
             avg_decoherence.as_secs_f64());
    
    println!("Remember: No information was transmitted faster than light! (Probably.)");
}
