use std::process::Command;
use std::fs;
use tempfile::NamedTempFile;

#[test]
fn test_basic_entanglement_check() {
    // Test basic functionality with two nodes
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--nodes", "localhost:8080,localhost:8081",
            "--particle-type", "photon",
            "--algorithm", "bell-state",
            "--timeout", "5",
            "--verbose",
        ])
        .output()
        .expect("Failed to execute quantum checker");
    
    assert!(output.status.success());
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("🎉 All particles successfully entangled!"));
    assert!(stdout.contains("Fidelity:"));
    assert!(stdout.contains("Success Rate:"));
}

#[test]
fn test_config_file() {
    // Create a test configuration file
    let config_content = r#"
[network]
algorithm = "bell-state"
topology = "star"
timeout = 10
nodes = ["test1:8080", "test2:8080"]

[particles]
particle_type = "electron"

[output]
verbose = true
metrics = true
animations = true
"#;
    
    let mut config_file = NamedTempFile::new().unwrap();
    config_file.write_all(config_content.as_bytes()).unwrap();
    
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&[
            "--config", config_file.path().to_str().unwrap(),
        ])
        .output()
        .expect("Failed to execute quantum checker with config");
    
    assert!(output.status.success());
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("🎉 All particles successfully entangled!"));
}

#[test]
fn test_different_algorithms() {
    let algorithms = vec!["bell-state", "ghz-state", "w-state"];
    
    for algorithm in algorithms {
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(&[
                "--nodes", "localhost:8080",
                "--algorithm", algorithm,
                "--timeout", "3",
            ])
            .output()
            .expect(&format!("Failed to execute quantum checker with {}", algorithm));
        
        // Should complete (may succeed or fail, but shouldn't crash)
        assert!(output.status.success() || output.status.code() == Some(1));
    }
}

#[test]
fn test_different_particle_types() {
    let particle_types = vec!["photon", "electron", "neutron", "quark"];
    
    for particle_type in particle_types {
        let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
            .args(&[
                "--nodes", "localhost:8080",
                "--particle-type", particle_type,
                "--timeout", "3",
            ])
            .output()
            .expect(&format!("Failed to execute quantum checker with {}", particle_type));
        
        // Should complete (may succeed or fail, but shouldn't crash)
        assert!(output.status.success() || output.status.code() == Some(1));
    }
}

#[test]
fn test_help_output() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&["--help"])
        .output()
        .expect("Failed to execute quantum checker help");
    
    assert!(output.status.success());
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("nightly-quantum-entanglement-checker"));
    assert!(stdout.contains("quantum entanglement verification"));
    assert!(stdout.contains("--nodes"));
    assert!(stdout.contains("--particle-type"));
    assert!(stdout.contains("--algorithm"));
}

#[test]
fn test_version_output() {
    let output = Command::new(env!("CARGO_BIN_EXE_nightly-quantum-entanglement-checker"))
        .args(&["--version"])
        .output()
        .expect("Failed to execute quantum checker version");
    
    assert!(output.status.success());
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("nightly-quantum-entanglement-checker 1.0.0"));
}
