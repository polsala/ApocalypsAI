package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/signal"
	"sync"
	"time"
)

// QuantumState represents the state of a quantum particle
type QuantumState int

const (
	StateUp   QuantumState = 0
	StateDown QuantumState = 1
)

// String implements Stringer for QuantumState
func (s QuantumState) String() string {
	if s == StateUp {
		return "↑"
	}
	return "↓"
}

// Particle represents a quantum particle with entangled properties
type Particle struct {
	ID          int
	State       QuantumState
	EntangledID int
	CreatedAt   time.Time
}

// MeasurementResult represents the result of measuring a particle
type MeasurementResult struct {
	ParticleID int
	State      QuantumState
	Timestamp  time.Time
}

// EntanglementChecker manages quantum entanglement verification
type EntanglementChecker struct {
	particles   map[int]*Particle
	measurements chan MeasurementResult
	mu          sync.RWMutex
	ctx         context.Context
	cancel      context.CancelFunc
}

// NewEntanglementChecker creates a new entanglement checker
func NewEntanglementChecker() *EntanglementChecker {
	ctx, cancel := context.WithCancel(context.Background())
	return &EntanglementChecker{
		particles:   make(map[int]*Particle),
		measurements: make(chan MeasurementResult, 1000),
		ctx:         ctx,
		cancel:      cancel,
	}
}

// GenerateEntangledPairs creates pairs of entangled particles
func (ec *EntanglementChecker) GenerateEntangledPairs(count int) {
	ec.mu.Lock()
	defer ec.mu.Unlock()

	for i := 0; i < count; i++ {
		// Create entangled pair with opposite states
		particle1 := &Particle{
			ID:        i*2 + 1,
			State:     QuantumState(rand.Intn(2)),
			EntangledID: i*2 + 2,
			CreatedAt: time.Now(),
		}

		particle2 := &Particle{
			ID:        i*2 + 2,
			State:     1 - particle1.State, // Opposite state
			EntangledID: particle1.ID,
			CreatedAt: time.Now(),
		}

		ec.particles[particle1.ID] = particle1
		ec.particles[particle2.ID] = particle2
	}

	log.Printf("Generated %d entangled particle pairs", count)
}

// MeasureParticle measures a particle's state
func (ec *EntanglementChecker) MeasureParticle(particleID int) (MeasurementResult, bool) {
	ec.mu.RLock()
	particle, exists := ec.particles[particleID]
	ec.mu.RUnlock()

	if !exists {
		return MeasurementResult{}, false
	}

	// Simulate quantum measurement (collapse to definite state)
	result := MeasurementResult{
		ParticleID: particleID,
		State:      particle.State,
		Timestamp:  time.Now(),
	}

	// Send measurement to channel for verification
	select {
	case ec.measurements <- result:
	default:
		// Channel full, drop measurement
	}

	return result, true
}

// VerifyEntanglement checks if entangled particles maintain correlation
func (ec *EntanglementChecker) VerifyEntanglement() (int, int, error) {
	ec.mu.RLock()
	defer ec.mu.RUnlock()

	verified := 0
	broken := 0

	for _, particle := range ec.particles {
		entangled, exists := ec.particles[particle.EntangledID]
		if !exists {
			broken++
			continue
		}

		// Check if states are correlated (opposite for this simulation)
		if particle.State != entangled.State {
			verified++
		} else {
			broken++
		}
	}

	return verified, broken, nil
}

// StartMeasurementProcess starts concurrent measurement of particles
func (ec *EntanglementChecker) StartMeasurementProcess(particleIDs []int, duration time.Duration) {
	go func() {
		ticker := time.NewTicker(100 * time.Millisecond)
		defer ticker.Stop()

		for {
			select {
			case <-ec.ctx.Done():
				return
			case <-ticker.C:
				if len(particleIDs) == 0 {
					continue
				}
				// Randomly measure a particle
				randIndex := rand.Intn(len(particleIDs))
				ec.MeasureParticle(particleIDs[randIndex])
			}
		}
	}()
}

// MonitorMeasurements monitors measurement results
func (ec *EntanglementChecker) MonitorMeasurements() {
	go func() {
		for {
			select {
			case <-ec.ctx.Done():
				return
			case measurement := <-ec.measurements:
				log.Printf("Measured particle %d: state %s at %v",
					measurement.ParticleID, measurement.State, measurement.Timestamp.Format("15:04:05"))
			}
		}
	}()
}

