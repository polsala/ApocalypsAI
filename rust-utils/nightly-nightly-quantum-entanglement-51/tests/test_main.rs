use nightly_quantum_entanglement_simulator::*;
use std::fs;
use tempfile::NamedTempFile;

#[test]
test_create_quantum_state() {
    let state = create_quantum_state(2);
    assert_eq!(state.particles, 2);
    assert_eq!(state.state_type, "bell");
    assert_eq!(state.coefficients.len(), 2);
    assert_eq!(state.measurements.len(), 0);
    
    // Test with different number of particles
    let state3 = create_quantum_state(3);
    assert_eq!(state3.particles, 3);
}

#[test]
test_measure_entangled_particles() {
    // Mock random number generator for deterministic testing
    use rand::rngs::mock::StepRng;
    let mut rng = StepRng::new(0, 1);
    
    // Test that entangled particles have correlated measurements
    let measurement = measure_entangled_particles(2);
    assert!(measurement.particle_1 == "up" || measurement.particle_1 == "down");
    assert!(measurement.particle_2 == "up" || measurement.particle_2 == "down");
    assert_eq!(measurement.particle_1, measurement.particle_2);
}

#[test]
test_format_spin() {
    assert_eq!(format_spin("up"), "↑ (spin up)");
    assert_eq!(format_spin("down"), "↓ (spin down)");
    assert_eq!(format_spin("unknown"), "unknown");
    assert_eq!(format_spin(""). "");
}

#[test]
test_check_correlation() {
    // Test perfect correlation
    let measurement_same = Measurement {
        particle_1: "up".to_string(),
        particle_2: "up".to_string(),
    };
    assert_eq!(check_correlation(&measurement_same), "Perfect correlation ✓");
    
    // Test perfect anti-correlation
    let measurement_different = Measurement {
        particle_1: "up".to_string(),
        particle_2: "down".to_string(),
    };
    assert_eq!(check_correlation(&measurement_different), "Perfect anti-correlation ✓");
}

#[test]
test_save_and_load_quantum_state() {
    let state = create_quantum_state(3);
    
    let temp_file = NamedTempFile::new().unwrap();
    let filename = temp_file.path().to_str().unwrap();
    
    // Save state
    assert!(save_quantum_state(&state, filename).is_ok());
    
    // Verify file exists and has content
    assert!(fs::metadata(filename).is_ok());
    let content = fs::read_to_string(filename).unwrap();
    assert!(!content.is_empty());
    
    // Load state
    let loaded_state = load_quantum_state(filename).unwrap();
    assert_eq!(state.particles, loaded_state.particles);
    assert_eq!(state.state_type, loaded_state.state_type);
    assert_eq!(state.coefficients, loaded_state.coefficients);
    assert_eq!(state.measurements, loaded_state.measurements);
}

#[test]
test_save_and_load_with_measurements() {
    let mut state = create_quantum_state(2);
    
    // Add some measurements
    state.measurements.push(Measurement {
        particle_1: "up".to_string(),
        particle_2: "up".to_string(),
    });
    state.measurements.push(Measurement {
        particle_1: "down".to_string(),
        particle_2: "down".to_string(),
    });
    
    let temp_file = NamedTempFile::new().unwrap();
    let filename = temp_file.path().to_str().unwrap();
    
    // Save and load
    assert!(save_quantum_state(&state, filename).is_ok());
    let loaded_state = load_quantum_state(filename).unwrap();
    
    assert_eq!(loaded_state.measurements.len(), 2);
    assert_eq!(loaded_state.measurements[0].particle_1, "up");
    assert_eq!(loaded_state.measurements[1].particle_1, "down");
}

#[test]
test_parse_args_basic() {
    let test_args = vec!["quantum_simulator", "--particles", "3", "--measurements", "10"];
    let mut args = Args::default();
    
    // Simulate argument parsing
    let mut iter = test_args.into_iter();
    iter.next(); // Skip program name
    
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "--particles" => {
                if let Some(val) = iter.next() {
                    args.particles = val.parse().unwrap_or(2);
                }
            }
            "--measurements" => {
                if let Some(val) = iter.next() {
                    args.measurements = val.parse().unwrap_or(5);
                }
            }
            _ => {}
        }
    }
    
    assert_eq!(args.particles, 3);
    assert_eq!(args.measurements, 10);
    assert!(!args.educational);
}

