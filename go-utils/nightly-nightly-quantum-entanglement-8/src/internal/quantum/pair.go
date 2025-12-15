package quantum

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"time"
)

// QuantumState represents the state of a quantum particle
type QuantumState int

const (
	QuantumStateSuperposition QuantumState = iota
	QuantumStateCollapsed
	QuantumStateDecohered
)

func (qs QuantumState) String() string {
	switch qs {
	case QuantumStateSuperposition:
		return "superposition"
	case QuantumStateCollapsed:
		return "collapsed"
	case QuantumStateDecohered:
		return "decohered"
	default:
		return "unknown"
	}
}

// QuantumPair represents an entangled pair of quantum particles
type QuantumPair struct {
	ID           string    `json:"id"`
	NodeA        string    `json:"node_a"`
	NodeB        string    `json:"node_b"`
	Fidelity     float64   `json:"fidelity"`
	CreatedAt    time.Time `json:"created_at"`
	LastMeasured time.Time  `json:"last_measured"`
	StateA       QuantumState `json:"state_a"`
	StateB       QuantumState `json:"state_b"`
	MeasuredValueA float64   `json:"measured_value_a,omitempty"`
	MeasuredValueB float64   `json:"measured_value_b,omitempty"`
}

// IsEntangled checks if the pair maintains entanglement
func (qp *QuantumPair) IsEntangled() bool {
	return qp.StateA == QuantumStateSuperposition && 
		   qp.StateB == QuantumStateSuperposition && 
		   qp.Fidelity > 0.5
}

// Measure collapses the quantum state and returns measurement values
func (qp *QuantumPair) Measure() (float64, float64) {
	if qp.StateA == QuantumStateCollapsed && qp.StateB == QuantumStateCollapsed {
		return qp.MeasuredValueA, qp.MeasuredValueB
	}

	// Generate correlated random measurements
	valueA := qp.generateMeasurement()
	valueB := valueA // Perfect correlation for entangled particles

	qp.StateA = QuantumStateCollapsed
	qp.StateB = QuantumStateCollapsed
	qp.MeasuredValueA = valueA
	qp.MeasuredValueB = valueB
	qp.LastMeasured = time.Now()

	return valueA, valueB
}

// Decohere simulates quantum decoherence over time
func (qp *QuantumPair) Decohere(elapsed time.Duration) {
	if qp.StateA == QuantumStateDecohered || qp.StateB == QuantumStateDecohered {
		return
	}

	// Calculate decoherence factor based on time
	decoherenceFactor := 0.01 * elapsed.Seconds() / 60.0 // 1% per minute
	qp.Fidelity *= (1 - decoherenceFactor)

	if qp.Fidelity < 0.1 {
		qp.StateA = QuantumStateDecohered
		qp.StateB = QuantumStateDecohered
		qp.Fidelity = 0
	}

	qp.LastMeasured = time.Now()
}

// generateMeasurement creates a quantum measurement value
func (qp *QuantumPair) generateMeasurement() float64 {
	// Use crypto/rand for better randomness
	bytes := make([]byte, 8)
	rand.Read(bytes)
	// Convert to float64 in range [0, 1)
	hexStr := hex.EncodeToString(bytes)
	hashValue := 0.0
	for _, c := range hexStr {
		hashValue += float64(c)
	}
	return hashValue / (16 * 32 * float64(len(hexStr))) // Normalize to [0,1)
}

// String implements Stringer interface
func (qp *QuantumPair) String() string {
	return fmt.Sprintf("Pair{ID:%s, Nodes:%s-%s, Fidelity:%.3f, State:%s-%s}",
		qp.ID, qp.NodeA, qp.NodeB, qp.Fidelity, qp.StateA, qp.StateB)
}

// GeneratorConfig configures the pair generator
type GeneratorConfig struct {
	DefaultFidelity float64
	MaxPairs        int
}

// PairGenerator creates entangled quantum pairs
type PairGenerator struct {
	config GeneratorConfig
}

// NewPairGenerator creates a new pair generator
func NewPairGenerator(config GeneratorConfig) *PairGenerator {
	if config.DefaultFidelity <= 0 || config.DefaultFidelity > 1 {
		config.DefaultFidelity = 0.95
	}
	if config.MaxPairs <= 0 {
		config.MaxPairs = 1000
	}
	return &PairGenerator{config: config}
}

// GeneratePairs creates multiple entangled pairs
func (pg *PairGenerator) GeneratePairs(count int) ([]*QuantumPair, error) {
	if count <= 0 {
		return nil, fmt.Errorf("pair count must be positive")
	}
	if count > pg.config.MaxPairs {
		return nil, fmt.Errorf("cannot generate more than %d pairs", pg.config.MaxPairs)
	}

	pairs := make([]*QuantumPair, count)
	for i := 0; i < count; i++ {
		pairs[i] = pg.generateSinglePair()
	}

	return pairs, nil
}

// generateSinglePair creates one entangled pair
func (pg *PairGenerator) generateSinglePair() *QuantumPair {
	id := pg.generateID()
	return &QuantumPair{
		ID:        id,
		NodeA:     fmt.Sprintf("node-%d", (i%2)+1), // Alternate between node-1 and node-2
		NodeB:     fmt.Sprintf("node-%d", ((i+1)%2)+1),
		Fidelity:  pg.config.DefaultFidelity,
		CreatedAt: time.Now(),
		StateA:    QuantumStateSuperposition,
		StateB:    QuantumStateSuperposition,
	}
}

// generateID creates a unique identifier for the pair
func (pg *PairGenerator) generateID() string {
	bytes := make([]byte, 16)
	rand.Read(bytes)
	return hex.EncodeToString(bytes)
}
