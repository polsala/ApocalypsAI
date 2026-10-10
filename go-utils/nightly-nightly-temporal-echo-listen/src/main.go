package main

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

// TemporalAnchor represents a point in the temporal fabric to listen to.
type TemporalAnchor struct {
	Name             string
	SimulatedDelayMs int // Base delay in milliseconds
	AnomalyChance    int // Percentage chance of an anomaly (0-100)
}

// TemporalEchoReport contains the results of listening to an anchor.
type TemporalEchoReport struct {
	AnchorName string
	Status     string
	DurationMs int
	Error      string
}

// For testability, these can be overridden in tests.
var (
	sleepFunc    = time.Sleep
	randIntnFunc = rand.Intn
)

// listenToAnchor simulates listening to a single temporal anchor.
func listenToAnchor(anchor TemporalAnchor) TemporalEchoReport {
	start := time.Now()
	var report TemporalEchoReport
	report.AnchorName = anchor.Name

	// Simulate delay
	delay := time.Duration(anchor.SimulatedDelayMs) * time.Millisecond
	sleepFunc(delay)

	// Simulate anomaly
	if randIntnFunc(100) < anchor.AnomalyChance {
		report.Status = "ANOMALY DETECTED"
		report.Error = "Temporal distortion detected at anchor point."
		// Add some extra simulated delay for anomalies
		sleepFunc(time.Duration(anchor.SimulatedDelayMs/2) * time.Millisecond)
	} else {
		report.Status = "STABLE"
	}

	report.DurationMs = int(time.Since(start).Milliseconds())
	return report
}

// runListener orchestrates the concurrent listening to all defined anchors
// and returns a slice of reports.
func runListener() []TemporalEchoReport {
	// Define our temporal anchors
	anchors := []TemporalAnchor{
		{Name: "Alpha Stream", SimulatedDelayMs: 100, AnomalyChance: 5},
		{Name: "Beta Nexus", SimulatedDelayMs: 150, AnomalyChance: 10},
		{Name: "Gamma Chronos", SimulatedDelayMs: 200, AnomalyChance: 2},
		{Name: "Delta Rift", SimulatedDelayMs: 50, AnomalyChance: 25},
		{Name: "Epsilon Echo", SimulatedDelayMs: 120, AnomalyChance: 8},
	}

	var wg sync.WaitGroup
	reportsChan := make(chan TemporalEchoReport, len(anchors)) // Buffered channel
	
	for _, anchor := range anchors {
		wg.Add(1)
		go func(a TemporalAnchor) {
			defer wg.Done()
			report := listenToAnchor(a)
			reportsChan <- report
		}(anchor)
	}

	// Wait for all goroutines to finish, then close the channel
	go func() {
		wg.Wait()
		close(reportsChan)
	}()

	// Collect reports
	var reports []TemporalEchoReport
	for report := range reportsChan {
		reports = append(reports, report)
	}
	return reports
}

func main() {
	fmt.Println("Initiating Temporal Echo Listener...")
	fmt.Println("-----------------------------------")

	reports := runListener()

	fmt.Println("Temporal Echo Reports:")
	for _, report := range reports {
		statusColor := "\033[0m" // Reset
		if report.Status == "ANOMALY DETECTED" {
			statusColor = "\033[31m" // Red
		} else {
			statusColor = "\033[32m" // Green
		}
		fmt.Printf("  [%s%s\033[0m] Anchor: %-15s Duration: %4dms", statusColor, report.Status, report.AnchorName, report.DurationMs)
		if report.Error != "" {
			fmt.Printf(" Error: %s", report.Error)
		}
		fmt.Println()
	}

	fmt.Println("-----------------------------------")
	fmt.Println("Temporal Echo Listener complete.")
}
