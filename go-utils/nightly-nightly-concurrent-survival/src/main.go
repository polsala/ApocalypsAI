package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"sync"
)

// ResourceCheck defines a survival resource status check
func ResourceCheck(name string, weight int, wg *sync.WaitGroup, results chan<- string) {
	defer wg.Done()

	// Simulate resource status calculation
	score := rand.Intn(100)
	status := "STABLE"
	emoji := "✅"

	if score < weight-20 {
		status = "CRITICAL"
		emoji = "🔥"
	} else if score < weight-10 {
		status = "LOW"
		emoji = "⚠️"
	}

	// Whimsical alert generation
	var alert string
	switch name {
	case "water":
		alert = fmt.Sprintf("%s The aquifer is %s (%d%% hydration). Bring backup cactus!", emoji, status, score)
	case "food":
		alert = fmt.Sprintf("%s The bug stash is %s (%d%% full). Consider eating that weird moss.", emoji, status, score)
	case "shelter":
		alert = fmt.Sprintf("%s Your bunker is %s (%d%% intact). Roof is missing 3 tiles.", emoji, status, score)
	default:
		alert = fmt.Sprintf("%s %s status: %d%%", emoji, name, score)
	}

	results <- alert
}

func main() {
	// Parse command line args
	waterWeight := 50
	foodWeight := 50
	shelterWeight := 50

	if len(os.Args) > 1 {
		for i := 1; i < len(os.Args); i++ {
			if os.Args[i][:1] == "--" {
				kv := os.Args[i][2:]
				sep := strings.Split(kv, "=")
				if len(sep) == 2 {
					val, _ := strconv.Atoi(sep[1])
					switch sep[0] {
					case "water":
						waterWeight = val
					case "food":
						foodWeight = val
					case "shelter":
						shelterWeight = val
					}
				}
			}
		}
	}

	var wg sync.WaitGroup
	results := make(chan string, 3)

	// Launch concurrent checks
	wg.Add(3)
	go ResourceCheck("water", waterWeight, &wg, results)
	go ResourceCheck("food", foodWeight, &wg, results)
	go ResourceCheck("shelter", shelterWeight, &wg, results)

	// Wait for all checks to complete
	go func() {
		wg.Wait()
		close(results)
	}()

	// Display results in arbitrary order
	fmt.Println("SURVIVAL STATUS REPORT")
	fmt.Println("--------------------")
	for alert := range results {
		fmt.Println(alert)
	}
}
