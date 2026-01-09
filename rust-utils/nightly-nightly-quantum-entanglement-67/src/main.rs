use clap::{Parser, Subcommand};
use rand::prelude::*;
use std::time::Instant;

/// A whimsical quantum entanglement verification tool
#[derive(Parser)]
#[command(name = "nightly-quantum-entanglement-checker")]
#[command(about = "Simulates quantum entanglement verification using Bell's inequality")]
#[command(version = "1.0.0")]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Perform a basic entanglement verification
    Check,
    /// Generate detailed entanglement statistics
    Report {
        /// Number of samples to generate
        #[arg(short, long, default_value = "1000")]
        samples: usize,
    },
    /// Test entanglement across multiple simulated nodes
    Distributed {
        /// Number of nodes to simulate
        #[arg(short, long, default_value = "5")]
        nodes: usize,
        /// Number of measurement rounds
        #[arg(short, long, default_value = "100")]
        rounds: usize,
    },
}

fn main() {
    let cli = Cli::parse();

    match &cli.command {
        Commands::Check => check_entanglement(),
        Commands::Report { samples } => generate_report(*samples),
        Commands::Distributed { nodes, rounds } => distributed_test(*nodes, *rounds),
    }
}

fn check_entanglement() {
    println!("🔬 Quantum Entanglement Verification");
    println!("=====================================");
    
    let start = Instant::now();
    let result = simulate_bell_test(100);
    let duration = start.elapsed();
    
    println!("\n⏱️  Measurement Time: {:.2?}", duration);
    
    if result.violation > 2.0 {
        println!("✅ ENTANGLEMENT VERIFIED");
        println!("Bell Inequality Violation: {:.3}", result.violation);
        println!("Statistical Significance: {:.1}%", result.significance);
    } else {
        println!("❌ NO ENTANGLEMENT DETECTED");
        println!("Bell Parameter: {:.3}", result.violation);
    }
    
    print_quantum_art();
}

fn generate_report(samples: usize) {
    println!("📊 Quantum Entanglement Analysis Report");
    println!("=========================================");
    println!("\n🔬 Parameters:");
    println!("  - Sample Size: {}", samples);
    println!("  - Measurement Settings: A, A', B, B'");
    println!("  - Quantum State: |ψ⟩ = (|01⟩ - |10⟩)/√2");
    
    let start = Instant::now();
    let results = run_multiple_bell_tests(samples, 10);
    let duration = start.elapsed();
    
    println!("\n⏱️  Analysis Time: {:.2?}", duration);
    
    let avg_violation: f64 = results.iter().map(|r| r.violation).sum::<f64>() / results.len() as f64;
    let max_violation = results.iter().map(|r| r.violation).fold(f64::NEG_INFINITY, f64::max);
    let min_violation = results.iter().map(|r| r.violation).fold(f64::INFINITY, f64::min);
    
    println!("\n📈 Statistical Results:");
    println!("  - Average Bell Violation: {:.3}", avg_violation);
    println!("  - Maximum Violation: {:.3}", max_violation);
    println!("  - Minimum Violation: {:.3}", min_violation);
    
    let entangled_count = results.iter().filter(|r| r.violation > 2.0).count();
    let entanglement_rate = (entangled_count as f64 / results.len() as f64) * 100.0;
    
    println!("  - Entanglement Rate: {:.1}%", entanglement_rate);
    
    if avg_violation > 2.0 {
        println!("\n✅ CONCLUSION: Strong quantum correlations detected!");
        println!("   Your system exhibits non-local behavior consistent with entanglement.");
    } else {
        println!("\n❌ CONCLUSION: No significant entanglement observed.");
        println!("   Results are consistent with classical correlations.");
    }
    
    print_correlation_matrix(&results);
}

