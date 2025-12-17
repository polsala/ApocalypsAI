use clap::{Arg, Command};
use nightly_quantum_entanglement_checker::{QuantumAnalyzer, OutputFormat, EntanglementConfig};
use std::io::{self, Read};
use std::path::Path;
use std::process;

#[tokio::main]
async fn main() {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI Collective")
        .about("Checks if two code snippets are quantum entangled with probabilistic twist")
        .arg(
            Arg::new("file1")
                .short('1')
                .long("file1")
                .value_name("FILE1")
                .help("First file to compare")
                .required_unless("stdin")
                .conflicts_with("stdin")
        )
        .arg(
            Arg::new("file2")
                .short('2')
                .long("file2")
                .value_name("FILE2")
                .help("Second file to compare")
                .required(true)
        )
        .arg(
            Arg::new("stdin")
                .short('s')
                .long("stdin")
                .help("Read first file from stdin")
                .required_unless("file1")
        )
        .arg(
            Arg::new("uncertainty")
                .short('u')
                .long("uncertainty")
                .value_name("UNCERTAINTY")
                .help("Quantum uncertainty threshold")
                .default_value("0.05")
                .validator(validate_uncertainty)
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose quantum state reporting")
                .action(clap::ArgAction::SetTrue)
        )
        .arg(
            Arg::new("format")
                .short('f')
                .long("format")
                .value_name("FORMAT")
                .help("Output format")
                .value_parser(["text", "json"])
                .default_value("text")
        )
        .get_matches();

    // Parse arguments
    let uncertainty: f64 = matches
        .get_one::<String>("uncertainty")
        .unwrap()
        .parse()
        .expect("Invalid uncertainty value");

    let verbose = matches.get_flag("verbose");
    let format = match matches.get_one::<String>("format").unwrap().as_str() {
        "json" => OutputFormat::Json,
        _ => OutputFormat::Text,
    };

    // Create analyzer
    let analyzer = QuantumAnalyzer::new();
    let config = EntanglementConfig {
        uncertainty_threshold: uncertainty,
        verbose,
        output_format: format,
    };

    // Get file contents
    let file1_content = if matches.get_flag("stdin") {
        read_stdin().await
    } else {
        let file1_path = matches.get_one::<String>("file1").unwrap();
        analyzer.read_file(file1_path).await.unwrap_or_else(|e| {
            eprintln!("Error reading file1 '{}': {}", file1_path, e);
            process::exit(1);
        })
    };

    let file2_path = matches.get_one::<String>("file2").unwrap();
    let file2_content = analyzer.read_file(file2_path).await.unwrap_or_else(|e| {
        eprintln!("Error reading file2 '{}': {}", file2_path, e);
        process::exit(1);
    });

    // Analyze entanglement
    match analyzer
        .analyze_content(&file1_content, file2_path, &file2_content, config)
        .await
    {
        Ok(result) => {
            match format {
                OutputFormat::Json => {
                    println!("{}", serde_json::to_string_pretty(&result).unwrap());
                }
                OutputFormat::Text => {
                    print_quantum_report(&result);
                }
            }
        }
        Err(e) => {
            eprintln!("Quantum analysis failed: {}", e);
            process::exit(1);
        }
    }
}

fn validate_uncertainty(val: &str) -> Result<(), String> {
    match val.parse::<f64>() {
        Ok(n) if n >= 0.0 && n <= 1.0 => Ok(()),
        Ok(_) => Err("Uncertainty must be between 0.0 and 1.0".to_string()),
        Err(_) => Err("Uncertainty must be a valid number".to_string()),
    }
}

async fn read_stdin() -> String {
    let mut buffer = String::new();
    io::stdin()
        .read_to_string(&mut buffer)
        .expect("Failed to read from stdin");
    buffer
}

fn print_quantum_report(result: &nightly_quantum_entanglement_checker::EntanglementResult) {
    println!("🌌 Quantum Entanglement Analysis 🌌\n");
    println!("File 1: {}", result.file1_path);
    println!("File 2: {}\n", result.file2_path);

    println!("🔮 Quantum State Analysis:");
    println!("- Hash similarity: {:.2}%", result.similarity * 100.0);
    println!("- Entanglement probability: {:.2}%", result.entanglement_probability * 100.0);
    println!("- Uncertainty threshold: {:.2}\n", result.config.uncertainty_threshold);

    match result.entanglement_state {
        nightly_quantum_entanglement_checker::EntanglementState::Entangled => {
            println!("✅ CONCLUSION: These files are QUANTUM ENTANGLED!");
            println!("   Spooky action detected at a distance.");
            println!("   Wave function collapse: DETERMINISTIC");
        }
        nightly_quantum_entanglement_checker::EntanglementState::Correlated => {
            println!("⚠️  CONCLUSION: These files show QUANTUM CORRELATION!");
            println!("   Similar wave functions detected.");
            println!("   Further observation recommended.");
        }
        nightly_quantum_entanglement_checker::EntanglementState::Independent => {
            println!("❌ CONCLUSION: These files are QUANTUM INDEPENDENT!");
            println!("   No spooky action detected.");
            println!("   Wave functions remain separate.");
        }
    }

    if result.config.verbose {
        println!("\n🔬 Detailed Quantum Metrics:");
        println!("- File 1 hash: {}", result.file1_hash);
        println!("- File 2 hash: {}", result.file2_hash);
        println!("- Hash distance: {:.6}", result.hash_distance);
        println!("- Quantum coherence: {:.2}%", result.quantum_coherence * 100.0);
    }

    if result.config.output_format == OutputFormat::Text {
        println!("\n✨ Quantum analysis complete!");
    }
}
