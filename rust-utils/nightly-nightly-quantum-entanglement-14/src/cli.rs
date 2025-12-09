use std::env;

#[derive(Debug)]
pub enum Command {
    Check {
        file1: String,
        file2: String,
        decoherence: f64,
    },
    Report {
        file1: String,
        file2: String,
        output: String,
    },
}

#[derive(Debug)]
pub struct Args {
    pub command: Command,
}

pub fn parse_args() -> Args {
    let args: Vec<String> = env::args().collect();
    
    if args.len() < 2 {
        print_help();
        std::process::exit(1);
    }
    
    let command = match args[1].as_str() {
        "check" => parse_check_command(&args),
        "report" => parse_report_command(&args),
        "--help" | "-h" => {
            print_help();
            std::process::exit(0);
        },
        _ => {
            eprintln!("Unknown command: {}", args[1]);
            print_help();
            std::process::exit(1);
        },
    };
    
    Args { command }
}

fn parse_check_command(args: &[String]) -> Command {
    if args.len() < 5 {
        eprintln!("Usage: {} check --file1 <file> --file2 <file> [--decoherence <factor>]", args[0]);
        std::process::exit(1);
    }
    
    let mut file1 = None;
    let mut file2 = None;
    let mut decoherence = 0.0;
    
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--file1" => {
                if i + 1 < args.len() {
                    file1 = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("--file1 requires a value");
                    std::process::exit(1);
                }
            },
            "--file2" => {
                if i + 1 < args.len() {
                    file2 = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("--file2 requires a value");
                    std::process::exit(1);
                }
            },
            "--decoherence" => {
                if i + 1 < args.len() {
                    match args[i + 1].parse::<f64>() {
                        Ok(val) => decoherence = val.clamp(0.0, 1.0),
                        Err(_) => {
                            eprintln!("--decoherence must be a number between 0.0 and 1.0");
                            std::process::exit(1);
                        },
                    }
                    i += 2;
                } else {
                    eprintln!("--decoherence requires a value");
                    std::process::exit(1);
                }
            },
            _ => {
                eprintln!("Unknown option: {}", args[i]);
                print_help();
                std::process::exit(1);
            },
        }
    }
    
    if file1.is_none() || file2.is_none() {
        eprintln!("Both --file1 and --file2 are required");
        print_help();
        std::process::exit(1);
    }
    
    Command::Check {
        file1: file1.unwrap(),
        file2: file2.unwrap(),
        decoherence,
    }
}

fn parse_report_command(args: &[String]) -> Command {
    if args.len() < 5 {
        eprintln!("Usage: {} report --file1 <file> --file2 <file> --output <file>", args[0]);
        std::process::exit(1);
    }
    
    let mut file1 = None;
    let mut file2 = None;
    let mut output = None;
    
    let mut i = 2;
    while i < args.len() {
        match args[i].as_str() {
            "--file1" => {
                if i + 1 < args.len() {
                    file1 = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("--file1 requires a value");
                    std::process::exit(1);
                }
            },
            "--file2" => {
                if i + 1 < args.len() {
                    file2 = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("--file2 requires a value");
                    std::process::exit(1);
                }
            },
            "--output" => {
                if i + 1 < args.len() {
                    output = Some(args[i + 1].clone());
                    i += 2;
                } else {
                    eprintln!("--output requires a value");
                    std::process::exit(1);
                }
            },
            _ => {
                eprintln!("Unknown option: {}", args[i]);
                print_help();
                std::process::exit(1);
            },
        }
    }
    
    if file1.is_none() || file2.is_none() || output.is_none() {
        eprintln!("--file1, --file2, and --output are all required");
        print_help();
        std::process::exit(1);
    }
    
    Command::Report {
        file1: file1.unwrap(),
        file2: file2.unwrap(),
        output: output.unwrap(),
    }
}

fn print_help() {
    println!("\n🔬 Nightly Quantum Entanglement Checker\n");
    println!("Usage:");
    println!("  {} check --file1 <file> --file2 <file> [--decoherence <factor>]");
    println!("  {} report --file1 <file> --file2 <file> --output <file>");
    println!("  {} --help\n", "cargo run --release --", "cargo run --release --", "cargo run --release --");
    
    println!("Commands:");
    println!("  check     Check if two files are quantumly entangled");
    println!("  report    Generate a detailed quantum entanglement report\n");
    
    println!("Options:");
    println!("  --file1 <file>        First file to compare");
    println!("  --file2 <file>        Second file to compare");
    println!("  --decoherence <f>   Decoherence factor (0.0-1.0, check command only)");
    println!("  --output <file>     Output file for JSON report (report command only)\n");
    
    println!("Examples:");
    println!("  {} check --file1 code1.rs --file2 code2.rs", "cargo run --release --");
    println!("  {} check --file1 code1.rs --file2 code2.rs --decoherence 0.1", "cargo run --release --");
    println!("  {} report --file1 code1.rs --file2 code2.rs --output report.json\n", "cargo run --release --");
}
