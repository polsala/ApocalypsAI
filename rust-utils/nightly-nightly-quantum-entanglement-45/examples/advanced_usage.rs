use nightly_quantum_entanglement_checker::*;
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Debug, Deserialize, Serialize)]
struct QuantumExperimentConfig {
    nodes: usize,
    duration: String,
    entanglement_strength: f64,
    decoherence_rate: f64,
    network_mode: bool,
    output_format: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Quantum Entanglement Checker - Advanced Usage Example\n");
    
    // Create a configuration
    let config = QuantumExperimentConfig {
        nodes: 8,
        duration: "10s".to_string(),
        entanglement_strength: 0.9,
        decoherence_rate: 0.01,
        network_mode: true,
        output_format: "json".to_string(),
    };
    
    println!("⚙️  Experiment Configuration:");
    println!("   Nodes: {}", config.nodes);
    println!("   Duration: {}", config.duration);
    println!("   Entanglement Strength: {:.2}", config.entanglement_strength);
    println!("   Decoherence Rate: {:.3}", config.decoherence_rate);
    println!("   Network Mode: {}", if config.network_mode { "ENABLED" } else { "DISABLED" });
    println!("   Output Format: {}", config.output_format);
    
    // Parse duration
    let duration = parse_duration(&config.duration)?;
    
    // Create simulators
    let mut quantum_simulator = QuantumSimulator::new(
        config.nodes,
        config.entanglement_strength,
        config.decoherence_rate,
    );
    
    let mut network_simulator = NetworkSimulator::new(config.nodes);
    
    // Run simulations
    println!("\n⚛️  Running quantum simulation...");
    let quantum_results = quantum_simulator.run_simulation(duration, false).await;
    
    let network_results = if config.network_mode {
        println!("\n📡 Running network simulation...");
        Some(network_simulator.run_simulation(duration, false).await)
    } else {
        None
    };
    
    // Create comprehensive report
    let report = QuantumReport {
        experiment_parameters: ExperimentParameters {
            nodes: config.nodes,
            duration: config.duration,
            entanglement_strength: config.entanglement_strength,
            decoherence_rate: config.decoherence_rate,
        },
        quantum_state_analysis: quantum_results,
        network_metrics: network_results.unwrap_or_default(),
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
    
    // Generate report in specified format
    let format = ReportFormat::from_string(&config.output_format);
    let generator = ReportGenerator::new(format);
    
    println!("\n📋 Generating {} report...", config.output_format.to_uppercase());
    generator.generate_report(&report);
    
    // Performance analysis
    println!("\n📊 Performance Analysis:");
    println!("   Quantum Coherence: {:.1}%", report.quantum_state_analysis.coherence_level * 100.0);
    println!("   Entanglement Quality: {:.1}%", report.quantum_state_analysis.entanglement_fidelity * 100.0);
    println!("   Network Reliability: {:.1}%", report.network_metrics.network_reliability * 100.0);
    
    if report.quantum_state_analysis.bell_inequality_violation {
        println!("   🎉 Bell's Inequality Violated - True Quantum Entanglement!");
    } else {
        println!("   ⚠️  Bell's Inequality Not Violated - Classical Correlations Only");
    }
    
    // Save configuration for future use
    let config_toml = toml::to_string(&config)?;
    std::fs::write("quantum_experiment_config.toml", config_toml)?;
    println!("\n💾 Configuration saved to: quantum_experiment_config.toml");
    
    println!("\n🎉 Advanced example completed successfully!");
    
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

// Example output:
// 
// 🔬 Quantum Entanglement Checker - Advanced Usage Example
// 
// ⚙️  Experiment Configuration:
//    Nodes: 8
//    Duration: 10s
//    Entanglement Strength: 0.90
//    Decoherence Rate: 0.010
//    Network Mode: ENABLED
//    Output Format: json
// 
// ⚛️  Running quantum simulation...
// 📡 Running network simulation...
// 
// 📋 Generating JSON report...
// {
//   "experiment_parameters": {
//     "nodes": 8,
//     "duration": "10s",
//     "entanglement_strength": 0.9,
//     "decoherence_rate": 0.01
//   },
//   "quantum_state_analysis": {
//     "coherence_level": 0.89,
//     "entanglement_fidelity": 0.87,
//     "bell_inequality_violation": true,
//     "quantum_correlation_score": 0.85
//   },
//   "network_metrics": {
//     "average_latency_ms": 11.2,
//     "packet_loss_percent": 0.08,
//     "synchronization_error_ns": 4.1,
//     "network_reliability": 0.96
//   },
//   "result": {
//     "success": true,
//     "message": "QUANTUM ENTANGLEMENT SUCCESSFUL",
//     "spooky_action_confirmed": true,
//     "confidence_level": 0.87
//   },
//   "timestamp": "2024-01-01T12:00:00Z"
// }
// 
// 📊 Performance Analysis:
//    Quantum Coherence: 89.0%
//    Entanglement Quality: 87.0%
//    Network Reliability: 96.0%
//    🎉 Bell's Inequality Violated - True Quantum Entanglement!
// 
// 💾 Configuration saved to: quantum_experiment_config.toml
// 
// 🎉 Advanced example completed successfully!
