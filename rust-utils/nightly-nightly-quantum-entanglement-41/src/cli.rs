use std::env;
use std::process;

#[derive(Debug, Clone)]
pub struct CliArgs {
    pub node_a: String,
    pub node_b: String,
    pub decoherence: f64,
    pub measurements: usize,
    pub batch_mode: bool,
    pub verbose: bool,
}

impl Default for CliArgs {
    fn default() -> Self {
        Self {
            node_a: String::new(),
            node_b: String::new(),
            decoherence: 0.1,
            measurements: 100,
            batch_mode: false,
            verbose: false,
        }
    }
}

pub fn parse_args() -> CliArgs {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 1 {
        print_help();
        process::exit(0);
    }
    
    let mut cli_args = CliArgs::default();
    let mut i = 1;
    
    while i < args.len() {
        let arg = &args[i];
        
        match arg.as_str() {
            "--node-a" => {
                i += 1;
                if i >= args.len() {
                    eprintln!("Error: --node-a requires a value");
                    process::exit(1);
                }
                cli_args.node_a = args[i].clone();
            },
            "--node-b" => {
                i += 1;
                if i >= args.len() {
                    eprintln!("Error: --node-b requires a value");
                    process::exit(1);
                }
                cli_args.node_b = args[i].clone();
            },
            "--decoherence" => {
                i += 1;
                if i >= args.len() {
                    eprintln!("Error: --decoherence requires a value");
                    process::exit(1);
                }
                match args[i].parse::<f64>() {
                    Ok(value) if value >= 0.0 && value <= 1.0 => {
                        cli_args.decoherence = value;
                    },
                    _ => {
                        eprintln!("Error: --decoherence must be a number between 0.0 and 1.0");
                        process::exit(1);
                    }
                }
            },
            "--measurements" => {
                i += 1;
                if i >= args.len() {
                    eprintln!("Error: --measurements requires a value");
                    process::exit(1);
                }
                match args[i].parse::<usize>() {
                    Ok(value) if value > 0 => {
                        cli_args.measurements = value;
                    },
                    _ => {
                        eprintln!("Error: --measurements must be a positive integer");
                        process::exit(1);
                    }
                }
            },
            "--batch-mode" => {
                cli_args.batch_mode = true;
            },
            "--verbose" => {
                cli_args.verbose = true;
            },
            "--help" | "-h" => {
                print_help();
                process::exit(0);
            },
            _ => {
                eprintln!("Unknown option: {}", arg);
                print_help();
                process::exit(1);
            }
        }
        
        i += 1;
    }
    
    // Validate required arguments
    if cli_args.node_a.is_empty() || cli_args.node_b.is_empty() {
        eprintln!("Error: Both --node-a and --node-b are required");
        print_help();
        process::exit(1);
    }
    
    cli_args
}

fn print_help() {
    println!("Nightly Quantum Entanglement Checker");
    println!("====================================");
    println!("");
    println!("A whimsical CLI tool that simulates quantum entanglement verification for distributed systems.");
    println!("");
    println!("Usage:");
    println!("  nightly-quantum-entanglement-checker [OPTIONS]");
    println!("");
    println!("Options:");
    println!("  --node-a <NAME>      Name of the first quantum node (required)");
    println!("  --node-b <NAME>      Name of the second quantum node (required)");
    println!("  --decoherence <VAL>  Decoherence factor (0.0 to 1.0, default: 0.1)");
    println!("  --measurements <NUM> Number of quantum measurements (default: 100)");
    println!("  --batch-mode         Process multiple node pairs in sequence");
    println!("  --verbose            Show detailed quantum state information");
    println!("  --help, -h           Show this help message");
    println!("");
    println!("Examples:");
    println!("  # Basic entanglement check");
    println!("  nightly-quantum-entanglement-checker --node-a Alpha --node-b Beta");
    println!("");
    println!("  # Advanced usage with custom parameters");
    println!("  nightly-quantum-entanglement-checker \");
    println!("    --node-a Server-01 \");
    println!("    --node-b Server-02 \");
    println!("    --decoherence 0.15 \");
    println!("    --measurements 1000 \");
    println!("    --verbose");
    println!("");
    println!("  # Check entanglement across multiple node pairs");
    println!("  nightly-quantum-entanglement-checker \");
    println!("    --node-a Alpha --node-b Beta \");
    println!("    --node-a Gamma --node-b Delta \");
    println!("    --batch-mode");
}
