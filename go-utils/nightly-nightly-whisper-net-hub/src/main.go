package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)

// Whisper represents a message received from a node.
type Whisper struct {
	Origin  string `json:"origin"`
	Message string `json:"message"`
	Timestamp time.Time `json:"timestamp"`
}

// WhisperHub manages the collection and aggregation of whispers.
type WhisperHub struct {
	mu      sync.Mutex
	whispers map[string][]Whisper // Key: Origin, Value: List of whispers from that origin
}

// NewWhisperHub creates a new WhisperHub instance.
func NewWhisperHub() *WhisperHub {
	return &WhisperHub{
		whispers: make(map[string][]Whisper),
	}
}

// HandleWhisper receives and stores a new whisper.
func (h *WhisperHub) HandleWhisper(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST requests are accepted", http.StatusMethodNotAllowed)
		return
	}

	var incomingWhisper Whisper
	err := json.NewDecoder(r.Body).Decode(&incomingWhisper)
	if err != nil {
		http.Error(w, "Invalid whisper format", http.StatusBadRequest)
		return
	}

	if incomingWhisper.Origin == "" || incomingWhisper.Message == "" {
		http.Error(w, "Origin and Message cannot be empty", http.StatusBadRequest)
		return
	}

	incomingWhisper.Timestamp = time.Now().UTC()

	h.mu.Lock()
	h.whispers[incomingWhisper.Origin] = append(h.whispers[incomingWhisper.Origin], incomingWhisper)
	h.mu.Unlock()

	log.Printf("Received whisper from %s: \"%s\"", incomingWhisper.Origin, incomingWhisper.Message)
	w.WriteHeader(http.StatusAccepted)
	fmt.Fprintf(w, "Whisper received from %s\n", incomingWhisper.Origin)
}

// HandleStatus provides a JSON overview of all collected whispers.
func (h *WhisperHub) HandleStatus(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Only GET requests are accepted", http.StatusMethodNotAllowed)
		return
	}

	h.mu.Lock()
	defer h.mu.Unlock()

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(h.whispers)
}

func main() {
	hub := NewWhisperHub()

	http.HandleFunc("/whisper", hub.HandleWhisper)
	http.HandleFunc("/status", hub.HandleStatus)

	port := ":8080"
	log.Printf("WhisperNet Hub listening on port %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
