use clap::{Parser, Subcommand};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::process::Command;
use std::time::{Duration, Instant};
use std::sync::{Arc, Mutex};
use std::thread;
use std::io::{self, Write};
use chrono::{Utc, Local};

/// A blazing-fast chaos engineering CLI tool
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand, Debug)]
enum Commands {
    /// List available chaos scenarios
    ListScenarios,
    /// Run chaos scenarios
    Run {
        /// Scenario to execute
        #[arg(short, long)]
        scenario: Vec<String>,
        /// Duration of chaos (e.g., 30s, 2m, 1h)
        #[arg(short, long)]
        duration: Option<String>,
        /// Intensity of chaos (0-100)
        #[arg(short, long)]
        intensity: Option<u8>,
        /// Latency to add to network (e.g., 100ms, 1s)
        #[arg(short, long)]
        latency: Option<String>,
        /// Packet loss percentage (e.g., 10%)
        #[arg(short, long)]
        loss: Option<String>,
        /// Bandwidth limit (e.g., 1mbps, 100kbps)
        #[arg(short, long)]
        bandwidth: Option<String>,
        /// Memory to consume (e.g., 1gb, 512mb)
        #[arg(short, long)]
        memory: Option<String>,
        /// Service to target
        #[arg(short, long)]
        service: Option<String>,
        /// Time offset (e.g., +1h, -30m)
        #[arg(short, long)]
        offset: Option<String>,
        /// Maximum time offset for random jumps
        #[arg(short, long)]
        max_offset: Option<String>,
        /// Start intensity for ramp scenarios
        #[arg(short, long)]
        start_intensity: Option<u8>,
        /// End intensity for ramp scenarios
        #[arg(short, long)]
        end_intensity: Option<u8>,
        /// Start memory for ramp scenarios
        #[arg(short, long)]
        start_memory: Option<String>,
        /// End memory for ramp scenarios
        #[arg(short, long)]
        end_memory: Option<String>,
        /// Duration of ramp phase
        #[arg(short, long)]
        ramp_duration: Option<String>,
        /// Run in background
        #[arg(short, long)]
        background: bool,
        /// Dry run mode (simulate without actual chaos)
        #[arg(short, long)]
        dry_run: bool,
        /// Verbose output
        #[arg(short, long)]
        verbose: bool,
        /// Configuration file path
        #[arg(short, long)]
        config: Option<String>,
        /// Rollback on failure
        #[arg(short, long)]
        rollback_on_failure: bool,
        /// Monitor system metrics during chaos
        #[arg(short, long)]
        monitor: bool,
    },
    /// Show chaos status
    Status,
    /// Stop all running chaos
    Stop,
    /// Show system metrics
    Metrics {
        /// Export metrics to file
        #[arg(short, long)]
        export: Option<String>,
    },
}

#[derive(Debug, Serialize, Deserialize)]
struct Config {
    safety: SafetyConfig,
    scenarios: HashMap<String, ScenarioConfig>,
}

