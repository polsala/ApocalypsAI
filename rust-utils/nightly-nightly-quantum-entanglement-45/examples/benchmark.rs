use nightly_quantum_entanglement_checker::*;
use std::time::{Duration, Instant};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Quantum Entanglement Checker - Performance Benchmark\n");
    
    let test_cases = vec![
        (2, "1s"),
        (4, "2s"),
        (8, "3s"),
        (16, "5s"),
        (32, "10s"),
    ];
    
    println!("Running benchmarks with different node counts...");
    println!("{:<8} {:<8} {:<12} {:<15} {:<15} {:<15}", "Nodes", "Time", "Coherence", "Fidelity", "Latency(ms)", "Reliability");
    println!("{}", "-".repeat(80));
    
    for (nodes, duration_str) in test_cases {
        let duration = parse_duration(duration_str)?;
        
        // Quantum simulation
        let mut quantum_simulator = QuantumSimulator::new(nodes, 0.8, 0.03);
        let quantum_start = Instant::now();
        let quantum_results = quantum_simulator.run_simulation(duration, false).await;
        let quantum_time = quantum_start.elapsed();
        
        // Network simulation
        let mut network_simulator = NetworkSimulator::new(nodes);
        let network_start = Instant::now();
        let network_results = network_simulator.run_simulation(duration, false).await;
        let network_time = network_start.elapsed();
        
        // Calculate total time
        let total_time = quantum_time.max(network_time);
        
        println!(
            "{:<8} {:<8} {:<12.1} {:<15.2} {:<15.1} {:<15.1}",
            nodes,
            duration_str,
            quantum_results.coherence_level * 100.0,
            quantum_results.entanglement_fidelity,
            network_results.average_latency_ms,
            network_results.network_reliability * 100.0,
        );
        
        // Performance metrics
        let quantum_throughput = nodes as f64 / quantum_time.as_secs_f64();
        let network_throughput = nodes as f64 / network_time.as_secs_f64();
        
        println!(
            "         → Quantum: {:.2} nodes/sec, Network: {:.2} nodes/sec",
            quantum_throughput,
            network_throughput
        );
        
        println!();
    }
    
    // Stress test
    println!("🧪 Running stress test...");
    let stress_start = Instant::now();
    
    let mut stress_simulator = QuantumSimulator::new(64, 0.7, 0.05);
    let stress_results = stress_simulator.run_simulation(Duration::from_secs(15), false).await;
    
    let stress_duration = stress_start.elapsed();
    
    println!(
        "Stress test completed in {:.2}s with 64 nodes",
        stress_duration.as_secs_f64()
    );
    println!(
        "Final metrics: Coherence {:.1}%, Fidelity {:.2}, Bell Violation: {}",
        stress_results.coherence_level * 100.0,
        stress_results.entanglement_fidelity,
        if stress_results.bell_inequality_violation { "YES" } else { "NO" }
    );
    
    // Memory usage estimation
    println!("\n💾 Memory Usage Estimation:");
    println!("   Quantum State: ~{} KB per node", estimate_quantum_memory(64) / 1024);
    println!("   Network State: ~{} KB per node", estimate_network_memory(64) / 1024);
    
    println!("\n🎉 Benchmark completed successfully!");
    
    Ok(())
}

fn parse_duration(duration_str: &str) -> Result<Duration, Box<dyn std::error::Error>> {
    let duration_str = duration_str.to_lowercase();
    
    if duration_str.ends_with('s') {
        let seconds = duration_str.trim_end_matches('s').parse::<u64>()?;
        Ok(Duration::from_secs(seconds))
    } else if duration_str.ends_with('m') {
        let minutes = duration_str.trim_end_matches('m').parse::<u64>()?;
        Ok(Duration::from_secs(minutes * 60))
    } else if duration_str.contains('m') && duration_str.contains('s') {
        let parts: Vec<&str> = duration_str.split(&['m', 's'][..]).collect();
        if parts.len() >= 2 {
            let minutes = parts[0].parse::<u64>()?;
            let seconds = parts[1].parse::<u64>()?;
            Ok(Duration::from_secs(minutes * 60 + seconds))
        } else {
            Err("Invalid duration format".into())
        }
    } else {
        Err("Invalid duration format. Use formats like: 30s, 1m, 5m30s".into())
    }
}

fn estimate_quantum_memory(nodes: usize) -> usize {
    // Estimate memory for quantum state (correlation matrix + other data)
    let correlation_matrix_size = nodes * nodes * 8; // f64 = 8 bytes
    let other_data_size = nodes * 24; // coherence, fidelity, etc.
    correlation_matrix_size + other_data_size
}

fn estimate_network_memory(nodes: usize) -> usize {
    // Estimate memory for network state
    let latency_array_size = nodes * 8; // f64 = 8 bytes
    let packet_loss_array_size = nodes * 8;
    let sync_error_array_size = nodes * 8;
    latency_array_size + packet_loss_array_size + sync_error_array_size
}

// Example output:
// 
// 🔬 Quantum Entanglement Checker - Performance Benchmark
// 
// Running benchmarks with different node counts...
// Nodes   Time     Coherence    Fidelity      Latency(ms)   Reliability  
// --------------------------------------------------------------------------------
// 2        1s       78.5        0.75          12.3          95.2          
//          → Quantum: 2.00 nodes/sec, Network: 2.00 nodes/sec
// 
// 4        2s       76.2        0.72          14.1          93.8          
//          → Quantum: 2.00 nodes/sec, Network: 2.00 nodes/sec
// 
// 8        3s       74.8        0.69          16.7          91.5          
//          → Quantum: 2.67 nodes/sec, Network: 2.67 nodes/sec
// 
// 16       5s       72.1        0.65          19.8          89.2          
//          → Quantum: 3.20 nodes/sec, Network: 3.20 nodes/sec
// 
// 32       10s      68.9        0.60          23.4          85.7          
//          → Quantum: 3.20 nodes/sec, Network: 3.20 nodes/sec
// 
// 🧪 Running stress test...
// Stress test completed in 15.02s with 64 nodes
// Final metrics: Coherence 62.3%, Fidelity 0.52, Bell Violation: YES
// 
// 💾 Memory Usage Estimation:
//    Quantum State: ~32 KB per node
//    Network State: ~0 KB per node
// 
// 🎉 Benchmark completed successfully!
