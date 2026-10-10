package main

import (
	"fmt"
	"io"
	"math/rand"
	"os"
	"sort"
	"sync"
	"time"
)

// Beacon represents a temporal point to be pinged.
type Beacon struct {
	Name string
}

// PingResult holds the outcome of a single beacon ping.
type PingResult struct {
	BeaconName   string
	DriftMs      int
	Status       string
	ErrorMessage string
}

// Pinger defines the interface for pinging a beacon.
type Pinger interface {
	Ping(b *Beacon) PingResult
}

// RealPinger implements Pinger for actual simulation.
type RealPinger struct {
	randSource *rand.Rand // Use a specific rand source for testability
	sleepFunc  func(time.Duration)
}

// NewRealPinger creates a new RealPinger with a given seed and sleep function.
func NewRealPinger(seed int64, sleepFn func(time.Duration)) *RealPinger {
	return &RealPinger{
		randSource: rand.New(rand.NewSource(seed)),
		sleepFunc:  sleepFn,
	}
}

// Ping simulates a temporal connection to a beacon.
// It introduces random latency and a chance of failure.
func (rp *RealPinger) Ping(b *Beacon) PingResult {
	// Simulate temporal drift (latency) between 50ms and 500ms
	drift := rp.randSource.Intn(451) + 50 // 50-500ms
	rp.sleepFunc(time.Duration(drift) * time.Millisecond)

	// Simulate a 20% chance of temporal instability (failure)
	if rp.randSource.Intn(100) < 20 { // 20% chance of failure
		return PingResult{
			BeaconName:   b.Name,
			DriftMs:      drift,
			Status:       "UNSTABLE",
			ErrorMessage: "Connection Rift!",
		}
	}

	return PingResult{
		BeaconName: b.Name,
		DriftMs:    drift,
		Status:     "STABLE",
	}
}

// run orchestrates the pinging process and writes results to the provided writer.
func run(out io.Writer, beaconNames []string, pinger Pinger) {
	if len(beaconNames) == 0 {
		// Default beacons if none are provided
		beaconNames = []string{
			"Chronos-Nexus",
			"Aether-Gate",
			"Void-Anchor",
			"Temporal-Flux-Point",
			"Echo-Chamber-Prime",
		}
	}

	fmt.Fprintf(out, "Pinging %d temporal beacons...\n\n", len(beaconNames))

	var wg sync.WaitGroup
	resultsChan := make(chan PingResult, len(beaconNames))

	for _, name := range beaconNames {
		wg.Add(1)
		go func(beaconName string) {
			defer wg.Done()
			beacon := Beacon{Name: beaconName}
			resultsChan <- pinger.Ping(&beacon)
		}(name)
	}

	wg.Wait()
	close(resultsChan)

	var allResults []PingResult
	for res := range resultsChan {
		allResults = append(allResults, res)
	}

	// Sort results by beacon name for deterministic output in tests
	sort.Slice(allResults, func(i, j int) bool {
		return allResults[i].BeaconName < allResults[j].BeaconName
	})

	stableCount := 0
	unstableCount := 0

	for _, res := range allResults {
		if res.Status == "STABLE" {
			fmt.Fprintf(out, "[%s] Temporal Drift: %dms, Status: %s\n", res.BeaconName, res.DriftMs, res.Status)
			stableCount++
		} else {
			fmt.Fprintf(out, "[%s] Temporal Drift: %dms, Status: %s (%s)\n", res.BeaconName, res.DriftMs, res.Status, res.ErrorMessage)
			unstableCount++
		}
	}

	fmt.Fprintf(out, "\nTemporal Beacon Pinger Report:\n")
	fmt.Fprintf(out, "- Total Beacons: %d\n", len(allResults))
	fmt.Fprintf(out, "- Stable Beacons: %d\n", stableCount)
	fmt.Fprintf(out, "- Unstable Beacons: %d\n", unstableCount)
}

func main() {
	// Use current time for seeding in production, but allow tests to inject a fixed seed.
	// The RealPinger constructor handles the seeding.
	pinger := NewRealPinger(time.Now().UnixNano(), time.Sleep)
	run(os.Stdout, os.Args[1:], pinger)
}