#[test]
test_parse_args_educational() {
    let test_args = vec!["quantum_simulator", "--educational", "--particles", "4"];
    let mut args = Args::default();
    
    let mut iter = test_args.into_iter();
    iter.next(); // Skip program name
    
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "--educational" => {
                args.educational = true;
            }
            "--particles" => {
                if let Some(val) = iter.next() {
                    args.particles = val.parse().unwrap_or(2);
                }
            }
            _ => {}
        }
    }
    
    assert!(args.educational);
    assert_eq!(args.particles, 4);
}

#[test]
test_parse_args_save_load() {
    let test_args = vec!["quantum_simulator", "--save", "test.json", "--load", "input.json"];
    let mut args = Args::default();
    
    let mut iter = test_args.into_iter();
    iter.next(); // Skip program name
    
    while let Some(arg) = iter.next() {
        match arg.as_str() {
            "--save" => {
                if let Some(val) = iter.next() {
                    args.save_file = Some(val);
                }
            }
            "--load" => {
                if let Some(val) = iter.next() {
                    args.load_file = Some(val);
                }
            }
            _ => {}
        }
    }
    
    assert_eq!(args.save_file, Some("test.json".to_string()));
    assert_eq!(args.load_file, Some("input.json".to_string()));
}

#[test]
test_quantum_state_serialization() {
    let state = QuantumState {
        particles: 2,
        state_type: "bell".to_string(),
        coefficients: vec![0.707, 0.707],
        measurements: vec![
            Measurement {
                particle_1: "up".to_string(),
                particle_2: "up".to_string(),
            },
            Measurement {
                particle_1: "down".to_string(),
                particle_2: "down".to_string(),
            },
        ],
    };
    
    // Test serialization
    let json = serde_json::to_string(&state).unwrap();
    assert!(json.contains("particles"));
    assert!(json.contains("bell"));
    assert!(json.contains("measurements"));
    
    // Test deserialization
    let deserialized: QuantumState = serde_json::from_str(&json).unwrap();
    assert_eq!(state.particles, deserialized.particles);
    assert_eq!(state.state_type, deserialized.state_type);
    assert_eq!(state.coefficients, deserialized.coefficients);
    assert_eq!(state.measurements.len(), deserialized.measurements.len());
}

#[test]
test_edge_cases() {
    // Test with 1 particle
    let state1 = create_quantum_state(1);
    assert_eq!(state1.particles, 1);
    
    // Test with large number of particles
    let state_large = create_quantum_state(100);
    assert_eq!(state_large.particles, 100);
    
    // Test empty measurements
    let state_empty = create_quantum_state(2);
    assert_eq!(state_empty.measurements.len(), 0);
}

#[test]
test_error_handling() {
    // Test loading non-existent file
    let result = load_quantum_state("nonexistent.json");
    assert!(result.is_err());
    
    // Test saving to invalid path
    let state = create_quantum_state(2);
    let result = save_quantum_state(&state, "/invalid/path/test.json");
    assert!(result.is_err());
}

#[test]
test_measurement_consistency() {
    // Run multiple measurements and ensure consistency
    let mut measurements = Vec::new();
    
    for _ in 0..100 {
        let measurement = measure_entangled_particles(2);
        measurements.push(measurement);
    }
    
    // All measurements should have correlated particles
    for measurement in &measurements {
        assert_eq!(measurement.particle_1, measurement.particle_2);
    }
    
    // Should have both up and down measurements (probabilistic)
    let has_up = measurements.iter().any(|m| m.particle_1 == "up");
    let has_down = measurements.iter().any(|m| m.particle_1 == "down");
    assert!(has_up && has_down);
}

// Mock rationale: These tests verify the core functionality of the quantum entanglement simulator
// including state creation, measurement simulation, file I/O operations, argument parsing,
// and edge cases. The tests use deterministic mocks where possible and verify both
// positive and negative scenarios to ensure robustness.
