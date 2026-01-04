use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::time::{SystemTime, UNIX_EPOCH};
use clap::{Arg, Command};
use rand::Rng;

#[derive(Debug, Serialize, Deserialize)]
struct EntanglementResult {
    timestamp: String,
    nodes: Vec<String>,
    entanglement_level: f64,
    status: String,
    message: String,
    certificate: Option<String>,
}

#[derive(Debug, Deserialize)]
struct Config {
    network: NetworkConfig,
    nodes: NodeConfig,
}

#[derive(Debug, Deserialize)]
struct NetworkConfig {
    threshold: f64,
    monitor_interval: u64,
}

#[derive(Debug, Deserialize)]
struct NodeConfig {
    participating: Vec<String>,
}

fn main() {
    let matches = Command::new("Quantum Entanglement Checker")
        .version("1.0.0")
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("nodes")
                .short('n')
                .long("nodes")
                .value_name("NODES")
                .help("Comma-separated list of node names")
                .required(false),
        )
        .arg(
            Arg::new("threshold")
                .short('t')
                .long("threshold")
                .value_name("THRESHOLD")
                .help("Entanglement threshold (0.0-1.0)")
                .default_value("0.75"),
        )
        .arg(
            Arg::new("certificate")
                .short('c')
                .long("certificate")
                .help("Generate entanglement certificate")
                .action(clap::ArgAction::SetTrue),
        )
        .arg(
            Arg::new("monitor")
                .short('m')
                .long("monitor")
                .help("Monitor entanglement continuously")
                .action(clap::ArgAction::SetTrue),
        )
        .arg(
            Arg::new("interval")
                .short('i')
                .long("interval")
                .value_name("SECONDS")
                .help("Monitor interval in seconds")
                .default_value("5"),
        )
        .arg(
            Arg::new("config")
                .short('f')
                .long("config")
                .value_name("FILE")
                .help("Configuration file path")
                .default_value("quantum.toml"),
        )
        .get_matches();

    let config_path = matches.get_one::<String>("config").unwrap();
    let config = load_config(config_path);
    
    let threshold: f64 = matches.get_one::<String>("threshold")
        .unwrap()
        .parse()
        .expect("Threshold must be a valid number between 0.0 and 1.0");
    
    let interval: u64 = matches.get_one::<String>("interval")
        .unwrap()
        .parse()
        .expect("Interval must be a valid number");

    let nodes = if let Some(nodes_str) = matches.get_one::<String>("nodes") {
        nodes_str.split(',').map(|s| s.trim().to_string()).collect()
    } else if !config.nodes.participating.is_empty() {
        config.nodes.participating.clone()
    } else {
        vec!["node1".to_string(), "node2".to_string(), "node3".to_string()]
    };

    if matches.get_flag("monitor") {
        monitor_entanglement(&nodes, threshold, interval);
    } else {
        let result = check_entanglement(&nodes, threshold);
        
        if matches.get_flag("certificate") {
            let cert = generate_certificate(&result);
            println!("{}", cert);
        } else {
            println!("{}", serde_json::to_string_pretty(&result).unwrap());
        }
    }
}

fn load_config(path: &str) -> Config {
    if Path::new(path).exists() {
        let content = fs::read_to_string(path).expect("Failed to read config file");
        toml::from_str(&content).expect("Failed to parse config file")
    } else {
        // Default config
        Config {
            network: NetworkConfig {
                threshold: 0.75,
                monitor_interval: 10,
            },
            nodes: NodeConfig {
                participating: vec![],
            },
        }
    }
}

fn check_entanglement(nodes: &[String], threshold: f64) -> EntanglementResult {
    let mut rng = rand::thread_rng();
    
    // Simulate quantum entanglement measurement
    let entanglement_level: f64 = rng.gen_range(0.0..1.0);
    
    let status = if entanglement_level >= threshold {
        "ENTANGLED".to_string()
    } else {
        "DECORRELATED".to_string()
    };
    
    let message = generate_quantum_message(entanglement_level, &status);
    
    let timestamp = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs()
        .to_string();
    
    EntanglementResult {
        timestamp,
        nodes: nodes.to_vec(),
        entanglement_level,
        status,
        message,
        certificate: None,
    }
}