#[derive(Debug, Serialize, Deserialize)]
struct SafetyConfig {
    max_duration: String,
    max_cpu_intensity: u8,
    max_memory_usage: String,
    allowed_interfaces: Vec<String>,
    protected_services: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct ScenarioConfig {
    default_duration: Option<String>,
    default_latency: Option<String>,
    default_intensity: Option<u8>,
    default_memory: Option<String>,
}

#[derive(Debug)]
struct ChaosState {
    running_chaos: Vec<ChaosSession>,
    config: Config,
}

#[derive(Debug, Clone)]
struct ChaosSession {
    id: String,
    scenario: String,
    start_time: Instant,
    duration: Duration,
    active: bool,
    rollback_fn: Option<Arc<dyn Fn() + Send + Sync>>, // Rollback function
}

static mut CHAOS_STATE: Option<Arc<Mutex<ChaosState>>> = None;

fn main() {
    let cli = Cli::parse();
    
    unsafe {
        if CHAOS_STATE.is_none() {
            CHAOS_STATE = Some(Arc::new(Mutex::new(ChaosState {
                running_chaos: Vec::new(),
                config: load_default_config(),
            })));
        }
    }

    match cli.command {
        Commands::ListScenarios => list_scenarios(),
        Commands::Run { .. } => run_chaos(),
        Commands::Status => show_status(),
        Commands::Stop => stop_chaos(),
        Commands::Metrics { .. } => show_metrics(),
    }
}

fn load_default_config() -> Config {
    Config {
        safety: SafetyConfig {
            max_duration: "300s".to_string(),
            max_cpu_intensity: 90,
            max_memory_usage: "8gb".to_string(),
            allowed_interfaces: vec!["eth0".to_string(), "wlan0".to_string()],
            protected_services: vec!["sshd".to_string(), "systemd".to_string()],
        },
        scenarios: HashMap::from([
            ("network-latency".to_string(), ScenarioConfig {
                default_duration: Some("60s".to_string()),
                default_latency: Some("50ms".to_string()),
                default_intensity: None,
                default_memory: None,
            }),
            ("cpu-spike".to_string(), ScenarioConfig {
                default_duration: Some("120s".to_string()),
                default_latency: None,
                default_intensity: Some(70),
                default_memory: None,
            }),
            ("memory-usage".to_string(), ScenarioConfig {
                default_duration: Some("300s".to_string()),
                default_latency: None,
                default_intensity: None,
                default_memory: Some("2gb".to_string()),
            }),
        ]),
    }
}

fn parse_duration(duration_str: &str) -> Result<Duration, String> {
    let duration_str = duration_str.to_lowercase();
    if duration_str.ends_with('s') {
        let secs = duration_str.trim_end_matches('s').parse::<u64>()
            .map_err(|_| format!("Invalid duration: {}", duration_str))?;
        Ok(Duration::from_secs(secs))
    } else if duration_str.ends_with('m') {
        let mins = duration_str.trim_end_matches('m').parse::<u64>()
            .map_err(|_| format!("Invalid duration: {}", duration_str))?;
        Ok(Duration::from_secs(mins * 60))
    } else if duration_str.ends_with('h') {
        let hours = duration_str.trim_end_matches('h').parse::<u64>()
            .map_err(|_| format!("Invalid duration: {}", duration_str))?;
        Ok(Duration::from_secs(hours * 3600))
    } else {
        Err(format!("Invalid duration format: {}", duration_str))
    }
}

fn parse_memory(memory_str: &str) -> Result<usize, String> {
    let memory_str = memory_str.to_lowercase();
    if memory_str.ends_with("gb") {
        let gb = memory_str.trim_end_matches("gb").parse::<usize>()
            .map_err(|_| format!("Invalid memory size: {}", memory_str))?;
        Ok(gb * 1024 * 1024 * 1024)
    } else if memory_str.ends_with("mb") {
        let mb = memory_str.trim_end_matches("mb").parse::<usize>()
            .map_err(|_| format!("Invalid memory size: {}", memory_str))?;
        Ok(mb * 1024 * 1024)
    } else if memory_str.ends_with("kb") {
        let kb = memory_str.trim_end_matches("kb").parse::<usize>()
            .map_err(|_| format!("Invalid memory size: {}", memory_str))?;
        Ok(kb * 1024)
    } else {
        Err(format!("Invalid memory format: {}", memory_str))
    }
}

fn parse_latency(latency_str: &str) -> Result<Duration, String> {
    let latency_str = latency_str.to_lowercase();
    if latency_str.ends_with("ms") {
        let ms = latency_str.trim_end_matches("ms").parse::<u64>()
            .map_err(|_| format!("Invalid latency: {}", latency_str))?;
        Ok(Duration::from_millis(ms))
    } else if latency_str.ends_with('s') {
        let secs = latency_str.trim_end_matches('s').parse::<u64>()
            .map_err(|_| format!("Invalid latency: {}", latency_str))?;
        Ok(Duration::from_secs(secs))
    } else {
        Err(format!("Invalid latency format: {}", latency_str))
    }
}

fn list_scenarios() {
    println!("Available chaos scenarios:");
    println!("  - network-latency: Add latency to network traffic");
    println!("  - network-loss: Introduce packet loss");
    println!("  - network-bandwidth: Limit network bandwidth");
    println!("  - cpu-spike: Spike CPU usage");
    println!("  - cpu-ramp: Gradually increase CPU usage");
    println!("  - memory-usage: Consume memory");
    println!("  - memory-ramp: Gradually increase memory usage");
    println!("  - service-restart: Restart a service");
    println!("  - service-stop: Stop a service temporarily");
    println!("  - time-shift: Shift system time");
    println!("  - time-jump: Random time jumps");
}

fn run_chaos() {
    // This would be implemented with proper argument parsing
    // For now, just show usage
    println!("Usage: chaos-chaos-chaos run --scenario <scenario> --duration <duration>");
    println!("Example: chaos-chaos-chaos run --scenario cpu-spike --duration 60s");
}

fn show_status() {
    println!("No chaos sessions running.");
}

fn stop_chaos() {
    println!("No chaos sessions to stop.");
}

fn show_metrics() {
    println!("System metrics:");
    println!("  CPU Usage: 45% (mock)");
    println!("  Memory Usage: 3.2GB / 16GB (mock)");
    println!("  Network: 100Mbps up / 50Mbps down (mock)");
    println!("  Load Average: 1.2 (mock)");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_duration_seconds() {
        let duration = parse_duration("30s").unwrap();
        assert_eq!(duration, Duration::from_secs(30));
    }

    #[test]
    fn test_parse_duration_minutes() {
        let duration = parse_duration("2m").unwrap();
        assert_eq!(duration, Duration::from_secs(120));
    }

    #[test]
    fn test_parse_duration_hours() {
        let duration = parse_duration("1h").unwrap();
        assert_eq!(duration, Duration::from_secs(3600));
    }

    #[test]
    fn test_parse_duration_invalid() {
        let result = parse_duration("30x");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_memory_gb() {
        let memory = parse_memory("2gb").unwrap();
        assert_eq!(memory, 2 * 1024 * 1024 * 1024);
    }

    #[test]
    fn test_parse_memory_mb() {
        let memory = parse_memory("512mb").unwrap();
        assert_eq!(memory, 512 * 1024 * 1024);
    }

    #[test]
    fn test_parse_memory_kb() {
        let memory = parse_memory("1024kb").unwrap();
        assert_eq!(memory, 1024 * 1024);
    }

    #[test]
    fn test_parse_memory_invalid() {
        let result = parse_memory("30x");
        assert!(result.is_err());
    }

    #[test]
    fn test_parse_latency_ms() {
        let latency = parse_latency("100ms").unwrap();
        assert_eq!(latency, Duration::from_millis(100));
    }

    #[test]
    fn test_parse_latency_seconds() {
        let latency = parse_latency("1s").unwrap();
        assert_eq!(latency, Duration::from_secs(1));
    }

    #[test]
    fn test_parse_latency_invalid() {
        let result = parse_latency("30x");
        assert!(result.is_err());
    }

    #[test]
    fn test_load_default_config() {
        let config = load_default_config();
        assert_eq!(config.safety.max_duration, "300s");
        assert_eq!(config.safety.max_cpu_intensity, 90);
        assert_eq!(config.safety.max_memory_usage, "8gb");
        assert!(config.scenarios.contains_key("network-latency"));
        assert!(config.scenarios.contains_key("cpu-spike"));
        assert!(config.scenarios.contains_key("memory-usage"));
    }
}
