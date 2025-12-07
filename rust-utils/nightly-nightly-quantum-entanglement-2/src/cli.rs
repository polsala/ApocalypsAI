use std::env;

/// Arguments structure for command-line options
#[derive(Debug)]
pub struct Args {
    /// List of nodes to check
    pub nodes: Vec<String>,
    /// Whether to run metrics monitoring
    pub metrics: bool,
    /// Monitoring interval in seconds
    pub interval: u64,
    /// Whether to run verification
    pub verify: bool,
    /// Entanglement threshold for verification
    pub threshold: f64,
}

/// Parse command-line arguments
pub fn parse_args() -> Args {
    let args: Vec<String> = env::args().collect();
    
    let mut parsed_args = Args {
        nodes: Vec::new(),
        metrics: false,
        interval: 5,
        verify: false,
        threshold: 0.8,
    };
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--nodes" => {
                i += 1;
                if i < args.len() {
                    parsed_args.nodes = args[i].split(',').map(|s| s.trim().to_string()).collect();
                }
            },
            "--metrics" => {
                parsed_args.metrics = true;
            },
            "--interval" => {
                i += 1;
                if i < args.len() {
                    if let Ok(interval) = args[i].parse::<u64>() {
                        parsed_args.interval = interval;
                    } else {
                        print_help();
                        std::process::exit(1);
                    }
                }
            },
            "--verify" => {
                parsed_args.verify = true;
            },
            "--threshold" => {
                i += 1;
                if i < args.len() {
                    if let Ok(threshold) = args[i].parse::<f64>() {
                        parsed_args.threshold = threshold.clamp(0.0, 1.0);
                    } else {
                        print_help();
                        std::process::exit(1);
                    }
                }
            },
            "--help" | "-h" => {
                print_help();
                std::process::exit(0);
            },
            _ => {
                eprintln!("Unknown option: {}", args[i]);
                print_help();
                std::process::exit(1);
            },
        }
        i += 1;
    }
    
    // If no specific mode is selected, default to entanglement check
    if !parsed_args.metrics && !parsed_args.verify {
        // If no nodes provided and not in metrics mode, show help
        if parsed_args.nodes.is_empty() {
            print_help();
            std::process::exit(1);
        }
    }
    
    parsed_args
}

/// Print help information
fn print_help() {
    println!("Quantum Entanglement Checker v1.0");
    println!("================================");
    println!();
    println!("Usage:");
    println!("  nightly-quantum-entanglement-checker [OPTIONS]");
    println!();
    println!("Options:");
    println!("  --nodes <NODES>      Comma-separated list of node names to check");
    println!("  --metrics            Generate quantum-inspired metrics");
    println!("  --interval <SECONDS>  Time interval in seconds for continuous monitoring (default: 5)");
    println!("  --verify             Verify synchronization with a threshold");
    println!("  --threshold <VALUE>   Entanglement threshold (0.0-1.0, default: 0.8)");
    println!("  --help, -h           Show this help message");
    println!();
    println!("Examples:");
    println!("  # Check entanglement between nodes");
    println!("  ./quantum-entanglement-checker --nodes node1,node2,node3");
    println!();
    println!("  # Generate quantum metrics");
    println!("  ./quantum-entanglement-checker --metrics --interval 5");
    println!();
    println!("  # Verify synchronization");
    println!("  ./quantum-entanglement-checker --verify --threshold 0.8");
    println!();
}
