use nightly_quantum_entanglement_checker::quantum_simulator::*;
use std::collections::HashMap;

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_file_info_creation() {
        let file_info = FileInfo {
            path: "test.txt".to_string(),
            last_modified: 1234567890,
            quantum_state: QuantumState::Normal,
        };
        
        assert_eq!(file_info.path, "test.txt");
        assert_eq!(file_info.last_modified, 1234567890);
        assert!(matches!(file_info.quantum_state, QuantumState::Normal));
    }
    
    #[test]
    fn test_entanglement_pair_creation() {
        let entanglement = EntanglementPair {
            file_a: "file1.txt".to_string(),
            file_b: "file2.txt".to_string(),
            entanglement_level: 0.75,
        };
        
        assert_eq!(entanglement.file_a, "file1.txt");
        assert_eq!(entanglement.file_b, "file2.txt");
        assert_eq!(entanglement.entanglement_level, 0.75);
    }
    
    #[test]
    fn test_quantum_state_variants() {
        let entangled = QuantumState::Entangled("partner.txt".to_string());
        let spooky = QuantumState::Spooky;
        let normal = QuantumState::Normal;
        
        assert!(matches!(entangled, QuantumState::Entangled(_)));
        assert!(matches!(spooky, QuantumState::Spooky));
        assert!(matches!(normal, QuantumState::Normal));
    }
    
    #[test]
    fn test_determine_quantum_state_entangled() {
        let file = FileInfo {
            path: "file1.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        };
        
        let entanglements = vec![
            EntanglementPair {
                file_a: "file1.txt".to_string(),
                file_b: "file2.txt".to_string(),
                entanglement_level: 0.8,
            },
        ];
        
        let state = determine_quantum_state(&file, &entanglements);
        assert!(matches!(state, QuantumState::Entangled(ref partner) if partner == "file2.txt"));
    }
    
    #[test]
    fn test_determine_quantum_state_spooky() {
        let file = FileInfo {
            path: "file3.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        };
        
        let entanglements = Vec::new();
        
        // This test is probabilistic, so we'll run it multiple times
        let mut found_spooky = false;
        for _ in 0..100 {
            let state = determine_quantum_state(&file, &entanglements);
            if matches!(state, QuantumState::Spooky) {
                found_spooky = true;
                break;
            }
        }
        
        // Should find spooky state at least once in 100 tries
        assert!(found_spooky, "Expected to find spooky state at least once");
    }
    
    #[test]
    fn test_determine_quantum_state_normal() {
        let file = FileInfo {
            path: "file4.txt".to_string(),
            last_modified: 1000,
            quantum_state: QuantumState::Normal,
        };
        
        let entanglements = Vec::new();
        
        // Test many times to ensure we can get normal state
        let mut found_normal = false;
        for _ in 0..1000 {
            let state = determine_quantum_state(&file, &entanglements);
            if matches!(state, QuantumState::Normal) {
                found_normal = true;
                break;
            }
        }
        
        assert!(found_normal, "Expected to find normal state");
    }
    
    #[test]
    fn test_dashboard_data_structure() {
        let files = vec![
            FileInfo {
                path: "test1.txt".to_string(),
                last_modified: 1000,
                quantum_state: QuantumState::Normal,
            },
        ];
        
        let entanglements = vec![
            EntanglementPair {
                file_a: "test1.txt".to_string(),
                file_b: "test2.txt".to_string(),
                entanglement_level: 0.5,
            },
        ];
        
        let dashboard_data = generate_dashboard_data(files, entanglements);
        
        // Check that we have the expected structure
        assert_eq!(dashboard_data.len(), 2);
        assert!(dashboard_data.contains_key("files"));
        assert!(dashboard_data.contains_key("entanglements"));
        
        // Check that files data is an array
        let files_value = dashboard_data.get("files").unwrap();
        assert!(files_value.is_array());
        
        // Check that entanglements data is an array
        let entanglements_value = dashboard_data.get("entanglements").unwrap();
        assert!(entanglements_value.is_array());
    }
}
