package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sort"
	"sync"
	"time"
)

// MoodReport represents a single mood reported by a component.
type MoodReport struct {
	Source    string    `json:"source"`
	Mood      string    `json:"mood"`
	Timestamp time.Time `json:"timestamp"`
}

// MoodRing stores and manages the moods of various components.
type MoodRing struct {
	mu             sync.RWMutex
	componentMoods map[string]MoodReport
}

// NewMoodRing creates and returns a new MoodRing instance.
func NewMoodRing() *MoodRing {
	return &MoodRing{
		componentMoods: make(map[string]MoodReport),
	}
}

// reportMoodHandler handles incoming POST requests to report a component's mood.
func (mr *MoodRing) reportMoodHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	var report MoodReport
	if err := json.NewDecoder(r.Body).Decode(&report); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if report.Source == "" || report.Mood == "" {
		http.Error(w, "'source' and 'mood' fields are required", http.StatusBadRequest)
		return
	}

	report.Timestamp = time.Now().UTC()

	mr.mu.Lock()
	mr.componentMoods[report.Source] = report
	mr.mu.Unlock()

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Mood for %s updated to %s\n", report.Source, report.Mood)
	log.Printf("Received mood report: Source=%s, Mood=%s\n", report.Source, report.Mood)
}

// getStatusHandler handles incoming GET requests to retrieve the overall network mood.
func (mr *MoodRing) getStatusHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
		return
	}

	mr.mu.RLock()
	defer mr.mu.RUnlock()

	allMoods := make([]MoodReport, 0, len(mr.componentMoods))
	for _, mood := range mr.componentMoods {
		allMoods = append(allMoods, mood)
	}

	// Sort by source for deterministic output in tests and consistent API responses
	sort.Slice(allMoods, func(i, j int) bool {
		return allMoods[i].Source < allMoods[j].Source
	})

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(map[string][]MoodReport{"component_moods": allMoods}); err != nil {
		log.Printf("Error encoding response: %v", err)
		http.Error(w, "Internal server error", http.StatusInternalServerError)
	}
}

func main() {
	mr := NewMoodRing()

	http.HandleFunc("/report", mr.reportMoodHandler)
	http.HandleFunc("/status", mr.getStatusHandler)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	addr := fmt.Sprintf(":%s", port)
	log.Printf("Nightly Network Mood Ring server starting on port %s...\n", port)
	log.Fatal(http.ListenAndServe(addr, nil))
}