fn monitor_entanglement(nodes: &[String], threshold: f64, interval: u64) {
    println!("Monitoring quantum entanglement...");
    println!("Nodes: {:?}", nodes);
    println!("Threshold: {:.2}", threshold);
    println!("Interval: {} seconds", interval);
    println!("Press Ctrl+C to stop\n");
    
    loop {
        let result = check_entanglement(nodes, threshold);
        println!("{}", serde_json::to_string_pretty(&result).unwrap());
        std::thread::sleep(std::time::Duration::from_secs(interval));
    }
}

fn generate_quantum_message(level: f64, status: &str) -> String {
    match status {
        "ENTANGLED" => {
            if level > 0.9 {
                "Quantum coherence achieved! Particles are perfectly synchronized across all nodes.".to_string()
            } else if level > 0.8 {
                "Strong entanglement detected. The quantum state is stable and reliable.".to_string()
            } else {
                "Entanglement confirmed. Quantum correlation is within acceptable parameters.".to_string()
            }
        },
        "DECORRELATED" => {
            if level < 0.3 {
                "Quantum decoherence detected! The system has collapsed into classical states.".to_string()
            } else {
                "Weak entanglement observed. Quantum correlation is below threshold.".to_string()
            }
        },
        _ => "Unknown quantum state detected.".to_string(),
    }
}

fn generate_certificate(result: &EntanglementResult) -> String {
    let status_symbol = if result.status == "ENTANGLED" { "✓" } else { "✗" };
    
    format!(
        "========================================\n"
        "QUANTUM ENTANGLEMENT CERTIFICATE\n"
        "========================================\n"
        "Timestamp: {}\n"
        "Status: {} {}\n"
        "Entanglement Level: {:.2}%\n"
        "Nodes: {}\n"
        "Message: {}\n"
        "========================================\n"
        "This certificate confirms the quantum\n"
        "state of the specified nodes at the\n"
        "time of verification.\n"
        "========================================",
        result.timestamp,
        status_symbol,
        result.status,
        result.entanglement_level * 100.0,
        result.nodes.join(", "),
        result.message
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;
    
    #[test]
    fn test_entanglement_check() {
        let nodes = vec!["node1".to_string(), "node2".to_string()];
        let result = check_entanglement(&nodes, 0.5);
        
        assert_eq!(result.nodes, nodes);
        assert!(result.entanglement_level >= 0.0 && result.entanglement_level <= 1.0);
        assert!(!result.timestamp.is_empty());
        assert!(!result.message.is_empty());
    }
    
    #[test]
    fn test_generate_quantum_message_entangled() {
        let message = generate_quantum_message(0.95, "ENTANGLED");
        assert!(message.contains("Quantum coherence"));
        
        let message = generate_quantum_message(0.85, "ENTANGLED");
        assert!(message.contains("Strong entanglement"));
        
        let message = generate_quantum_message(0.75, "ENTANGLED");
        assert!(message.contains("Entanglement confirmed"));
    }
    
    #[test]
    fn test_generate_quantum_message_decourrelated() {
        let message = generate_quantum_message(0.2, "DECORRELATED");
        assert!(message.contains("Quantum decoherence"));
        
        let message = generate_quantum_message(0.4, "DECORRELATED");
        assert!(message.contains("Weak entanglement"));
    }
    
    #[test]
    fn test_generate_certificate() {
        let result = EntanglementResult {
            timestamp: "1234567890".to_string(),
            nodes: vec!["node1".to_string(), "node2".to_string()],
            entanglement_level: 0.85,
            status: "ENTANGLED".to_string(),
            message: "Test message".to_string(),
            certificate: None,
        };
        
        let cert = generate_certificate(&result);
        assert!(cert.contains("QUANTUM ENTANGLEMENT CERTIFICATE"));
        assert!(cert.contains("✓ ENTANGLED"));
        assert!(cert.contains("85.00%"));
    }
    
    #[test]
    fn test_load_config_default() {
        let config = load_config("nonexistent.toml");
        assert_eq!(config.network.threshold, 0.75);
        assert_eq!(config.network.monitor_interval, 10);
        assert!(config.nodes.participating.is_empty());
    }
    
    #[test]
    fn test_load_config_custom() {
        let config_content = r#"
[network]
threshold = 0.8
monitor_interval = 5

[nodes]
participating = ["test1", "test2", "test3"]
"#;
        
        fs::write("test_config.toml", config_content).unwrap();
        let config = load_config("test_config.toml");
        
        assert_eq!(config.network.threshold, 0.8);
        assert_eq!(config.network.monitor_interval, 5);
        assert_eq!(config.nodes.participating, vec!["test1", "test2", "test3"]);
        
        fs::remove_file("test_config.toml").unwrap();
    }
}