fn distributed_test(nodes: usize, rounds: usize) {
    println!("🌐 Distributed Quantum Entanglement Test");
    println!("=========================================");
    println!("\n📡 Network Configuration:");
    println!("  - Nodes: {}", nodes);
    println!("  - Measurement Rounds: {}", rounds);
    println!("  - Communication Protocol: Quantum Channel Simulation");
    
    let start = Instant::now();
    let mut rng = thread_rng();
    let mut global_violation = 0.0;
    let mut successful_nodes = 0;
    
    for node in 1..=nodes {
        print!("\nNode {}: [", node);
        let node_result = simulate_distributed_node(rounds, &mut rng);
        
        if node_result.violation > 2.0 {
            successful_nodes += 1;
            global_violation += node_result.violation;
            println!(" ✅ ] Entanglement Verified (Violation: {:.3})", node_result.violation);
        } else {
            println!(" ❌ ] No Entanglement (Violation: {:.3})", node_result.violation);
        }
    }
    
    let duration = start.elapsed();
    println!("\n⏱️  Total Network Time: {:.2?}", duration);
    
    let success_rate = (successful_nodes as f64 / nodes as f64) * 100.0;
    let avg_violation = if successful_nodes > 0 {
        global_violation / successful_nodes as f64
    } else {
        0.0
    };
    
    println!("\n📊 Network Statistics:");
    println!("  - Success Rate: {:.1}%", success_rate);
    println!("  - Average Violation (successful nodes): {:.3}", avg_violation);
    
    if success_rate > 50.0 {
        println!("\n✅ NETWORK STATUS: Quantum network is operational!");
        println!("   {}% of nodes exhibit quantum entanglement.", success_rate);
    } else {
        println!("\n⚠️  NETWORK STATUS: Classical behavior detected.");
        println!("   Consider checking your quantum channels.");
    }
}

#[derive(Debug)]
struct BellTestResult {
    violation: f64,
    significance: f64,
}

fn simulate_bell_test(samples: usize) -> BellTestResult {
    let mut rng = thread_rng();
    let mut correlations = [0.0; 4];
    
    // Bell test settings
    let settings = [
        (0.0, 0.0),      // A, B
        (0.0, std::f64::consts::PI / 4.0),  // A, B'
        (std::f64::consts::PI / 8.0, 0.0),  // A', B
        (std::f64::consts::PI / 8.0, std::f64::consts::PI / 4.0), // A', B'
    ];
    
    for (i, &(a, b)) in settings.iter().enumerate() {
        let mut sum = 0.0;
        for _ in 0..samples {
            // Simulate entangled particle measurement
            let hidden_var = rng.gen_range(0.0..std::f64::consts::TAU);
            let result_a = if (hidden_var.cos() * a.cos() + hidden_var.sin() * a.sin()) > 0.0 { 1.0 } else { -1.0 };
            let result_b = if (hidden_var.cos() * b.cos() + hidden_var.sin() * b.sin()) > 0.0 { 1.0 } else { -1.0 };
            sum += result_a * result_b;
        }
        correlations[i] = sum / samples as f64;
    }
    
    // Calculate Bell parameter
    let bell_parameter = correlations[0] - correlations[1] + correlations[2] + correlations[3];
    
    // Calculate statistical significance
    let standard_error = 2.0 / (samples as f64).sqrt();
    let significance = if bell_parameter > 2.0 {
        ((bell_parameter - 2.0) / standard_error).min(5.0) * 20.0
    } else {
        0.0
    };
    
    BellTestResult {
        violation: bell_parameter.abs(),
        significance: significance.min(100.0),
    }
}

fn run_multiple_bell_tests(samples: usize, tests: usize) -> Vec<BellTestResult> {
    (0..tests).map(|_| simulate_bell_test(samples)).collect()
}

fn simulate_distributed_node(rounds: usize, rng: &mut ThreadRng) -> BellTestResult {
    // Simulate network latency and quantum noise
    let noise_factor = rng.gen_range(0.95..1.05);
    let base_result = simulate_bell_test(rounds);
    
    BellTestResult {
        violation: base_result.violation * noise_factor,
        significance: base_result.significance * noise_factor,
    }
}

fn print_quantum_art() {
    println!("\n🌌 Quantum Visualization:");
    println!("   .·´  Quantum State  `·.");
    println!("  (   |ψ⟩ = (|01⟩-|10⟩)/√2   )");
    println!("   `·.                .·´");
    println!("      `·.          .·´");
    println!("         `·.    .·´");
    println!("            `··´");
}

fn print_correlation_matrix(results: &[BellTestResult]) {
    println!("\n🔗 Quantum Correlation Matrix:");
    let max_violation = results.iter().map(|r| r.violation).fold(f64::NEG_INFINITY, f64::max);
    let progress = (max_violation / 2.828 * 20.0) as usize; // 2.828 ≈ 2√2
    
    print!("[");
    for i in 0..20 {
        if i < progress {
            print!("████");
        } else {
            print!("    ");
        }
    }
    println!("] {:.1}% entangled", (max_violation / 2.828) * 100.0);
}
