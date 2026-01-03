use nightly_quantum_entanglement_checker::{
    entanglement::EntanglementVerifier,
    format::{ExportFormat, ReportExporter},
    visualization::EntanglementVisualizer,
};

fn main() {
    println!("=== Nightly Quantum Entanglement Checker Examples ===\n");

    // Example 1: Basic entanglement verification
    println!("1. Basic Entanglement Verification");
    let components = vec![
        "user-service".to_string(),
        "order-service".to_string(),
        "payment-service".to_string(),
    ];
    
    let verifier = EntanglementVerifier::new(components, 0.8, 0.9);
    let verification = verifier.verify_entanglement();
    
    println!("Components: {:?}", verification.components);
    println!("Coherence Score: {:.2}", verification.coherence_score);
    println!("Status: {:?}", verification.verification_status);
    println!("Verification Time: {:.2}ms\n", verification.verification_time_ms);

    // Example 2: Export to different formats
    println!("2. Export to Different Formats");
    
    let exporter_json = ReportExporter::new(ExportFormat::Json);
    let json_output = exporter_json.export(&verification).unwrap();
    println!("JSON Output:\n{}\n", json_output);
    
    let exporter_yaml = ReportExporter::new(ExportFormat::Yaml);
    let yaml_output = exporter_yaml.export(&verification).unwrap();
    println!("YAML Output:\n{}\n", yaml_output);
    
    let exporter_xml = ReportExporter::new(ExportFormat::Xml);
    let xml_output = exporter_xml.export(&verification).unwrap();
    println!("XML Output:\n{}\n", xml_output);

    // Example 3: Generate visualization
    println!("3. Generate Visualization");
    let visualizer = EntanglementVisualizer::new();
    
    // Generate ASCII art
    let ascii_art = visualizer.generate_ascii_art(&verification);
    println!("{}", ascii_art);
    
    // Generate SVG (would normally save to file)
    let svg_content = visualizer.generate_svg(&verification);
    println!("SVG generated ({} characters)", svg_content.len());
    println!("SVG preview: {}\n", &svg_content[..100]);

    // Example 4: Component metrics
    println!("4. Component Metrics");
    let metrics = verifier.get_component_metrics();
    
    for (component, metric) in &metrics {
        println!("Component: {}", component);
        println!("  Entanglements: {}", metric.entanglement_count);
        println!("  Avg Strength: {:.2}", metric.average_strength);
        println!("  Max Strength: {:.2}", metric.max_strength);
        println!("  Min Strength: {:.2}\n", metric.min_strength);
    }

    // Example 5: Performance benchmarking
    println!("5. Performance Benchmarking");
    let benchmark_components = vec![
        "service-a".to_string(),
        "service-b".to_string(),
        "service-c".to_string(),
        "service-d".to_string(),
        "service-e".to_string(),
    ];
    
    let benchmark_result = nightly_quantum_entanglement_checker::benchmark::benchmark_entanglement(
        benchmark_components,
        100
    );
    
    println!("Benchmark Results:");
    println!("  Iterations: {}", benchmark_result.iterations);
    println!("  Total Time: {:.2}ms", benchmark_result.total_time_ms);
    println!("  Average Time: {:.2}ms", benchmark_result.average_time_ms);
    println!("  Throughput: {:.2} ops/sec", benchmark_result.throughput_ops_per_sec);
    println!("  Components per verification: {}\n", benchmark_result.components_per_verification);

    println!("=== Examples Complete ===");
}
