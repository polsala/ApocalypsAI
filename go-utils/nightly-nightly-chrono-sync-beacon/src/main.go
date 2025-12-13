package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"
)

// BeaconResponse represents the JSON structure for the time beacon response.
type BeaconResponse struct {
	BeaconID            string    `json:"beacon_id"`
	CurrentTimeUTC      time.Time `json:"current_time_utc"`
	TemporalOffsetSeconds int       `json:"temporal_offset_seconds"`
	Message             string    `json:"message"`
}

var (
	port          = flag.Int("port", 8080, "Port for the Chrono-Sync Beacon server to listen on")
	offsetSeconds = flag.Int("offset", 0, "Temporal offset in seconds to apply to UTC time (can be negative)")
	beaconID      = flag.String("id", "APOCALYPSAI-BEACON-001", "Unique identifier for this Chrono-Sync Beacon")
)

func main() {
	flag.Parse()

	log.Printf("Starting Chrono-Sync Beacon '%s' on port %d with temporal offset of %d seconds...",
		*beaconID, *port, *offsetSeconds)

	http.HandleFunc("/time", timeHandler)

	addr := fmt.Sprintf(":%d", *port)
	log.Fatal(http.ListenAndServe(addr, nil))
}

func timeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Get current UTC time and apply the configured offset
	nowUTC := time.Now().UTC()
	adjustedTime := nowUTC.Add(time.Duration(*offsetSeconds) * time.Second)

	response := BeaconResponse{
		BeaconID:            *beaconID,
		CurrentTimeUTC:      adjustedTime,
		TemporalOffsetSeconds: *offsetSeconds,
		Message:             "Time synchronized from the ApocalypsAI Chrono-Sync Beacon. May your chronometers be ever true (or whimsically skewed).",
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("Error encoding response: %v", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
	}
}
