use std::collections::HashMap;
use std::time::{Duration, Instant};
use std::thread;
use std::env;
use rand::Rng;

mod quantum_simulator;
mod metrics;
mod cli;

use quantum_simulator::QuantumSimulator;
use metrics::QuantumMetrics;
use cli::parse_args;

/// Main entry point for the Quantum Entanglement Checker
fn main() {
    println!("🔬 Quantum Entanglement Checker v1.0");
    println!("=====================================");
    println!();

    let args = parse_args();

    if args.metrics {
        run_metrics_monitoring(args.interval);
    } else if args.verify {
        run_verification(args.nodes, args.threshold);
    } else {
        run_entanglement_check(args.nodes);
    }
}

/// Run entanglement checking between specified nodes
fn run_entanglement_check(nodes: Vec<String>) {
    if nodes.is_empty() {
        println!("❌ No nodes specified. Use --nodes to specify at least one node.");
        return;
    }

    println!("📡 Checking entanglement between nodes: {}", nodes.join(", "));
    println!();

    let simulator = QuantumSimulator::new();
    let mut all_entangled = true;

    // Check entanglement between all pairs of nodes
    for i in 0..nodes.len() {
        for j in (i + 1)..nodes.len() {
            let fidelity = simulator.check_entanglement(&nodes[i], &nodes[j]);
            
            if fidelity >= 0.8 {
                println!("✓ {} ↔ {}: Entangled (fidelity: {:.2})", 
                         nodes[i], nodes[j], fidelity);
            } else {
                println!("⚠ {} ↔ {}: Weak entanglement (fidelity: {:.2})", 
                         nodes[i], nodes[j], fidelity);
                all_entangled = false;
            }
        }
    }

    println!();
    
    if all_entangled {
        println!("✨ Quantum coherence maintained across all nodes!");
    } else {
        println!("⚠ Quantum decoherence detected. Consider recalibrating your nodes.");
    }
}

/// Run verification with threshold
fn run_verification(nodes: Vec<String>, threshold: f64) {
    println!("🔍 Verifying synchronization with threshold: {:.2}", threshold);
    println!();

    let simulator = QuantumSimulator::new();
    let mut passed = 0;
    let mut total = 0;

    for i in 0..nodes.len() {
        for j in (i + 1)..nodes.len() {
            total += 1;
            let fidelity = simulator.check_entanglement(&nodes[i], &nodes[j]);
            
            if fidelity >= threshold {
                println!("✓ {} ↔ {}: PASS (fidelity: {:.2})", 
                         nodes[i], nodes[j], fidelity);
                passed += 1;
            } else {
                println!("❌ {} ↔ {}: FAIL (fidelity: {:.2})", 
                         nodes[i], nodes[j], fidelity);
            }
        }
    }

    println!();
    println!("📊 Verification Results:");
    println!("- Passed: {}/{} ({:.1}%)", passed, total, (passed as f64 / total as f64) * 100.0);
    
    if passed == total {
        println!("🎉 All nodes passed verification!");
    } else {
        println!("⚠ Some nodes failed verification. Check entanglement strength.");
    }
}

/// Run continuous metrics monitoring
fn run_metrics_monitoring(interval: u64) {
    println!("📡 Starting quantum metrics monitoring...");
    println!("⏱️  Interval: {} seconds", interval);
    println!();

    let simulator = QuantumSimulator::new();
    let metrics = QuantumMetrics::new();
    let start_time = Instant::now();

    loop {
        println!("📊 Quantum Metrics (Uptime: {:.1}s):", start_time.elapsed().as_secs_f64());
        
        let current_metrics = metrics.generate_current_metrics();
        
        println!("- Superposition stability: {:.0}%", current_metrics.superposition_stability * 100.0);
        println!("- Entanglement fidelity: {:.0}%", current_metrics.entanglement_fidelity * 100.0);
        println!("- Decoherence resistance: {:.0}%", current_metrics.decoherence_resistance * 100.0);
        println!("- Quantum tunneling events: {}", current_metrics.tunneling_events);
        
        // Simulate some quantum events
        let quantum_events = simulator.simulate_quantum_events();
        if !quantum_events.is_empty() {
            println!("🔮 Quantum Events:");
            for event in quantum_events {
                println!("  • {}", event);
            }
        }
        
        println!();
        
        // Wait for the specified interval
        thread::sleep(Duration::from_secs(interval));
    }
}
