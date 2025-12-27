use std::env;
use std::fs;
use std::path::Path;
use serde::{Deserialize, Serialize};
use clap::{Arg, Command};
use rand::Rng;
use chrono::{DateTime, Utc};

#[derive(Debug, Serialize, Deserialize)]
struct EntanglementReport {
    timestamp: DateTime<Utc>,
    node_a: String,
    node_b: String,
    verification_mode: String,
    correlation_coefficient: f64,
    entanglement_status: String,
    quantum_state: String,
    bell_inequality_violation: f64,
    measurement_precision: String,
    correlation_threshold: f64,
    quantum_correlations: Vec<f64>,
}

#[derive(Debug)]
struct QuantumChecker {
    node_a: String,
    node_b: String,
    verification_mode: VerificationMode,
    correlation_threshold: f64,
    measurement_precision: MeasurementPrecision,
    output_format: OutputFormat,
    save_report: Option<String>,
    verbose: bool,
}

#[derive(Debug, Clone)]
enum VerificationMode {
    Classical,
    Quantum,
}

#[derive(Debug, Clone)]
enum MeasurementPrecision {
    Low,
    Medium,
    High,
}

#[derive(Debug, Clone)]
enum OutputFormat {
    Text,
    Json,
    Yaml,
}

impl QuantumChecker {
    fn new(
        node_a: String,
        node_b: String,
        verification_mode: VerificationMode,
        correlation_threshold: f64,
        measurement_precision: MeasurementPrecision,
        output_format: OutputFormat,
        save_report: Option<String>,
        verbose: bool,
    ) -> Self {
        Self {
            node_a,
            node_b,
            verification_mode,
            correlation_threshold,
            measurement_precision,
            output_format,
            save_report,
            verbose,
        }
    }

    fn run(&self) -> Result<(), Box<dyn std::error::Error>> {
        let report = self.generate_entanglement_report();
        
        match &self.output_format {
            OutputFormat::Text => self.print_text_report(&report),
            OutputFormat::Json => self.print_json_report(&report)?,
            OutputFormat::Yaml => self.print_yaml_report(&report)?,
        }

        if let Some(path) = &self.save_report {
            self.save_report_to_file(&report, path)?;
        }

        Ok(())
    }

    fn generate_entanglement_report(&self) -> EntanglementReport {
        let mut rng = rand::thread_rng();
        
        // Generate quantum correlations based on precision
        let num_measurements = match self.measurement_precision {
            MeasurementPrecision::Low => 100,
            MeasurementPrecision::Medium => 1000,
            MeasurementPrecision::High => 10000,
        };

        let quantum_correlations: Vec<f64> = (0..num_measurements)
            .map(|_| {
                let base_correlation = match self.verification_mode {
                    VerificationMode::Classical => rng.gen_range(0.6..0.9),
                    VerificationMode::Quantum => rng.gen_range(0.85..0.99),
                };
                
                // Add quantum noise
                let noise = rng.gen_range(-0.05..0.05);
                (base_correlation + noise).max(0.0).min(1.0)
            })
            .collect();

        let avg_correlation = quantum_correlations.iter().sum::<f64>() / quantum_correlations.len() as f64;
        
        // Calculate Bell inequality violation
        let bell_violation = self.calculate_bell_violation(avg_correlation);
        
        // Determine entanglement status
        let entanglement_status = if avg_correlation >= self.correlation_threshold && bell_violation > 2.0 {
            "✅ VERIFIED".to_string()
        } else {
            "❌ NOT ENTANGLED".to_string()
        };

        // Generate quantum state notation
        let quantum_state = self.generate_quantum_state(avg_correlation);

        EntanglementReport {
            timestamp: Utc::now(),
            node_a: self.node_a.clone(),
            node_b: self.node_b.clone(),
            verification_mode: match self.verification_mode {
                VerificationMode::Classical => "Classical".to_string(),
                VerificationMode::Quantum => "Quantum".to_string(),
            },
            correlation_coefficient: avg_correlation,
            entanglement_status,
            quantum_state,
            bell_inequality_violation: bell_violation,
            measurement_precision: match self.measurement_precision {
                MeasurementPrecision::Low => "Low".to_string(),
                MeasurementPrecision::Medium => "Medium".to_string(),
                MeasurementPrecision::High => "High".to_string(),
            },
            correlation_threshold: self.correlation_threshold,
            quantum_correlations,
        }
    }

