use nightly_quantum_entanglement_checker::*;

#[test]
fn test_generate_entanglement_pair() {
    // Generate a pair and verify they have the same base ID
    let (particle_a, particle_b) = generate_entanglement_pair();
    
    // Both particles should have the same base ID
    let base_a = extract_base_id(&particle_a.id);
    let base_b = extract_base_id(&particle_b.id);
    assert_eq!(base_a, base_b);
    
    // Both should start with quantum prefix
    assert!(base_a.starts_with("Q-ENT"));
    
    // Coherence should be between 90% and 100%
    assert!(particle_a.coherence >= 90.0);
    assert!(particle_a.coherence <= 100.0);
    assert!(particle_b.coherence >= 90.0);
    assert!(particle_b.coherence <= 100.0);
}

#[test]
fn test_verify_entanglement_valid() {
    // Generate a valid pair
    let (particle_a, particle_b) = generate_entanglement_pair();
    
    // Verify they are entangled
    let result = verify_entanglement(&particle_a.id, &particle_b.id);
    assert!(result.is_some());
    
    let coherence = result.unwrap();
    assert!(coherence >= 90.0);
    assert!(coherence <= 100.0);
}

#[test]
fn test_verify_entanglement_invalid() {
    // Test with different base IDs
    let (particle_a, _) = generate_entanglement_pair();
    let (particle_c, _) = generate_entanglement_pair();
    
    // Extract different base IDs
    let base_a = extract_base_id(&particle_a.id);
    let base_c = extract_base_id(&particle_c.id);
    
    // Ensure they are different
    assert_ne!(base_a, base_c);
    
    // Verify they are NOT entangled
    let result = verify_entanglement(&particle_a.id, &particle_c.id);
    assert!(result.is_none());
}

#[test]
fn test_verify_entanglement_invalid_format() {
    // Test with invalid particle IDs
    let result = verify_entanglement("invalid-id", "another-invalid-id");
    assert!(result.is_none());
}

#[test]
fn test_extract_base_id() {
    // Test extracting base ID from particle ID
    let particle_id = "Q-ENT-123456-ABCD-7890";
    let base_id = extract_base_id(particle_id);
    assert_eq!(base_id, "Q-ENT-123456-ABCD");
    
    // Test with ID without timestamp
    let simple_id = "Q-ENT-123456-ABCD";
    let base_id_simple = extract_base_id(simple_id);
    assert_eq!(base_id_simple, "Q-ENT-123456-ABCD");
}

#[test]
fn test_calculate_coherence_deterministic() {
    // Same input should always produce same coherence
    let base_id = "Q-ENT-123456-ABCD";
    let timestamp = 1234567890;
    
    let coherence1 = calculate_coherence(base_id, timestamp);
    let coherence2 = calculate_coherence(base_id, timestamp);
    
    assert_eq!(coherence1, coherence2);
    assert!(coherence1 >= 90.0);
    assert!(coherence1 <= 100.0);
}

#[test]
fn test_calculate_checksum() {
    // Test checksum calculation
    let input = "123456";
    let checksum = calculate_checksum(input);
    
    // Checksum should be 4 hex characters
    assert_eq!(checksum.len(), 4);
    assert!(checksum.chars().all(|c| c.is_ascii_hexdigit()));
    
    // Same input should produce same checksum
    let checksum2 = calculate_checksum(input);
    assert_eq!(checksum, checksum2);
}

#[test]
fn test_generate_base_id_format() {
    // Generate base ID and verify format
    let base_id = generate_base_id();
    
    // Should start with quantum prefix
    assert!(base_id.starts_with("Q-ENT-"));
    
    // Should have 3 parts separated by dashes
    let parts: Vec<&str> = base_id.split('-').collect();
    assert_eq!(parts.len(), 3);
    
    // First part should be Q-ENT
    assert_eq!(parts[0], "Q-ENT");
    
    // Second part should be numeric
    assert!(parts[1].chars().all(|c| c.is_ascii_digit()));
    
    // Third part should be hex checksum
    assert!(parts[2].chars().all(|c| c.is_ascii_hexdigit()));
}

#[test]
fn test_whimsical_messages() {
    // Test that we get a whimsical message
    let message = get_whimsical_message();
    assert!(!message.is_empty());
    
    // Test multiple calls to ensure we get different messages over time
    let messages: Vec<String> = (0..10)
        .map(|_| get_whimsical_message().to_string())
        .collect();
    
    // Should have at least some variety (not all identical)
    let unique_messages: std::collections::HashSet<_> = messages.iter().collect();
    assert!(unique_messages.len() > 1 || messages.len() == 1);
}

#[test]
fn test_quantum_prefix_constant() {
    // Verify quantum prefix is correct
    assert_eq!(QUANTUM_PREFIX, "Q-ENT");
}

#[test]
fn test_coherence_range() {
    // Test coherence calculation across various inputs
    let test_inputs = [
        "Q-ENT-123456-ABCD",
        "Q-ENT-999999-FFFF",
        "Q-ENT-000000-0000",
        "Q-ENT-ABC123-DEAD",
    ];
    
    let timestamp = 1234567890;
    
    for input in test_inputs.iter() {
        let coherence = calculate_coherence(input, timestamp);
        assert!(coherence >= 90.0, "Coherence too low for {}: {}", input, coherence);
        assert!(coherence <= 100.0, "Coherence too high for {}: {}", input, coherence);
    }
}

#[test]
fn test_particle_creation() {
    // Test QuantumParticle creation
    let base_id = "Q-ENT-TEST-1234";
    let particle = QuantumParticle::new(base_id);
    
    // Verify particle has correct structure
    assert!(particle.id.starts_with(base_id));
    assert!(particle.timestamp > 0);
    assert!(particle.coherence >= 90.0);
    assert!(particle.coherence <= 100.0);
}

#[test]
fn test_entanglement_pair_consistency() {
    // Generate multiple pairs and verify each pair is internally consistent
    for _ in 0..10 {
        let (particle_a, particle_b) = generate_entanglement_pair();
        
        // Verify they can be verified as entangled
        let result = verify_entanglement(&particle_a.id, &particle_b.id);
        assert!(result.is_some(), "Generated pair should be verifiable");
        
        // Verify coherence is reasonable
        let coherence = result.unwrap();
        assert!(coherence >= 90.0);
        assert!(coherence <= 100.0);
    }
}

#[test]
fn test_mock_rationale() {
    // Mock rationale: Using deterministic algorithms to simulate quantum behavior
    // for testing purposes. Real quantum entanglement is non-deterministic, but
    // for a whimsical utility, deterministic behavior allows for reliable testing.
    
    let base_id = "Q-ENT-MOCK-TEST";
    let timestamp = 42;
    
    // Multiple calls with same parameters should yield same results
    let coherence1 = calculate_coherence(base_id, timestamp);
    let coherence2 = calculate_coherence(base_id, timestamp);
    let coherence3 = calculate_coherence(base_id, timestamp);
    
    assert_eq!(coherence1, coherence2);
    assert_eq!(coherence2, coherence3);
    
    // Should be in expected range
    assert!(coherence1 >= 90.0 && coherence1 <= 100.0);
}
