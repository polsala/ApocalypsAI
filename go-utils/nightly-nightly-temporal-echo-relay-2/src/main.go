package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"time"
)

// RelayRequest defines the structure of the incoming JSON payload.
type RelayRequest struct {
	Message   string `json:"message"`
	TargetURL string `json:"target_url"`
	DelayMs   int    `json:"delay_ms"` // Optional, default to 100ms
}

// defaultSleeper is the default function for sleeping. It can be overridden for testing.
var defaultSleeper = time.Sleep

// relayHandler handles incoming relay requests.
func relayHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is supported", http.StatusMethodNotAllowed)
		return
	}

	var req RelayRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	if req.TargetURL == "" {
		http.Error(w, "target_url is required", http.StatusBadRequest)
		return
	}

	if req.DelayMs <= 0 {
		req.DelayMs = 100 // Default delay
	}

	// Respond immediately to the client
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Message scheduled for relay to %s with %dms delay.\n", req.TargetURL, req.DelayMs)

	// Schedule the delayed forwarding in a new goroutine
	go delayedForward(req.Message, req.TargetURL, time.Duration(req.DelayMs)*time.Millisecond, defaultSleeper)
}

// delayedForward waits for the specified delay and then forwards the message.
func delayedForward(message, targetURL string, delay time.Duration, sleeper func(time.Duration)) {
	log.Printf("Scheduling message for %s with %v delay...", targetURL, delay)
	sleeper(delay) // Simulate temporal distortion/delay

	payload := map[string]string{"echo_message": message}
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		log.Printf("Error marshalling payload for %s: %v", targetURL, err)
		return
	}

	resp, err := http.Post(targetURL, "application/json", bytes.NewBuffer(jsonPayload))
	if err != nil {
		log.Printf("Error forwarding message to %s: %v", targetURL, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(resp.Body)
		log.Printf("Failed to forward message to %s. Status: %s, Body: %s", targetURL, resp.Status, string(body))
	} else {
		log.Printf("Successfully forwarded message to %s after %v delay.", targetURL, delay)
	}
}

func main() {
	http.HandleFunc("/relay", relayHandler)
	port := ":8080"
	log.Printf("Temporal Echo Relay listening on %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