// Stop gracefully stops the checker
func (ec *EntanglementChecker) Stop() {
	ec.cancel()
	close(ec.measurements)
}

// DistributedConsensusNode represents a node in a distributed consensus simulation
type DistributedConsensusNode struct {
	ID       int
	State    QuantumState
	Votes    map[int]QuantumState
	mu       sync.RWMutex
	ctx      context.Context
	cancel   context.CancelFunc
}

// NewDistributedConsensusNode creates a new consensus node
func NewDistributedConsensusNode(id int) *DistributedConsensusNode {
	ctx, cancel := context.WithCancel(context.Background())
	return &DistributedConsensusNode{
		ID:     id,
		State:  QuantumState(rand.Intn(2)),
		Votes:  make(map[int]QuantumState),
		ctx:    ctx,
		cancel: cancel,
	}
}

// Vote sends a vote to another node
func (n *DistributedConsensusNode) Vote(target *DistributedConsensusNode) {
	n.mu.RLock()
	state := n.State
	n.mu.RUnlock()

	select {
	case <-n.ctx.Done():
		return
	default:
		target.mu.Lock()
		target.Votes[n.ID] = state
		target.mu.Unlock()
	}
}

// GetConsensusState determines the consensus state based on votes
func (n *DistributedConsensusNode) GetConsensusState() (QuantumState, int) {
	n.mu.RLock()
	defer n.mu.RUnlock()

	upCount := 0
	downCount := 0

	for _, vote := range n.Votes {
		if vote == StateUp {
			upCount++
		} else {
			downCount++
		}
	}

	if upCount > downCount {
		return StateUp, upCount
	}
	return StateDown, downCount
}

// StartConsensusProcess starts the consensus voting process
func StartConsensusProcess(nodes []*DistributedConsensusNode, duration time.Duration) {
	ctx, cancel := context.WithTimeout(context.Background(), duration)
	defer cancel()

	for {
		select {
		case <-ctx.Done():
			return
		default:
			for i, node := range nodes {
				for j, target := range nodes {
					if i != j {
						node.Vote(target)
					}
				}
				time.Sleep(100 * time.Millisecond)
			}
		}
	}
}

func main() {
	// Parse command line flags
	particleCount := flag.Int("particles", 10, "number of entangled particle pairs to generate")
	duration := flag.Duration("duration", 10*time.Second, "duration of the measurement process")
	consensus := flag.Bool("consensus", false, "run distributed consensus simulation")
	nodeCount := flag.Int("nodes", 5, "number of nodes for consensus simulation")

	flag.Parse()

	// Seed random number generator
	rand.Seed(time.Now().UnixNano())

	if *consensus {
		// Run distributed consensus simulation
		log.Println("Starting distributed consensus simulation...")

		nodes := make([]*DistributedConsensusNode, *nodeCount)
		for i := 0; i < *nodeCount; i++ {
			nodes[i] = NewDistributedConsensusNode(i + 1)
		}

		StartConsensusProcess(nodes, *duration)

		// Print final consensus states
		for _, node := range nodes {
			consensusState, voteCount := node.GetConsensusState()
			log.Printf("Node %d consensus: %s (votes: %d)", node.ID, consensusState, voteCount)
		}

		return
	}

	// Run quantum entanglement simulation
	log.Println("Starting quantum entanglement simulation...")

	checker := NewEntanglementChecker()
	defer checker.Stop()

	// Generate entangled particles
	checker.GenerateEntangledPairs(*particleCount)

	// Get all particle IDs
	particleIDs := make([]int, 0, *particleCount*2)
	checker.mu.RLock()
	for id := range checker.particles {
		particleIDs = append(particleIDs, id)
	}
	checker.mu.RUnlock()

	// Start measurement process
	checker.StartMeasurementProcess(particleIDs, *duration)
	checker.MonitorMeasurements()

	// Wait for duration
	time.Sleep(*duration)

	// Verify entanglement
	verified, broken, err := checker.VerifyEntanglement()
	if err != nil {
		log.Fatalf("Failed to verify entanglement: %v", err)
	}

	log.Printf("Entanglement verification complete:")
	log.Printf("  Verified pairs: %d", verified)
	log.Printf("  Broken pairs: %d", broken)
	log.Printf("  Success rate: %.2f%%", float64(verified)/float64(verified+broken)*100)

	// Handle graceful shutdown
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt)
	<-c
	log.Println("Shutting down...")
}
