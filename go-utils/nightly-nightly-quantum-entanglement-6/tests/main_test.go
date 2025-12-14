package main

import (
	"context"
	"testing"
	"time"
)

func TestEntanglementChecker_GenerateEntangledPairs(t *testing.T) {
	checker := NewEntanglementChecker()
	defer checker.Stop()

	pairCount := 5
	checker.GenerateEntangledPairs(pairCount)

	checker.mu.RLock()
	particleCount := len(checker.particles)
	checker.mu.RUnlock()

	// Should have 2 particles per pair
	if particleCount != pairCount*2 {
		t.Errorf("Expected %d particles, got %d", pairCount*2, particleCount)
	}
}

func TestEntanglementChecker_MeasureParticle(t *testing.T) {
	checker := NewEntanglementChecker()
	defer checker.Stop()

	// Generate a single entangled pair
	checker.GenerateEntangledPairs(1)

	// Measure the first particle
	checker.mu.RLock()
	var particleID int
	for id := range checker.particles {
		particleID = id
		break
	}
	checker.mu.RUnlock()

	result, exists := checker.MeasureParticle(particleID)

	if !exists {
		t.Error("Particle should exist")
	}

	if result.ParticleID != particleID {
		t.Errorf("Expected particle ID %d, got %d", particleID, result.ParticleID)
	}
}

func TestEntanglementChecker_VerifyEntanglement(t *testing.T) {
	checker := NewEntanglementChecker()
	defer checker.Stop()

	// Generate entangled pairs
	pairCount := 10
	checker.GenerateEntangledPairs(pairCount)

	verified, broken, err := checker.VerifyEntanglement()

	if err != nil {
		t.Errorf("Verification failed: %v", err)
	}

	// All pairs should be verified since we just created them
	if verified != pairCount {
		t.Errorf("Expected %d verified pairs, got %d", pairCount, verified)
	}

	if broken != 0 {
		t.Errorf("Expected 0 broken pairs, got %d", broken)
	}
}

func TestDistributedConsensusNode_Vote(t *testing.T) {
	node1 := NewDistributedConsensusNode(1)
	defer node1.cancel()

	node2 := NewDistributedConsensusNode(2)
	defer node2.cancel()

	// Node 1 votes on Node 2
	node1.Vote(node2)

	// Check if vote was recorded
	consensusState, voteCount := node2.GetConsensusState()

	if voteCount != 1 {
		t.Errorf("Expected 1 vote, got %d", voteCount)
	}

	// The consensus state should match node1's state
	if consensusState != node1.State {
		t.Errorf("Expected consensus state %s, got %s", node1.State, consensusState)
	}
}

func TestDistributedConsensusNode_GetConsensusState(t *testing.T) {
	node := NewDistributedConsensusNode(1)
	defer node.cancel()

	// Add votes
	node.Votes[1] = StateUp
	node.Votes[2] = StateUp
	node.Votes[3] = StateDown

	consensusState, voteCount := node.GetConsensusState()

	// Should return StateUp since it has more votes
	if consensusState != StateUp {
		t.Errorf("Expected consensus state %s, got %s", StateUp, consensusState)
	}

	if voteCount != 2 {
		t.Errorf("Expected 2 votes for StateUp, got %d", voteCount)
	}
}

func TestEntanglementChecker_ConcurrentMeasurements(t *testing.T) {
	checker := NewEntanglementChecker()
	defer checker.Stop()

	// Generate entangled pairs
	pairCount := 10
	checker.GenerateEntangledPairs(pairCount)

	// Get all particle IDs
	particleIDs := make([]int, 0, pairCount*2)
	checker.mu.RLock()
	for id := range checker.particles {
		particleIDs = append(particleIDs, id)
	}
	checker.mu.RUnlock()

	// Start measurement process
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()

	measurementCount := 0
	checker.StartMeasurementProcess(particleIDs, 1*time.Second)
	checker.MonitorMeasurements()

	// Count measurements for 1 second
	for {
		select {
		case <-ctx.Done():
			goto done
		case <-checker.measurements:
			measurementCount++
		}
	}

done:
	// Should have made some measurements
	if measurementCount == 0 {
		t.Error("Expected at least one measurement")
	}
}

func TestDistributedConsensus_Stability(t *testing.T) {
	nodeCount := 5
	nodes := make([]*DistributedConsensusNode, nodeCount)

	for i := 0; i < nodeCount; i++ {
		nodes[i] = NewDistributedConsensusNode(i + 1)
		defer nodes[i].cancel()
	}

	// Run consensus process for a short duration
	ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel()

	for {
		select {
		case <-ctx.Done():
			goto done
		default:
			for i, node := range nodes {
				for j, target := range nodes {
					if i != j {
						node.Vote(target)
					}
				}
			}
			time.Sleep(10 * time.Millisecond)
		}
	}

done:

	// Check that all nodes have reached some consensus
	for _, node := range nodes {
		_, voteCount := node.GetConsensusState()
		if voteCount == 0 {
			t.Errorf("Node %d has no votes", node.ID)
		}
	}
}

func BenchmarkEntanglementChecker_GeneratePairs(b *testing.B) {
	for i := 0; i < b.N; i++ {
		checker := NewEntanglementChecker()
		checker.GenerateEntangledPairs(100)
		checker.Stop()
	}
}

func BenchmarkDistributedConsensusNode_Vote(b *testing.B) {
	node1 := NewDistributedConsensusNode(1)
	defer node1.cancel()

	node2 := NewDistributedConsensusNode(2)
	defer node2.cancel()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		node1.Vote(node2)
	}
}