    fn calculate_bell_violation(&self, correlation: f64) -> f64 {
        // Simplified Bell inequality calculation
        // In real quantum mechanics, this would be more complex
        let base_violation = 2.0 + (correlation - 0.5) * 2.0;
        
        // Add quantum randomness
        let mut rng = rand::thread_rng();
        let randomness = rng.gen_range(-0.1..0.1);
        
        (base_violation + randomness).max(0.0).min(4.0)
    }

    fn generate_quantum_state(&self, correlation: f64) -> String {
        let alpha = (correlation * 0.7).sqrt();
        let beta = ((1.0 - correlation) * 0.7).sqrt();
        
        format!(
            "|ψ⟩ = {:.3}|00⟩ + {:.3}|11⟩",
            alpha,
            beta
        )
    }

    fn print_text_report(&self, report: &EntanglementReport) {
        println!("\n🔬 Quantum Entanglement Verification Report");
        println!("==========================================\n");

        println!("Node A: {}", report.node_a);
        println!("Node B: {}", report.node_b);
        println!("Verification Mode: {}", report.verification_mode);
        println!("Correlation Coefficient: {:.3}", report.correlation_coefficient);
        println!("Entanglement Status: {}", report.entanglement_status);
        println!("Quantum State: {}", report.quantum_state);
        println!("Bell Inequality Violation: {:.2} (S > 2 indicates quantum entanglement)", report.bell_inequality_violation);

        if self.verbose {
            println!("\n📊 Quantum Correlation Measurements:");
            for (i, &correlation) in report.quantum_correlations.iter().enumerate().take(10) {
                println!("  Measurement {}: {:.3}", i + 1, correlation);
            }
            if report.quantum_correlations.len() > 10 {
                println!("  ... and {} more measurements", report.quantum_correlations.len() - 10);
            }
        }

        if report.entanglement_status == "✅ VERIFIED" {
            println!("\n🎉 Nodes are quantumly entangled!");
        } else {
            println!("\n⚠️  Nodes are not sufficiently entangled.");
        }

        println!("\nTimestamp: {}", report.timestamp.format("%Y-%m-%d %H:%M:%S UTC"));
    }

    fn print_json_report(&self, report: &EntanglementReport) -> Result<(), Box<dyn std::error::Error>> {
        let json = serde_json::to_string_pretty(report)?;
        println!("{}", json);
        Ok(())
    }

    fn print_yaml_report(&self, report: &EntanglementReport) -> Result<(), Box<dyn std::error::Error>> {
        let yaml = serde_yaml::to_string(report)?;
        println!("{}", yaml);
        Ok(())
    }

    fn save_report_to_file(&self, report: &EntanglementReport, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let content = match &self.output_format {
            OutputFormat::Text => {
                let mut text = String::new();
                text.push_str(&format!("Quantum Entanglement Verification Report\n"));
                text.push_str(&format!("========================================\n\n"));
                text.push_str(&format!("Node A: {}\n", report.node_a));
                text.push_str(&format!("Node B: {}\n", report.node_b));
                text.push_str(&format!("Verification Mode: {}\n", report.verification_mode));
                text.push_str(&format!("Correlation Coefficient: {:.3}\n", report.correlation_coefficient));
                text.push_str(&format!("Entanglement Status: {}\n", report.entanglement_status));
                text.push_str(&format!("Quantum State: {}\n", report.quantum_state));
                text.push_str(&format!("Bell Inequality Violation: {:.2}\n", report.bell_inequality_violation));
                text.push_str(&format!("Measurement Precision: {}\n", report.measurement_precision));
                text.push_str(&format!("Correlation Threshold: {:.3}\n", report.correlation_threshold));
                text.push_str(&format!("Timestamp: {}\n", report.timestamp.format("%Y-%m-%d %H:%M:%S UTC")));
                text
            },
            OutputFormat::Json => serde_json::to_string_pretty(report)?,
            OutputFormat::Yaml => serde_yaml::to_string(report)?,
        };

        fs::write(path, content)?;
        println!("\n📄 Report saved to: {}", path);
        Ok(())
    }
}

