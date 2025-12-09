use nightly_quantum_entanglement_checker::quantum_simulator::*;
use std::fs;
use std::path::PathBuf;
use tempfile::TempDir;
use serde_json;

#[test]
fn test_scan_directory() {
    // Create a temporary directory with test files
    let temp_dir = TempDir::new().unwrap();
    let temp_path = temp_dir.path();
    
    // Create test files
    fs::write(temp_path.join("file1.txt"), "content1").unwrap();
    fs::write(temp_path.join("file2.txt"), "content2").unwrap();
    fs::create_dir(temp_path.join("subdir")).unwrap();
    fs::write(temp_path.join("subdir").join("file3.txt"), "content3").unwrap();
    
    // Scan directory
    let files = scan_directory(&temp_path.to_path_buf());
    
    // Should find 3 files (not the directory)
    assert_eq!(files.len(), 3);
    
    // Check that all files have valid paths
    for file in &files {
        assert!(file.path.contains("file"));
        assert!(file.last_modified > 0);
    }
}

#[test]
fn test_create_entanglements() {
    let files = vec![
        FileInfo {
            path: "file1.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        },
        FileInfo {
            path: "file2.txt".to_string(),
            last_modified: 2000,
            quantum_state: QuantumState::Normal,
        },
        FileInfo {
            path: "file3.txt".to_string(),
            last_modified: 3000,
            quantum_state: QuantumState::Normal,
        },
    ];
    
    let entanglements = create_entanglements(files, 2);
    
    // Should create 2 entanglement pairs
    assert_eq!(entanglements.len(), 2);
    
    // Each entanglement should have different files
    for entanglement in &entanglements {
        assert_ne!(entanglement.file_a, entanglement.file_b);
        assert!(entanglement.entanglement_level >= 0.1 && entanglement.entanglement_level <= 1.0);
    }
}

#[test]
fn test_analyze_quantum_states() {
    let files = vec![
        FileInfo {
            path: "file1.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        },
        FileInfo {
            path: "file2.txt".to_string(),
            last_modified: 2000,
            quantum_state: QuantumState::Normal,
        },
    ];
    
    let entanglements = vec![
        EntanglementPair {
            file_a: "file1.txt".to_string(),
            file_b: "file2.txt".to_string(),
            entanglement_level: 0.8,
        },
    ];
    
    let results = analyze_quantum_states(files, &entanglements);
    
    // Should have 2 results
    assert_eq!(results.len(), 2);
    
    // Check that entangled files are correctly identified
    for (file, state) in results {
        if file.path == "file1.txt" {
            assert!(matches!(state, QuantumState::Entangled(ref partner) if partner == "file2.txt"));
        } else if file.path == "file2.txt" {
            assert!(matches!(state, QuantumState::Entangled(ref partner) if partner == "file1.txt"));
        }
    }
}

#[test]
fn test_save_and_load_entanglements() {
    let temp_dir = TempDir::new().unwrap();
    let temp_path = temp_dir.path().join("test_entanglements.json");
    
    let entanglements = vec![
        EntanglementPair {
            file_a: "file1.txt".to_string(),
            file_b: "file2.txt".to_string(),
            entanglement_level: 0.8,
        },
        EntanglementPair {
            file_a: "file3.txt".to_string(),
            file_b: "file4.txt".to_string(),
            entanglement_level: 0.6,
        },
    ];
    
    // Save entanglements
    save_entanglements_to_file(&entanglements, temp_path.to_str().unwrap()).unwrap();
    
    // Load entanglements
    let loaded = load_entanglements_from_file(temp_path.to_str().unwrap()).unwrap();
    
    // Should have same number of entanglements
    assert_eq!(loaded.len(), 2);
    
    // Check that data is preserved
    assert_eq!(loaded[0].file_a, "file1.txt");
    assert_eq!(loaded[0].file_b, "file2.txt");
    assert_eq!(loaded[0].entanglement_level, 0.8);
    assert_eq!(loaded[1].file_a, "file3.txt");
    assert_eq!(loaded[1].file_b, "file4.txt");
    assert_eq!(loaded[1].entanglement_level, 0.6);
}

#[test]
fn test_generate_dashboard_data() {
    let files = vec![
        FileInfo {
            path: "file1.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Entangled("file2.txt".to_string()),
        },
        FileInfo {
            path: "file2.txt".to_string(),
            last_modified: 2000,
            quantum_state: QuantumState::Normal,
        },
    ];
    
    let entanglements = vec![
        EntanglementPair {
            file_a: "file1.txt".to_string(),
            file_b: "file2.txt".to_string(),
            entanglement_level: 0.8,
        },
    ];
    
    let dashboard_data = generate_dashboard_data(files, entanglements);
    
    // Should have files and entanglements keys
    assert!(dashboard_data.contains_key("files"));
    assert!(dashboard_data.contains_key("entanglements"));
    
    // Check files data
    let files_data = dashboard_data.get("files").unwrap().as_array().unwrap();
    assert_eq!(files_data.len(), 2);
    
    // Check entanglements data
    let entanglements_data = dashboard_data.get("entanglements").unwrap().as_array().unwrap();
    assert_eq!(entanglements_data.len(), 1);
}

#[test]
fn test_empty_directory_scan() {
    let temp_dir = TempDir::new().unwrap();
    let files = scan_directory(&temp_dir.path().to_path_buf());
    
    // Empty directory should return empty vector
    assert_eq!(files.len(), 0);
}

#[test]
fn test_insufficient_files_for_entanglement() {
    let files = vec![
        FileInfo {
            path: "single_file.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        },
    ];
    
    let entanglements = create_entanglements(files, 5);
    
    // Should not create any entanglements with only one file
    assert_eq!(entanglements.len(), 0);
}

#[test]
fn test_spooky_state_probability() {
    let files = vec![
        FileInfo {
            path: "file1.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        },
        FileInfo {
            path: "file2.txt".to_string(),
            last_modified: 2000,
            quantum_state: QuantumState::Normal,
        },
    ];
    
    let entanglements = Vec::new();
    
    // Test multiple times to check spooky state probability
    let mut spooky_count = 0;
    for _ in 0..100 {
        let results = analyze_quantum_states(files.clone(), &entanglements);
        for (_, state) in results {
            if matches!(state, QuantumState::Spooky) {
                spooky_count += 1;
                break;
            }
        }
    }
    
    // Should have some spooky states (with 10% probability, 100 trials should give some)
    // This is a probabilistic test, so it might occasionally fail
    assert!(spooky_count > 0, "Expected some spooky states to appear");
}
