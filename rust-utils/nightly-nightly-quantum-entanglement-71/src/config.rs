use clap::ArgMatches;
use serde::{Deserialize, Serialize};
use std::time::Duration;
use std::fs;
use std::path::Path;

#[derive(Debug, Clone)]
pub struct Config {
    pub nodes: Vec<String>,
    pub quantum: QuantumConfig,
    pub distributed: bool,
    pub report_type: String,
    pub verbose: bool,
}

#[derive(Debug, Clone)]
pub struct QuantumConfig {
    pub entanglement_strength: f64,
    pub coherence_threshold: f64,
    pub latency_simulation: Duration,
}

impl Config {
    pub fn from_file(path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let content = fs::read_to_string(path)?;
        let toml_config: TomlConfig = toml::from_str(&content)?;
        
        Ok(Config {
            nodes: vec![
                toml_config.nodes.primary,
                toml_config.nodes.secondary,
            ],
            quantum: QuantumConfig {
                entanglement_strength: toml_config.quantum.entanglement_strength,
                coherence_threshold: toml_config.quantum.coherence_threshold,
                latency_simulation: parse_duration(&toml_config.quantum.latency_simulation)?,
            },
            distributed: false, // Default for file config
            report_type: "simple".to_string(),
            verbose: false,
        })
    }

    pub fn from_args(matches: &ArgMatches) -> Result<Self, Box<dyn std::error::Error>> {
        let nodes_str = matches.get_one::<String>("nodes").unwrap();
        let nodes: Vec<String> = nodes_str.split(',').map(|s| s.trim().to_string()).collect();
        
        let entanglement_strength = matches.get_one::<String>("strength")
            .unwrap()
            .parse::<f64>()?;
        
        let coherence_threshold = matches.get_one::<String>("coherence-threshold")
            .unwrap()
            .parse::<f64>()?;
        
        let latency_simulation = parse_duration(matches.get_one::<String>("latency").unwrap())?;
        
        Ok(Config {
            nodes,
            quantum: QuantumConfig {
                entanglement_strength: entanglement_strength.clamp(0.0, 1.0),
                coherence_threshold: coherence_threshold.clamp(0.0, 1.0),
                latency_simulation,
            },
            distributed: matches.get_flag("distributed"),
            report_type: matches.get_one::<String>("report").unwrap().clone(),
            verbose: matches.get_flag("verbose"),
        })
    }
}

fn parse_duration(duration_str: &str) -> Result<Duration, Box<dyn std::error::Error>> {
    if duration_str == "0ms" {
        return Ok(Duration::from_millis(0));
    }
    
    if let Some(ms_pos) = duration_str.find("ms") {
        let num_str = &duration_str[..ms_pos];
        let ms = num_str.parse::<u64>()?;
        return Ok(Duration::from_millis(ms));
    }
    
    if let Some(s_pos) = duration_str.find('s') {
        let num_str = &duration_str[..s_pos];
        let seconds = num_str.parse::<u64>()?;
        return Ok(Duration::from_secs(seconds));
    }
    
    Err("Invalid duration format. Use '50ms' or '1s'".into())
}

#[derive(Deserialize)]
struct TomlConfig {
    nodes: TomlNodes,
    quantum: TomlQuantum,
}

#[derive(Deserialize)]
struct TomlNodes {
    primary: String,
    secondary: String,
}

#[derive(Deserialize)]
struct TomlQuantum {
    entanglement_strength: f64,
    coherence_threshold: f64,
    latency_simulation: String,
}

#[cfg(test)]
mod tests {
    use super::*;
    use clap::{Arg, Command};
    use tempfile::NamedTempFile;
    use std::io::Write;

    #[test]
    fn test_parse_duration_ms() {
        let duration = parse_duration("50ms").unwrap();
        assert_eq!(duration, Duration::from_millis(50));
    }

    #[test]
    fn test_parse_duration_seconds() {
        let duration = parse_duration("2s").unwrap();
        assert_eq!(duration, Duration::from_secs(2));
    }

    #[test]
    fn test_parse_duration_zero() {
        let duration = parse_duration("0ms").unwrap();
        assert_eq!(duration, Duration::from_millis(0));
    }

    #[test]
    fn test_config_from_args() {
        let matches = Command::new("test")
            .arg(Arg::new("nodes").required(true))
            .arg(Arg::new("strength").default_value("0.75"))
            .arg(Arg::new("coherence-threshold").default_value("0.8"))
            .arg(Arg::new("latency").default_value("0ms"))
            .get_matches_from(vec![
                "test", 
                "--nodes", "node1,node2", 
                "--strength", "0.85",
                "--coherence-threshold", "0.9",
                "--latency", "100ms"
            ]);
        
        let config = Config::from_args(&matches).unwrap();
        assert_eq!(config.nodes, vec!["node1", "node2"]);
        assert_eq!(config.quantum.entanglement_strength, 0.85);
        assert_eq!(config.quantum.coherence_threshold, 0.9);
        assert_eq!(config.quantum.latency_simulation, Duration::from_millis(100));
    }
}
