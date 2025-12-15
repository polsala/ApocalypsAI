package quantum

import (
	"math/rand"
	"time"
)

// VerificationResult contains the result of an entanglement verification
type VerificationResult struct {
	Entangled        bool    `json:"entangled"`
	MeasuredFidelity float64 `json:"measured_fidelity"`
	Correlation      float64 `json:"correlation"`
	Timestamp        time.Time `json:"timestamp"`
	Error            string  `json:"error,omitempty"`
}

// EntanglementVerifier verifies quantum entanglement between nodes
type EntanglementVerifier struct {
	rand *rand.Rand
}

// NewEntanglementVerifier creates a new verifier
func NewEntanglementVerifier() *EntanglementVerifier {
	return &EntanglementVerifier{
		rand: rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// VerifyEntanglement checks if two nodes maintain entanglement
func (ev *EntanglementVerifier) VerifyEntanglement(nodeA, nodeB string) VerificationResult {
	if nodeA == nodeB {
		return VerificationResult{
			Entangled: false,
			Error:     "nodes must be different",
			Timestamp: time.Now(),
		}
	}

	// Simulate measurement correlation
	correlation := ev.rand.Float64() * 0.8 + 0.2 // Range [0.2, 1.0]
	fidelity := correlation * (0.8 + ev.rand.Float64()*0.2) // Range [0.8*correlation, 1.0*correlation]

	// Determine if entangled based on correlation threshold
	entangled := correlation > 0.7

	return VerificationResult{
		Entangled:        entangled,
		MeasuredFidelity: fidelity,
		Correlation:      correlation,
		Timestamp:        time.Now(),
	}
}

// BatchVerify performs multiple verification tests
func (ev *EntanglementVerifier) BatchVerify(nodeA, nodeB string, iterations int) []VerificationResult {
	results := make([]VerificationResult, iterations)
	for i := 0; i < iterations; i++ {
		results[i] = ev.VerifyEntanglement(nodeA, nodeB)
	}
	return results
}

// CalculateAverageFidelity computes the average fidelity from results
func CalculateAverageFidelity(results []VerificationResult) float64 {
	if len(results) == 0 {
		return 0.0
	}

	total := 0.0
	count := 0
	for _, result := range results {
		if result.Error == "" {
			total += result.MeasuredFidelity
			count++
		}
	}

	if count == 0 {
		return 0.0
	}

	return total / float64(count)
}

// CalculateEntanglementRatio computes the ratio of successful entanglements
func CalculateEntanglementRatio(results []VerificationResult) float64 {
	if len(results) == 0 {
		return 0.0
	}

	entangled := 0
	for _, result := range results {
		if result.Entangled && result.Error == "" {
			entangled++
		}
	}

	return float64(entangled) / float64(len(results))
}
