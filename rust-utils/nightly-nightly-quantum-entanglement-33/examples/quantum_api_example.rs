use nightly_quantum_entanglement_checker::{QuantumAnalyzer, EntanglementConfig, OutputFormat, EntanglementState};
use std::error::Error;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Create a quantum analyzer
    let analyzer = QuantumAnalyzer::new();
    
    // Configure quantum analysis
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05, // 5% uncertainty (Heisenberg compensation)
        verbose: true,                // Show detailed quantum metrics
        output_format: OutputFormat::Text, // Human-readable output
    };
    
    println!("🌌 Initializing Quantum Entanglement Analysis...\n");
    
    // Example 1: Analyze two code snippets
    let code_snippet_1 = r#"
fn calculate_total(items: Vec<f64>) -> f64 {
    items.iter().sum()
}
"#;
    
    let code_snippet_2 = r#"
fn compute_sum(values: Vec<f64>) -> f64 {
    values.iter().sum()
}
"#;
    
    println!("🔬 Analyzing code snippets...");
    let result = analyzer
        .analyze_content(
            code_snippet_1,
            "snippet_1.rs",
            "snippet_2.rs",
            config.clone(),
        )
        .await?;
    
    print_analysis_result(&result);
    
    // Example 2: Analyze files from disk
    println!("\n📁 Analyzing files from disk...");
    
    // Create temporary files for demonstration
    std::fs::write("temp_file_1.rs", code_snippet_1)?;
    std::fs::write("temp_file_2.rs", code_snippet_2)?;
    
    let file_result = analyzer
        .analyze_files(
            "temp_file_1.rs",
            "temp_file_2.rs",
            config,
        )
        .await?;
    
    print_analysis_result(&file_result);
    
    // Example 3: Different uncertainty thresholds
    println!("\n🧪 Testing different uncertainty thresholds...");
    
    for uncertainty in [0.01, 0.1, 0.3, 0.5] {
        let config = EntanglementConfig {
            uncertainty_threshold: uncertainty,
            verbose: false,
            output_format: OutputFormat::Text,
        };
        
        let result = analyzer
            .analyze_content(
                code_snippet_1,
                "test_1.rs",
                "test_2.rs",
                config,
            )
            .await?;
        
        println!(
            "  Uncertainty {:.2}: {} (probability: {:.1}%)",
            uncertainty,
            match result.entanglement_state {
                EntanglementState::Entangled => "ENTANGLED",
                EntanglementState::Correlated => "CORRELATED",
                EntanglementState::Independent => "INDEPENDENT",
            },
            result.entanglement_probability * 100.0
        );
    }
    
    // Example 4: JSON output for machine processing
    println!("\n📊 Generating JSON report...");
    
    let json_config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: true,
        output_format: OutputFormat::Json,
    };
    
    let json_result = analyzer
        .analyze_content(
            code_snippet_1,
            "json_1.rs",
            "json_2.rs",
            json_config,
        )
        .await?;
    
    let json_output = serde_json::to_string_pretty(&json_result)?;
    println!("{}", json_output);
    
    // Cleanup temporary files
    std::fs::remove_file("temp_file_1.rs")?;
    std::fs::remove_file("temp_file_2.rs")?;
    
    println!("\n✨ Quantum analysis complete!");
    
    Ok(())
}

fn print_analysis_result(result: &nightly_quantum_entanglement_checker::EntanglementResult) {
    println!("\n🌌 Quantum Entanglement Analysis Results:");
    println!("  File 1: {}", result.file1_path);
    println!("  File 2: {}", result.file2_path);
    
    println!("\n🔮 Quantum State Analysis:");
    println!("  Hash similarity: {:.2}%", result.similarity * 100.0);
    println!("  Entanglement probability: {:.2}%", result.entanglement_probability * 100.0);
    println!("  Quantum coherence: {:.2}%", result.quantum_coherence * 100.0);
    println!("  Uncertainty threshold: {:.2}", result.config.uncertainty_threshold);
    
    println!("\n🔬 Quantum Signatures:");
    println!("  File 1 hash: {}", result.file1_hash);
    println!("  File 2 hash: {}", result.file2_hash);
    println!("  Hash distance: {:.6}", result.hash_distance);
    
    println!("\n✅ CONCLUSION:");
    match result.entanglement_state {
        EntanglementState::Entangled => {
            println!("  These files are QUANTUM ENTANGLED!");
            println!("  Spooky action detected at a distance.");
            println!("  Wave function collapse: DETERMINISTIC");
        }
        EntanglementState::Correlated => {
            println!("  These files show QUANTUM CORRELATION!");
            println!("  Similar wave functions detected.");
            println!("  Further observation recommended.");
        }
        EntanglementState::Independent => {
            println!("  These files are QUANTUM INDEPENDENT!");
            println!("  No spooky action detected.");
            println!("  Wave functions remain separate.");
        }
    }
}

