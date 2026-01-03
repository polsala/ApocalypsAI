use clap::{Arg, Command};
use nightly_quantum_entanglement_checker::{
    benchmark::benchmark_entanglement,
    entanglement::EntanglementVerifier,
    format::{ExportFormat, ReportExporter},
    visualization::EntanglementVisualizer,
};
use std::process;

mod benchmark;
mod entanglement;
mod format;
mod visualization;

fn main() {
    let matches = Command::new("nightly-quantum-entanglement-checker")
        .version(env!("CARGO_PKG_VERSION"))
        .about("Simulates quantum entanglement verification for distributed systems")
        .subcommand(
            Command::new("verify")
                .about("Verifies quantum entanglement between components")
                .arg(
                    Arg::new("components")
                        .short('c')
                        .long("components")
                        .value_name("LIST")
                        .help("Comma-separated list of component names")
                        .required(true)
                )
                .arg(
                    Arg::new("strength")
                        .short('s')
                        .long("strength")
                        .value_name("FLOAT")
                        .help("Entanglement strength (0.0-1.0)")
                        .default_value("0.7")
                )
                .arg(
                    Arg::new("threshold")
                        .short('t')
                        .long("threshold")
                        .value_name("FLOAT")
                        .help("Coherence threshold (0.0-1.0)")
                        .default_value("0.9")
                )
        )
        .subcommand(
            Command::new("generate")
                .about("Generates entanglement reports")
                .arg(
                    Arg::new("components")
                        .short('c')
                        .long("components")
                        .value_name("LIST")
                        .help("Comma-separated list of component names")
                        .required(true)
                )
                .arg(
                    Arg::new("format")
                        .short('f')
                        .long("format")
                        .value_name("FORMAT")
                        .help("Output format (json, yaml, xml)")
                        .default_value("json")
                        .possible_values(["json", "yaml", "xml"])
                )
                .arg(
                    Arg::new("strength")
                        .short('s')
                        .long("strength")
                        .value_name("FLOAT")
                        .help("Entanglement strength (0.0-1.0)")
                        .default_value("0.7")
                )
        )
        .subcommand(
            Command::new("visualize")
                .about("Creates visual representations of entanglement networks")
                .arg(
                    Arg::new("components")
                        .short('c')
                        .long("components")
                        .value_name("LIST")
                        .help("Comma-separated list of component names")
                        .required(true)
                )
                .arg(
                    Arg::new("output")
                        .short('o')
                        .long("output")
                        .value_name("FILE")
                        .help("Output file path")
                        .default_value("entanglement.svg")
                )
        )
        .subcommand(
            Command::new("benchmark")
                .about("Benchmarks entanglement verification performance")
                .arg(
                    Arg::new("iterations")
                        .short('i')
                        .long("iterations")
                        .value_name("COUNT")
                        .help("Number of benchmark iterations")
                        .default_value("100")
                )
                .arg(
                    Arg::new("components")
                        .short('c')
                        .long("components")
                        .value_name("LIST")
                        .help("Comma-separated list of component names (auto-generated if not provided)")
                )
        )
        .get_matches();

    match matches.subcommand() {
        Some(("verify", sub_matches)) => {
            let components_str = sub_matches.get_one::<String>("components").unwrap();
            let components: Vec<String> = components_str
                .split(',')
                .map(|s| s.trim().to_string())
                .collect();
            
            let strength: f64 = sub_matches
                .get_one::<String>("strength")
                .unwrap()
                .parse()
                .expect("Invalid strength value");
            
            let threshold: f64 = sub_matches
                .get_one::<String>("threshold")
                .unwrap()
                .parse()
                .expect("Invalid threshold value");

            let verifier = EntanglementVerifier::new(components, strength, threshold);
            let result = verifier.verify_entanglement();
            
            println!("{}", serde_json::to_string_pretty(&result).unwrap());
        }
        Some(("generate", sub_matches)) => {
            let components_str = sub_matches.get_one::<String>("components").unwrap();
            let components: Vec<String> = components_str
                .split(',')
                .map(|s| s.trim().to_string())
                .collect();
            
            let format_str = sub_matches.get_one::<String>("format").unwrap();
            let format = match format_str.as_str() {
                "json" => ExportFormat::Json,
                "yaml" => ExportFormat::Yaml,
                "xml" => ExportFormat::Xml,
                _ => {
                    eprintln!("Invalid format: {}. Use json, yaml, or xml.", format_str);
                    process::exit(1);
                }
            };
            
            let strength: f64 = sub_matches
                .get_one::<String>("strength")
                .unwrap()
                .parse()
                .expect("Invalid strength value");

            let verifier = EntanglementVerifier::new(components, strength, 0.9);
            let result = verifier.verify_entanglement();
            
            let exporter = ReportExporter::new(format);
            match exporter.export(&result) {
                Ok(output) => println!("{}", output),
                Err(e) => {
                    eprintln!("Error exporting report: {}", e);
                    process::exit(1);
                }
            }
        }
        Some(("visualize", sub_matches)) => {
            let components_str = sub_matches.get_one::<String>("components").unwrap();
            let components: Vec<String> = components_str
                .split(',')
                .map(|s| s.trim().to_string())
                .collect();
            
            let output_path = sub_matches.get_one::<String>("output").unwrap();

            let verifier = EntanglementVerifier::new(components, 0.7, 0.9);
            let result = verifier.verify_entanglement();
            
            let visualizer = EntanglementVisualizer::new();
            match visualizer.visualize(&result, output_path) {
                Ok(_) => println!("Entanglement visualization saved to {}", output_path),
                Err(e) => {
                    eprintln!("Error creating visualization: {}", e);
                    process::exit(1);
                }
            }
        }
        Some(("benchmark", sub_matches)) => {
            let iterations: usize = sub_matches
                .get_one::<String>("iterations")
                .unwrap()
                .parse()
                .expect("Invalid iterations value");
            
            let components_opt = sub_matches.get_one::<String>("components");
            let components = if let Some(components_str) = components_opt {
                components_str
                    .split(',')
                    .map(|s| s.trim().to_string())
                    .collect()
            } else {
                // Auto-generate components for benchmarking
                (0..10)
                    .map(|i| format!("service-{}", i))
                    .collect()
            };

            let benchmark_result = benchmark_entanglement(components, iterations);
            println!("{}", serde_json::to_string_pretty(&benchmark_result).unwrap());
        }
        _ => {
            eprintln!("No subcommand provided. Use --help for usage information.");
            process::exit(1);
        }
    }
}
