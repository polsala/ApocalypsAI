use clap::{Arg, Command};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::io::{self, Write};

mod quantum;
mod report;

use quantum::{QuantumState, QuantumEntanglementChecker};
use report::{EntanglementReport, OutputFormat};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let matches = Command::new("Nightly Quantum Entanglement Checker")
        .version(env!("CARGO_PKG_VERSION"))
        .author("ApocalypsAI")
        .about("Simulates quantum entanglement verification for distributed systems")
        .arg(
            Arg::new("node-a")
                .short('a')
                .long("node-a")
                .value_name("NAME")
                .help("First node/service name")
                .required(false),
        )
        .arg(
            Arg::new("node-b")
                .short('b')
                .long("node-b")
                .value_name("NAME")
                .help("Second node/service name")
                .required(false),
        )
        .arg(
            Arg::new("report")
                .short('r')
                .long("report")
                .help("Generate quantum state report")
                .action(clap::ArgAction::SetTrue),
        )
        .arg(
            Arg::new("format")
                .short('f')
                .long("format")
                .value_name("FORMAT")
                .help("Output format (json, yaml, text)")
                .default_value("text"),
        )
        .arg(
            Arg::new("cluster")
                .short('c')
                .long("cluster")
                .value_name("FILE")
                .help("File containing cluster node list")
                .required(false),
        )
        .arg(
            Arg::new("threshold")
                .short('t')
                .long("threshold")
                .value_name("VALUE")
                .help("Entanglement threshold (0.0-1.0)")
                .default_value("0.8"),
        )
        .get_matches();

    let format = matches.get_one::<String>("format").unwrap();
    let output_format = OutputFormat::from_str(format)?;
    let threshold: f64 = matches.get_one::<String>("threshold").unwrap().parse()?;

    if matches.get_flag("report") {
        generate_entanglement_report(output_format, threshold)?;
    } else if let (Some(node_a), Some(node_b)) = (
        matches.get_one::<String>("node-a"),
        matches.get_one::<String>("node-b"),
    ) {
        check_entanglement(node_a, node_b, output_format, threshold)?;
    } else if let Some(cluster_file) = matches.get_one::<String>("cluster") {
        check_cluster_entanglement(cluster_file, output_format, threshold)?;
    } else {
        println!("Use --help for usage information");
    }

    Ok(())
}

fn check_entanglement(
    node_a: &str,
    node_b: &str,
    format: OutputFormat,
    threshold: f64,
) -> Result<(), Box<dyn std::error::Error>> {
    let checker = QuantumEntanglementChecker::new();
    let result = checker.verify_entanglement(node_a, node_b, threshold);

    let report = EntanglementReport {
        node_a: node_a.to_string(),
        node_b: node_b.to_string(),
        timestamp: chrono::Utc::now(),
        entanglement_verified: result.is_entangled,
        fidelity_score: result.fidelity,
        measurement_correlation: result.correlation,
        bell_state: result.bell_state,
        decoherence_risk: result.decoherence_risk,
        recommended_action: result.recommended_action,
    };

    print_report(report, format)?;
    Ok(())
}

fn generate_entanglement_report(
    format: OutputFormat,
    threshold: f64,
) -> Result<(), Box<dyn std::error::Error>> {
    let checker = QuantumEntanglementChecker::new();
    let nodes = vec!["service-a", "service-b", "service-c", "service-d"];

    let mut reports = Vec::new();
    for i in 0..nodes.len() {
        for j in (i + 1)..nodes.len() {
            let result = checker.verify_entanglement(nodes[i], nodes[j], threshold);
            reports.push(EntanglementReport {
                node_a: nodes[i].to_string(),
                node_b: nodes[j].to_string(),
                timestamp: chrono::Utc::now(),
                entanglement_verified: result.is_entangled,
                fidelity_score: result.fidelity,
                measurement_correlation: result.correlation,
                bell_state: result.bell_state,
                decoherence_risk: result.decoherence_risk,
                recommended_action: result.recommended_action,
            });
        }
    }

    print_cluster_report(reports, format)?;
    Ok(())
}

fn check_cluster_entanglement(
    cluster_file: &str,
    format: OutputFormat,
    threshold: f64,
) -> Result<(), Box<dyn std::error::Error>> {
    let content = fs::read_to_string(cluster_file)?;
    let nodes: Vec<String> = content
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| line.trim().to_string())
        .collect();

    if nodes.len() < 2 {
        return Err("Cluster file must contain at least 2 nodes".into());
    }

    let checker = QuantumEntanglementChecker::new();
    let mut reports = Vec::new();

    for i in 0..nodes.len() {
        for j in (i + 1)..nodes.len() {
            let result = checker.verify_entanglement(&nodes[i], &nodes[j], threshold);
            reports.push(EntanglementReport {
                node_a: nodes[i].clone(),
                node_b: nodes[j].clone(),
                timestamp: chrono::Utc::now(),
                entanglement_verified: result.is_entangled,
                fidelity_score: result.fidelity,
                measurement_correlation: result.correlation,
                bell_state: result.bell_state,
                decoherence_risk: result.decoherence_risk,
                recommended_action: result.recommended_action,
            });
        }
    }

    print_cluster_report(reports, format)?;
    Ok(())
}

fn print_report(
    report: EntanglementReport,
    format: OutputFormat,
) -> Result<(), Box<dyn std::error::Error>> {
    match format {
        OutputFormat::Text => {
            println!("🔬 Quantum Entanglement Verification Report");
            println!("==========================================");
            println!();
            println!("Node A: {}", report.node_a);
            println!("Node B: {}", report.node_b);
            println!();
            println!(
                "Entanglement Status: {}",
                if report.entanglement_verified {
                    "✅ VERIFIED"
                } else {
                    "❌ FAILED"
                }
            );
            println!("Bell State: {}", report.bell_state);
            println!("Fidelity Score: {:.3}", report.fidelity_score);
            println!("Measurement Correlation: {:.1}%", report.measurement_correlation * 100.0);
            println!();
            println!("Quantum Decoherence Risk: {}", report.decoherence_risk);
            println!("Recommended Action: {}", report.recommended_action);
        }
        OutputFormat::Json => {
            println!("{}", serde_json::to_string_pretty(&report)?);
        }
        OutputFormat::Yaml => {
            println!("{}", serde_yaml::to_string(&report)?);
        }
    }
    Ok(())
}

fn print_cluster_report(
    reports: Vec<EntanglementReport>,
    format: OutputFormat,
) -> Result<(), Box<dyn std::error::Error>> {
    match format {
        OutputFormat::Text => {
            println!("🔬 Quantum Cluster Entanglement Report");
            println!("=====================================");
            println!();
            
            let mut verified_count = 0;
            let total_count = reports.len();
            
            for report in &reports {
                println!(
                    "{} ↔ {} : {} (Fidelity: {:.3})",
                    report.node_a,
                    report.node_b,
                    if report.entanglement_verified { "✅" } else { "❌" },
                    report.fidelity_score
                );
                if report.entanglement_verified {
                    verified_count += 1;
                }
            }
            
            println!();
            println!(
                "Overall Entanglement Rate: {:.1}% ({}/{})",
                (verified_count as f64 / total_count as f64) * 100.0,
                verified_count,
                total_count
            );
        }
        OutputFormat::Json => {
            println!("{}", serde_json::to_string_pretty(&reports)?);
        }
        OutputFormat::Yaml => {
            println!("{}", serde_yaml::to_string(&reports)?);
        }
    }
    Ok(())
}
