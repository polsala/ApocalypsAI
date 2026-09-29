package main

import (
	"fmt"
	"io"
	"math/rand"
	"os"
	"strings"
	"sync"
	"time"
)

// ScavengeResult holds the outcome of a scavenger's search in a zone.
type ScavengeResult struct {
	Zone    string
	Found   bool
	Message string
}

// ZoneContents is a mock data source for zones.
// # Mock rationale: This map simulates the resources available in different zones
// # without requiring actual file I/O or network requests, ensuring deterministic tests.
var ZoneContents = map[string][]string{
	"Old Factory":    {"scrap metal", "wires", "rusty tools"},
	"Abandoned Mall": {"canned food", "water filter", "first aid kit", "clothing"},
	"Overgrown Park": {"herbs", "wild berries", "fresh water source"},
	"Collapsed Bridge": {"rope", "climbing gear"},
	"Silent Library": {"books", "maps", "old records"},
}

// Scavenge simulates searching a specific zone for a target resource.
// It returns true if the resource is found, false otherwise.
// It also simulates a variable delay.
func Scavenge(zone string, target string) ScavengeResult {
	// Simulate network latency or search time
	// The random delay makes execution time non-deterministic but not the search result.
	time.Sleep(time.Duration(rand.Intn(500)+100) * time.Millisecond) // 100-600ms delay

	resources, exists := ZoneContents[zone]
	if !exists {
		return ScavengeResult{Zone: zone, Found: false, Message: "Zone not recognized or empty."}
	}

	for _, res := range resources {
		if strings.EqualFold(res, target) {
			return ScavengeResult{Zone: zone, Found: true, Message: fmt.Sprintf("Found '%s' in %s!", target, zone)}
		}
	}

	return ScavengeResult{Zone: zone, Found: false, Message: fmt.Sprintf("'%s' not found in %s.", target, zone)}
}

func main() {
	// Initialize random seed for time.Sleep variability
	rand.Seed(time.Now().UnixNano())

	if len(os.Args) < 3 {
		fmt.Println("Usage: nightly-scavenger-swarm-coord <target_resource> <zone1> [zone2]...")
		os.Exit(1)
	}

	targetResource := os.Args[1]
	zones := os.Args[2:]

	fmt.Printf("Dispatching scavenger swarm to find '%s' across %d zones...\n", targetResource, len(zones))

	resultsChan := make(chan ScavengeResult, len(zones))
	var wg sync.WaitGroup

	for _, zone := range zones {
		wg.Add(1)
		go func(z string) {
			defer wg.Done()
			result := Scavenge(z, targetResource)
			resultsChan <- result
		}(zone)
	}

	wg.Wait()
	close(resultsChan)

	foundCount := 0
	for result := range resultsChan {
		if result.Found {
			fmt.Printf("[SUCCESS] %s\n", result.Message)
			foundCount++
		} else {
			fmt.Printf("[FAILURE] %s\n", result.Message)
		}
	}

	fmt.Printf("\n--- Scavenge Summary ---\n")
	if foundCount > 0 {
		fmt.Printf("Successfully located '%s' in %d out of %d zones.\n", targetResource, foundCount, len(zones))
	} else {
		fmt.Printf("'%s' was not found in any of the %d zones.\n", targetResource, len(zones))
	}
}
