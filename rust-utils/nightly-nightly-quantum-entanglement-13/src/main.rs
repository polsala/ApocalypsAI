use std::env;
use std::time::Duration;
use std::net::IpAddr;
use std::str::FromStr;
use tokio::time::timeout;
use rand::Rng;

mod quantum_sim;
mod network_checker;

use quantum_sim::QuantumEntanglementSimulator;
use network_checker::NetworkChecker;

#[derive(Debug)]
struct Config {
    nodes: Vec<IpAddr>,
    threshold: f64,
    timeout_ms: u64,
}

impl Default for Config {
    fn default() -> Self {
        Self {
            nodes: vec!["127.0.0.1".parse().unwrap()],
            threshold: 0.7,
            timeout_ms: 5000,
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("🔬 Quantum Entanglement Checker v1.0");
    println!("=====================================");
    println!("\n📡 Spooky action at a distance detected!\n");

    let config = parse_args();
    
    let simulator = QuantumEntanglementSimulator::new();
    let network_checker = NetworkChecker::new(config.timeout_ms);
    
    let mut total_coherence = 0.0;
    let mut stable_nodes = 0;
    let mut all_nodes_stable = true;
    
    for (i, node) in config.nodes.iter().enumerate() {
        println!("Node: {}", node);
        
        // Check network connectivity first
        let network_ok = timeout(
            Duration::from_millis(config.timeout_ms),
            network_checker.ping(node)
        ).await??;
        
        if !network_ok {
            println!("  - Network status: ❌ UNREACHABLE");
            println!("  - Quantum coherence: N/A");
            println!("  - Entanglement status: 🚫 DISCONNECTED");
            println!("  - Measurement collapsed: Yes\n");
            all_nodes_stable = false;
            continue;
        }
        
        // Simulate quantum measurement
        let measurement = simulator.measure_entanglement();
        
        println!("  - Quantum coherence: {:.3} ({:.1}%)", 
                 measurement.coherence, measurement.coherence * 100.0);
        
        if measurement.coherence >= config.threshold {
            println!("  - Entanglement status: ✨ SUPERPOSED");
            println!("  - Measurement collapsed: No");
            stable_nodes += 1;
            total_coherence += measurement.coherence;
        } else {
            println!("  - Entanglement status: 🔄 COLLAPSED");
            println!("  - Measurement collapsed: Yes");
            all_nodes_stable = false;
        }
        
        if i < config.nodes.len() - 1 {
            println!("");
        }
    }
    
    // Overall system status
    println!("\n🎉 Overall system entanglement: ", end="");
    if stable_nodes > 0 {
        let avg_coherence = total_coherence / stable_nodes as f64;
        println!("{:.1}% ({})", 
                 avg_coherence * 100.0,
                 if all_nodes_stable { "STABLE" } else { "PARTIAL" });
    } else {
        println!("0.0% (UNSTABLE)");
    }
    
    Ok(())
}

fn parse_args() -> Config {
    let mut args = env::args().skip(1);
    let mut config = Config::default();
    
    while let Some(arg) = args.next() {
        match arg.as_str() {
            "--nodes" => {
                if let Some(nodes_str) = args.next() {
                    config.nodes = nodes_str
                        .split(',')
                        .filter_map(|s| IpAddr::from_str(s.trim()).ok())
                        .collect();
                    if config.nodes.is_empty() {
                        eprintln!("❌ Invalid node list. Use comma-separated IP addresses.");
                        std::process::exit(1);
                    }
                }
            },
            "--threshold" => {
                if let Some(threshold_str) = args.next() {
                    match threshold_str.parse::<f64>() {
                        Ok(val) if val >= 0.0 && val <= 1.0 => config.threshold = val,
                        _ => {
                            eprintln!("❌ Threshold must be between 0.0 and 1.0");
                            std::process::exit(1);
                        }
                    }
                }
            },
            "--timeout" => {
                if let Some(timeout_str) = args.next() {
                    match timeout_str.parse::<u64>() {
                        Ok(val) if val > 0 => config.timeout_ms = val,
                        _ => {
                            eprintln!("❌ Timeout must be a positive number (ms)");
                            std::process::exit(1);
                        }
                    }
                }
            },
            "--help" | "-h" => {
                print_help();
                std::process::exit(0);
            },
            _ => {
                eprintln!("❌ Unknown argument: {}. Use --help for usage.", arg);
                std::process::exit(1);
            }
        }
    }
    
    config
}

fn print_help() {
    println!("Quantum Entanglement Checker - Usage:");
    println!("=====================================");
    println!("\nBasic:");
    println!("  cargo run -- --nodes 192.168.1.100,192.168.1.101");
    println!("\nAdvanced:");
    println!("  cargo run -- --nodes 192.168.1.100,192.168.1.101 --threshold 0.7 --timeout 5000");
    println!("\nOptions:");
    println!("  --nodes <IP1,IP2,...>  Comma-separated list of IP addresses");
    println!("  --threshold <0.0-1.0>   Entanglement threshold (default: 0.7)");
    println!("  --timeout <ms>          Network timeout in milliseconds (default: 5000)");
    println!("  --help, -h              Show this help message");
}
