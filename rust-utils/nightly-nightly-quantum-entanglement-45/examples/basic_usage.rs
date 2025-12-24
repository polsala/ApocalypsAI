use nightly_quantum_entanglement_checker::*;
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Quantum Entanglement Checker - Basic Usage Example\n");
    
    // Create a quantum simulator
    let mut quantum_simulator = QuantumSimulator::new(
        6,           // 6 nodes
        0.85,        // High entanglement strength
        0.02         // Low decoherence rate
    );
    
    // Run quantum simulation
    println!("⚛️  Running quantum simulation...");
    let quantum_results = quantum_simulator.run_simulation(
        Duration::from_secs(2),
        true  // verbose output
    ).await;
    
    println!("\n✅ Quantum simulation completed!");
    println!("   Coherence Level: {:.1}%", quantum_results.coherence_level * 100.0);
    println!("   Entanglement Fidelity: {:.2}", quantum_results.entanglement_fidelity);
    println!("   Bell Inequality Violation: {}", if quantum_results.bell_inequality_violation { "YES" } else { "NO" });
    
    // Create a network simulator
    let mut network_simulator = NetworkSimulator::new(6);
    
    // Run network simulation
    println!("\n📡 Running network simulation...");
    let network_results = network_simulator.run_simulation(
        Duration::from_secs(2),
        true  // verbose output
    ).await;
    
    println!("\n✅ Network simulation completed!");
    println!("   Average Latency: {:.1}ms", network_results.average_latency_ms);
    println!("   Packet Loss: {:.2}%", network_results.packet_loss_percent);
    println!("   Network Reliability: {:.1}%", network_results.network_reliability * 100.0);
    
    // Generate a report
    let report = QuantumReport {
        experiment_parameters: ExperimentParameters {
            nodes: 6,
            duration: "2s".to_string(),
            entanglement_strength: 0.85,
            decoherence_rate: 0.02,
        },
        quantum_state_analysis: quantum_results,
        network_metrics: network_results,
        result: QuantumResult {
            success: quantum_results.entanglement_fidelity > 0.5,
            message: if quantum_results.entanglement_fidelity > 0.5 {
                "QUANTUM ENTANGLEMENT SUCCESSFUL".to_string()
            } else {
                "QUANTUM ENTANGLEMENT FAILED".to_string()
            },
            spooky_action_confirmed: quantum_results.bell_inequality_violation,
            confidence_level: quantum_results.entanglement_fidelity,
        },
        timestamp: chrono::Utc::now().to_rfc3339(),
    };
    
    println!("\n📋 Generating report...");
    let generator = ReportGenerator::new(ReportFormat::Text);
    generator.generate_report(&report);
    
    println!("\n🎉 Example completed successfully!");
    
    Ok(())
}

// Example output:
// 
// 🔬 Quantum Entanglement Checker - Basic Usage Example
// 
// ⚛️  Running quantum simulation...
// ⏱️  Total execution time: 2.00s
// ✅ Quantum simulation completed!
//    Coherence Level: 82.3%
//    Entanglement Fidelity: 0.79
//    Bell Inequality Violation: YES
// 
// 📡 Running network simulation...
// ✅ Network simulation completed!
//    Average Latency: 15.2ms
//    Packet Loss: 0.15%
//    Network Reliability: 94.2%
// 
// 📋 Generating report...
// 
// 🔬 Quantum Entanglement Verification Report
// ==================================================
// 
// 📍 Experiment Parameters:
//    • Nodes: 6
//    • Duration: 2s
//    • Entanglement Strength: 0.85
//    • Decoherence Rate: 0.02
// 
// ⚛️  Quantum State Analysis:
//    • Coherence Level: 82.3%
//    • Entanglement Fidelity: 0.79
//    • Bell Inequality Violation: ✅ CONFIRMED
//    • Quantum Correlation Score: 0.76
// 
// 📡 Network Metrics:
//    • Average Latency: 15.2ms
//    • Packet Loss: 0.15%
//    • Synchronization Error: ±8.3ns
//    • Network Reliability: 94.2%
// 
// 🎉 Result: QUANTUM ENTANGLEMENT SUCCESSFUL
//    Spooky action at a distance: CONFIRMED
//    Confidence Level: 79.0%
// 
//     ╔══════════════════════════════════════╗
//     ║  🌀 QUANTUM ENTANGLEMENT ZONE 🌀   ║
//     ║                                    ║
//     ║    ⚛️  Spooky Action Detected! ⚛️   ║
//     ║                                    ║
//     ║  📡 Maintaining Coherence... 📡    ║
//     ╚══════════════════════════════════════╝
// 
// 🕒 Report generated at: 2024-01-01T12:00:00Z
// 
// 🎉 Example completed successfully!
