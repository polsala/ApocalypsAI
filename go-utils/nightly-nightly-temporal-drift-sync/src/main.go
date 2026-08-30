package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"sync"
)

// DriftReport represents a single temporal drift report from a node.
type DriftReport struct {
	NodeID    string  `json:"node_id"`
	DriftValue float64 `json:"drift_value"`
}

// ConsensusResponse represents the response for the consensus drift endpoint.
type ConsensusResponse struct {
	ConsensusDrift float64 `json:"consensus_drift"`
}

// ErrorResponse represents a generic error response.
type ErrorResponse struct {
	Error string `json:"error"`
}

// DriftManager manages the collection and calculation of temporal drifts.
type DriftManager struct {
	mu     sync.RWMutex
	drifts map[string]float64 // Map from NodeID to its latest DriftValue
}

// NewDriftManager creates and returns a new DriftManager.
func NewDriftManager() *DriftManager {
	return &DriftManager{
		drifts: make(map[string]float64),
	}
}

// AddDrift adds or updates a drift report for a given node.
func (dm *DriftManager) AddDrift(nodeID string, driftValue float64) {
	dm.mu.Lock()
	defer dm.mu.Unlock()
	dm.drifts[nodeID] = driftValue
	log.Printf("Node %s reported drift: %.2f", nodeID, driftValue)
}

// GetConsensusDrift calculates the average of all reported drift values.
func (dm *DriftManager) GetConsensusDrift() float64 {
	dm.mu.RLock()
	defer dm.mu.RUnlock()

	if len(dm.drifts) == 0 {
		return 0.0
	}

	totalDrift := 0.0
	for _, drift := range dm.drifts {
		totalDrift += drift
	}
	return totalDrift / float64(len(dm.drifts))
}

// handleReportDrift handles incoming POST requests to report temporal drift.
func handleReportDrift(dm *DriftManager, w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var report DriftReport
	if err := json.NewDecoder(r.Body).Decode(&report); err != nil {
		sendJSONError(w, "Invalid request payload", http.StatusBadRequest)
		return
	}

	if report.NodeID == "" {
		sendJSONError(w, "NodeID cannot be empty", http.StatusBadRequest)
		return
	}

	dm.AddDrift(report.NodeID, report.DriftValue)
	w.WriteHeader(http.StatusAccepted)
	fmt.Fprintf(w, `{"status": "drift reported for %s"}`, report.NodeID)
}

// handleGetConsensus handles incoming GET requests to retrieve the consensus drift.
func handleGetConsensus(dm *DriftManager, w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	consensus := dm.GetConsensusDrift()
	response := ConsensusResponse{ConsensusDrift: consensus}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("Error encoding consensus response: %v", err)
		sendJSONError(w, "Internal server error", http.StatusInternalServerError)
	}
}

// sendJSONError sends a JSON formatted error response.
func sendJSONError(w http.ResponseWriter, message string, statusCode int) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(ErrorResponse{Error: message})
}

func main() {
	dm := NewDriftManager()

	http.HandleFunc("/report-drift", func(w http.ResponseWriter, r *http.Request) {
		handleReportDrift(dm, w, r)
	})
	http.HandleFunc("/consensus-drift", func(w http.ResponseWriter, r *http.Request) {
		handleGetConsensus(dm, w, r)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port
	}
	addr := ":" + port

	log.Printf("Nightly Temporal Drift Synchronizer starting on %s", addr)
	log.Fatal(http.ListenAndServe(addr, nil))
}