// Additional utility functions for advanced usage

/// Batch analyze multiple file pairs
async fn batch_analyze_files(
    analyzer: &QuantumAnalyzer,
    file_pairs: Vec<(&str, &str)>,
    config: EntanglementConfig,
) -> Result<Vec<nightly_quantum_entanglement_checker::EntanglementResult>, Box<dyn std::error::Error>> {
    let mut results = Vec::new();
    
    for (file1, file2) in file_pairs {
        match analyzer.analyze_files(file1, file2, config.clone()).await {
            Ok(result) => results.push(result),
            Err(e) => {
                eprintln!("Error analyzing {} vs {}: {}", file1, file2, e);
            }
        }
    }
    
    Ok(results)
}

/// Find entangled files in a directory
async fn find_entangled_files(
    analyzer: &QuantumAnalyzer,
    directory: &str,
    threshold: f64,
) -> Result<Vec<(String, String)>, Box<dyn std::error::Error>> {
    use std::fs;
    
    let mut entangled_pairs = Vec::new();
    let config = EntanglementConfig {
        uncertainty_threshold: 0.05,
        verbose: false,
        output_format: OutputFormat::Text,
    };
    
    let entries: Vec<_> = fs::read_dir(directory)?
        .filter_map(|entry| entry.ok())
        .filter(|entry| entry.path().is_file())
        .collect();
    
    for i in 0..entries.len() {
        for j in (i + 1)..entries.len() {
            let file1 = entries[i].path();
            let file2 = entries[j].path();
            
            if let Ok(result) = analyzer
                .analyze_files(
                    file1.to_str().unwrap(),
                    file2.to_str().unwrap(),
                    config.clone(),
                )
                .await
            {
                if result.entanglement_probability > threshold {
                    entangled_pairs.push((
                        file1.to_string_lossy().to_string(),
                        file2.to_string_lossy().to_string(),
                    ));
                }
            }
        }
    }
    
    Ok(entangled_pairs)
}

/// Generate a quantum entanglement report
fn generate_quantum_report(
    results: &[nightly_quantum_entanglement_checker::EntanglementResult],
) -> String {
    let mut report = String::new();
    report.push_str("# Quantum Entanglement Analysis Report\n\n");
    
    let entangled_count = results.iter().filter(|r| {
        matches!(r.entanglement_state, EntanglementState::Entangled)
    }).count();
    let correlated_count = results.iter().filter(|r| {
        matches!(r.entanglement_state, EntanglementState::Correlated)
    }).count();
    let independent_count = results.iter().filter(|r| {
        matches!(r.entanglement_state, EntanglementState::Independent)
    }).count();
    
    report.push_str(&format!(
        "## Summary\n\n"
        "- Total comparisons: {}\n"
        "- Entangled pairs: {}\n"
        "- Correlated pairs: {}\n"
        "- Independent pairs: {}\n\n",
        results.len(),
        entangled_count,
        correlated_count,
        independent_count,
    ));
    
    report.push_str("## Detailed Results\n\n");
    
    for result in results {
        report.push_str(&format!(
            "### {} vs {}\n\n"
            "- **Entanglement State**: {:?}\n"
            "- **Similarity**: {:.2}%\n"
            "- **Probability**: {:.2}%\n"
            "- **Coherence**: {:.2}%\n\n",
            result.file1_path,
            result.file2_path,
            result.entanglement_state,
            result.similarity * 100.0,
            result.entanglement_probability * 100.0,
            result.quantum_coherence * 100.0,
        ));
    }
    
    report
}
