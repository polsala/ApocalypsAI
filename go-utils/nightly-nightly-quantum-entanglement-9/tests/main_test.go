package main

import (
	"testing"
	"time"
)

// TestParticleCreation tests that particles are created correctly
cfunc TestParticleCreation(t *testing.T) {
	particleCount := 10
	timeoutSeconds := 1
	verbose := false
	
	checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
	checker.GenerateParticles()
	
	// Verify correct number of particles
	if len(checker.particles) != particleCount*2 {
		t.Errorf("Expected %d particles, got %d", particleCount*2, len(checker.particles))
	}
	
	// Verify correct number of pairs
	if len(checker.pairs) != particleCount {
		t.Errorf("Expected %d pairs, got %d", particleCount, len(checker.pairs))
	}
}

// TestEntanglementVerification tests that entanglement verification works
cfunc TestEntanglementVerification(t *testing.T) {
	particleCount := 5
	timeoutSeconds := 2
	verbose := false
	
	checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
	checker.GenerateParticles()
	
	// Manually verify a few pairs to ensure logic is correct
	for pairID, particles := range checker.pairs {
		if len(particles) != 2 {
			t.Errorf("Pair %d has %d particles, expected 2", pairID, len(particles))
			continue
		}
		
		p1, p2 := particles[0], particles[1]
		
		// Check that spins are opposite (entangled)
		if !( (p1.Spin == "↑" && p2.Spin == "↓") || (p1.Spin == "↓" && p2.Spin == "↑") ) {
			t.Errorf("Pair %d particles not properly entangled: %s and %s", pairID, p1.Spin, p2.Spin)
		}
		
		// Break after checking first few pairs
		if pairID >= 2 {
			break
		}
	}
}

// TestTimeoutBehavior tests that timeout works correctly
cfunc TestTimeoutBehavior(t *testing.T) {
	particleCount := 100 // Large number to ensure timeout
	timeoutSeconds := 1 // Short timeout
	verbose := false
	
	checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
	checker.GenerateParticles()
	
	startTime := time.Now()
	checker.VerifyEntanglement()
	elapsed := time.Since(startTime)
	
	// Should timeout quickly
	if elapsed > time.Duration(timeoutSeconds+1)*time.Second {
		t.Errorf("Verification took too long: %v, expected ~%ds", elapsed, timeoutSeconds)
	}
}

// TestSmallParticleCount tests with minimal particle count
cfunc TestSmallParticleCount(t *testing.T) {
	particleCount := 1
	timeoutSeconds := 5
	verbose := true
	
	checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
	checker.GenerateParticles()
	
	if len(checker.particles) != 2 {
		t.Errorf("Expected 2 particles for count=1, got %d", len(checker.particles))
	}
	
	if len(checker.pairs) != 1 {
		t.Errorf("Expected 1 pair for count=1, got %d", len(checker.pairs))
	}
}

// TestLargeParticleCount tests with larger particle count
cfunc TestLargeParticleCount(t *testing.T) {
	particleCount := 1000
	timeoutSeconds := 10
	verbose := false
	
	checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
	checker.GenerateParticles()
	
	if len(checker.particles) != particleCount*2 {
		t.Errorf("Expected %d particles, got %d", particleCount*2, len(checker.particles))
	}
	
	if len(checker.pairs) != particleCount {
		t.Errorf("Expected %d pairs, got %d", particleCount, len(checker.pairs))
	}
}

// BenchmarkEntanglementVerification benchmarks the verification process
cfunc BenchmarkEntanglementVerification(b *testing.B) {
	for i := 0; i < b.N; i++ {
		particleCount := 100
		timeoutSeconds := 5
		verbose := false
		
		checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
		checker.GenerateParticles()
		checker.VerifyEntanglement()
	}
}

// TestParticleSpinDistribution tests that spins are properly distributed
cfunc TestParticleSpinDistribution(t *testing.T) {
	particleCount := 100
	timeoutSeconds := 1
	verbose := false
	
	checker := NewQuantumEntanglementChecker(particleCount, timeoutSeconds, verbose)
	checker.GenerateParticles()
	
	upCount := 0
	downCount := 0
	
	for _, particle := range checker.particles {
		if particle.Spin == "↑" {
			upCount++
		} else if particle.Spin == "↓" {
			downCount++
		}
	}
	
	// Should be roughly equal distribution
	total := upCount + downCount
	if total != len(checker.particles) {
		t.Errorf("Count mismatch: up=%d, down=%d, total=%d, expected=%d", 
			upCount, downCount, total, len(checker.particles))
	}
	
	// Allow some variance due to randomness
	if upCount < total*0.4 || upCount > total*0.6 {
		t.Errorf("Spin distribution seems biased: %d up, %d down out of %d total", 
			upCount, downCount, total)
	}
}
