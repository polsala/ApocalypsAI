package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"
)

type TimeResponse struct {
	Timestamp string `json:"timestamp"`
	DriftMs   int    `json:"drift_ms,omitempty"`
	Message   string `json:"message"`
}

func timeHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	currentTime := time.Now().UTC()
	driftMs := 0

	driftParam := r.URL.Query().Get("drift_ms")
	if driftParam != "" {
		parsedDrift, err := strconv.Atoi(driftParam)
		if err != nil {
			http.Error(w, `{"error": "Invalid drift_ms parameter. Must be an integer."}`, http.StatusBadRequest)
			return
		}
		driftMs = parsedDrift
		currentTime = currentTime.Add(time.Duration(driftMs) * time.Millisecond)
	}

	response := TimeResponse{
		Timestamp: currentTime.Format(time.RFC3339Nano),
		DriftMs:   driftMs,
		Message:   "Time signal from the Chrono-Sync Beacon. May contain temporal whimsy.",
	}

	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("Error encoding response: %v", err)
		http.Error(w, `{"error": "Internal server error."}`, http.StatusInternalServerError)
	}
}

func statusHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := map[string]string{
		"status":  "Operational",
		"message": "Chrono-Sync Beacon is humming along, broadcasting temporal truths (mostly).",
		"uptime":  time.Since(startTime).String(),
	}
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("Error encoding status response: %v", err)
		http.Error(w, `{"error": "Internal server error."}`, http.StatusInternalServerError)
	}
}

var startTime time.Time

func main() {
	startTime = time.Now()
	port := flag.Int("port", 8080, "Port to run the Chrono-Sync Beacon on")
	flag.Parse()

	http.HandleFunc("/time", timeHandler)
	http.HandleFunc("/status", statusHandler)

	addr := fmt.Sprintf(":%d", *port)
	log.Printf("Chrono-Sync Beacon starting on port %s", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}
