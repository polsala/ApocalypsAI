package quantum

import (
	"sync"
	"time"
)

// CoherenceStatus represents the current coherence state
type CoherenceStatus struct {
	Coherence   float64 `json:"coherence"`
	Stable      bool    `json:"stable"`
	Measurements int    `json:"measurements"`
	LastUpdate  time.Time `json:"last_update"`
}

// CoherenceMonitor tracks quantum system coherence
type CoherenceMonitor struct {
	mu        sync.RWMutex
	threshold float64
	coherence float64
	measurements int
	stable    bool
	startTime time.Time
}

// NewCoherenceMonitor creates a new coherence monitor
func NewCoherenceMonitor(threshold float64) *CoherenceMonitor {
	if threshold <= 0 || threshold > 1 {
		threshold = 0.8
	}

	return &CoherenceMonitor{
		threshold: threshold,
		coherence: 1.0,
		stable:    true,
		startTime: time.Now(),
	}
}

// Measure performs a coherence measurement
func (cm *CoherenceMonitor) Measure() CoherenceStatus {
	cm.mu.Lock()
	defer cm.mu.Unlock()

	// Simulate measurement noise
	noise := (rand.Float64() - 0.5) * 0.05 // ±2.5%
	cm.coherence += noise
	cm.coherence = clamp(cm.coherence, 0.0, 1.0)
	cm.measurements++

	// Check stability
	cm.stable = cm.coherence >= cm.threshold

	return CoherenceStatus{
		Coherence:   cm.coherence,
		Stable:      cm.stable,
		Measurements: cm.measurements,
		LastUpdate:  time.Now(),
	}
}

// GetStatus returns the current status without measurement
func (cm *CoherenceMonitor) GetStatus() CoherenceStatus {
	cm.mu.RLock()
	defer cm.mu.RUnlock()

	return CoherenceStatus{
		Coherence:   cm.coherence,
		Stable:      cm.stable,
		Measurements: cm.measurements,
		LastUpdate:  time.Now(),
	}
}

// SimulateDecoherence simulates natural decoherence over time
func (cm *CoherenceMonitor) SimulateDecoherence(elapsed time.Duration) CoherenceStatus {
	cm.mu.Lock()
	defer cm.mu.Unlock()

	// Natural decoherence: 0.1% per second
	decoherence := 0.001 * elapsed.Seconds()
	cm.coherence *= (1 - decoherence)
	cm.coherence = clamp(cm.coherence, 0.0, 1.0)
	cm.stable = cm.coherence >= cm.threshold
	cm.measurements++

	return CoherenceStatus{
		Coherence:   cm.coherence,
		Stable:      cm.stable,
		Measurements: cm.measurements,
		LastUpdate:  time.Now(),
	}
}

// Reset resets the monitor to initial state
func (cm *CoherenceMonitor) Reset() {
	cm.mu.Lock()
	defer cm.mu.Unlock()

	cm.coherence = 1.0
	cm.measurements = 0
	cm.stable = true
	cm.startTime = time.Now()
}

// clamp ensures a value stays within bounds
func clamp(value, min, max float64) float64 {
	if value < min {
		return min
	}
	if value > max {
		return max
	}
	return value
}
