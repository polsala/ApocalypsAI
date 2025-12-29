package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"
)

type TimeResponse struct {
	UTCTime        string `json:"utc_time"`
	TemporalStatus string `json:"temporal_status"`
}

func timeHandler(w http.ResponseWriter, r *http.Request) {
	currentTime := time.Now().UTC()
	response := TimeResponse{
		UTCTime:        currentTime.Format(time.RFC3339Nano),
		TemporalStatus: "Temporal flow is stable. All systems nominal.", // Deterministic for testing
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	http.HandleFunc("/time", timeHandler)
	port := ":8080"
	fmt.Printf("Chrono-Sync Beacon listening on port %s...\n", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
