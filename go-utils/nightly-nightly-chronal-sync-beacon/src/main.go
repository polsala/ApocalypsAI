package main

import (
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"
)

const defaultPort = "8080"

func main() {
	port := defaultPort
	if len(os.Args) > 1 {
		port = os.Args[1]
	}

	http.HandleFunc("/time", timeHandler)

	addr := ":" + port
	log.Printf("Chronal Sync Beacon listening on %s", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}

// timeHandler serves the current time, with optional drift and anomaly.
func timeHandler(w http.ResponseWriter, r *http.Request) {
	currentTime := time.Now().UTC()

	// Apply drift if specified
	driftStr := r.URL.Query().Get("drift")
	if driftStr != "" {
		driftDuration, err := time.ParseDuration(driftStr)
		if err != nil {
			http.Error(w, fmt.Sprintf("Invalid drift duration: %s", err), http.StatusBadRequest)
			return
		}
		currentTime = currentTime.Add(driftDuration)
	}

	// Apply anomaly if specified
	if r.URL.Query().Get("anomaly") != "" {
		// # Mock rationale: In tests, rand.Seed is used to make this deterministic.
		// In production, it's truly random.
		// Random drift between -1 hour and +1 hour
		randomOffsetSeconds := rand.Intn(7200) - 3600 // -3600 to +3599 seconds
		anomalyDuration := time.Duration(randomOffsetSeconds) * time.Second
		currentTime = currentTime.Add(anomalyDuration)
	}

	w.Header().Set("Content-Type", "text/plain; charset=utf-8")
	fmt.Fprint(w, currentTime.Format(time.RFC3339Nano))
}

// Helper for tests to set a deterministic random seed
func setDeterministicRandSeed(seed int64) {
	rand.Seed(seed)
}
