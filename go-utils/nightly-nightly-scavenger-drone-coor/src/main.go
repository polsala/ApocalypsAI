package main

import (
	"flag"
	"fmt"
	"log"
	"math/rand"
	"strings"
	"sync"
	"time"
)

// ScavengeResult holds the outcome of a single drone's scavenging mission.
type ScavengeResult struct {
	Zone     string
	Resource string
	Error    error
}

// ScavengeFn defines the signature for a function that simulates a drone scavenging a zone.
type ScavengeFn func(zone string) (string, error)

// ScavengeCoordinator manages the dispatch and collection of scavenger drone results.
type ScavengeCoordinator struct {
	scavengeAction ScavengeFn
}

// NewScavengeCoordinator creates a new coordinator with a given scavenging function.
func NewScavengeCoordinator(action ScavengeFn) *ScavengeCoordinator {
	return &ScavengeCoordinator{
		scavengeAction: action,
	}
}

// CoordinateScavenging dispatches drones to zones concurrently and collects their findings.
func (c *ScavengeCoordinator) CoordinateScavenging(zones []string) []ScavengeResult {
	if len(zones) == 0 {
		return []ScavengeResult{}
	}

	resultsChan := make(chan ScavengeResult, len(zones))
	var wg sync.WaitGroup

	for _, zone := range zones {
		wg.Add(1)
		go func(z string) {
			defer wg.Done()
			resource, err := c.scavengeAction(z)
			resultsChan <- ScavengeResult{Zone: z, Resource: resource, Error: err}
		}(zone)
	}

	wg.Wait()
	close(resultsChan)

	var allResults []ScavengeResult
	for res := range resultsChan {
		allResults = append(allResults, res)
	}
	return allResults
}

// simulatedScavenge is a default ScavengeFn that simulates finding a random resource after a delay.
func simulatedScavenge(zone string) (string, error) {
	// # Mock rationale: In a real scenario, this might involve network requests,
	// # database lookups, or complex computations. For this utility, we simulate
	// # it with a random delay and predefined resources to keep it self-contained
	// # and deterministic for testing (when mocked).
	time.Sleep(time.Duration(rand.Intn(500)+100) * time.Millisecond) // Simulate work

	resources := []string{"Scrap Metal", "Purified Water", "Ancient Tech Part", "Mutated Flora", "Pre-War Ration"}
	if rand.Intn(10) == 0 { // 10% chance of failure
		return "", fmt.Errorf("drone encountered a temporal anomaly in %s", zone)
	}
	return resources[rand.Intn(len(resources))], nil
}

func main() {
	zonesStr := flag.String("zones", "", "Comma-separated list of wasteland zones to scavenge")
	flag.Parse()

	if *zonesStr == "" {
		log.Fatal("Error: Please provide at least one zone using --zones")
	}

	zones := strings.Split(*zonesStr, ",")
	for i := range zones {
		zones[i] = strings.TrimSpace(zones[i])
	}

	// Seed random for simulatedScavenge. This makes the main utility's output non-deterministic,
	// but tests use deterministic mocks.
	rand.Seed(time.Now().UnixNano())

	coordinator := NewScavengeCoordinator(simulatedScavenge)
	fmt.Printf("Dispatching scavenger drones to %d zones...\n", len(zones))

	results := coordinator.CoordinateScavenging(zones)

	fmt.Println("\n--- Scavenging Report ---")
	for _, res := range results {
		if res.Error != nil {
			fmt.Printf("Zone: %s | Status: FAILED | Error: %v\n", res.Zone, res.Error)
		} else {
			fmt.Printf("Zone: %s | Found: %s\n", res.Zone, res.Resource)
		}
	}
	fmt.Println("-------------------------")
}