fn parse_verification_mode(value: &str) -> Result<VerificationMode, String> {
    match value.to_lowercase().as_str() {
        "classical" => Ok(VerificationMode::Classical),
        "quantum" => Ok(VerificationMode::Quantum),
        _ => Err(format!("Invalid verification mode: {}. Must be 'classical' or 'quantum'.", value)),
    }
}

fn parse_measurement_precision(value: &str) -> Result<MeasurementPrecision, String> {
    match value.to_lowercase().as_str() {
        "low" => Ok(MeasurementPrecision::Low),
        "medium" => Ok(MeasurementPrecision::Medium),
        "high" => Ok(MeasurementPrecision::High),
        _ => Err(format!("Invalid precision level: {}. Must be 'low', 'medium', or 'high'.", value)),
    }
}

fn parse_output_format(value: &str) -> Result<OutputFormat, String> {
    match value.to_lowercase().as_str() {
        "text" => Ok(OutputFormat::Text),
        "json" => Ok(OutputFormat::Json),
        "yaml" => Ok(OutputFormat::Yaml),
        _ => Err(format!("Invalid output format: {}. Must be 'text', 'json', or 'yaml'.", value)),
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("nightly-quantum-entanglement-checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("A whimsical utility that simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("node-a")
                .short('a')
                .long("node-a")
                .value_name("NAME")
                .help("Name of the first quantum node")
                .required(true)
        )
        .arg(
            Arg::new("node-b")
                .short('b')
                .long("node-b")
                .value_name("NAME")
                .help("Name of the second quantum node")
                .required(true)
        )
        .arg(
            Arg::new("verification-mode")
                .long("verification-mode")
                .value_name("MODE")
                .help("Verification mode (classical|quantum)")
                .default_value("quantum")
                .value_parser(clap::value_parser!(String).range(1..))
        )
        .arg(
            Arg::new("correlation-threshold")
                .long("correlation-threshold")
                .value_name("VALUE")
                .help("Minimum correlation threshold (0.0-1.0)")
                .default_value("0.8")
                .value_parser(clap::value_parser!(f64).range(0.0..=1.0))
        )
        .arg(
            Arg::new("measurement-precision")
                .long("measurement-precision")
                .value_name("LEVEL")
                .help("Measurement precision (low|medium|high)")
                .default_value("medium")
                .value_parser(clap::value_parser!(String).range(1..))
        )
        .arg(
            Arg::new("output-format")
                .long("output-format")
                .value_name("FORMAT")
                .help("Output format (text|json|yaml)")
                .default_value("text")
                .value_parser(clap::value_parser!(String).range(1..))
        )
        .arg(
            Arg::new("save-report")
                .long("save-report")
                .value_name("FILE")
                .help("Save report to file")
        )
        .arg(
            Arg::new("verbose")
                .short('v')
                .long("verbose")
                .help("Enable verbose quantum state logging")
                .action(clap::ArgAction::SetTrue)
        )
        .get_matches();

    // Parse arguments
    let node_a = matches.get_one::<String>("node-a").unwrap().clone();
    let node_b = matches.get_one::<String>("node-b").unwrap().clone();
    
    let verification_mode = parse_verification_mode(matches.get_one::<String>("verification-mode").unwrap())?;
    let correlation_threshold = *matches.get_one::<f64>("correlation-threshold").unwrap();
    let measurement_precision = parse_measurement_precision(matches.get_one::<String>("measurement-precision").unwrap())?;
    let output_format = parse_output_format(matches.get_one::<String>("output-format").unwrap())?;
    
    let save_report = matches.get_one::<String>("save-report").cloned();
    let verbose = matches.get_flag("verbose");

    // Create and run quantum checker
    let checker = QuantumChecker::new(
        node_a,
        node_b,
        verification_mode,
        correlation_threshold,
        measurement_precision,
        output_format,
        save_report,
        verbose,
    );

    checker.run()?;
    Ok(())
}
