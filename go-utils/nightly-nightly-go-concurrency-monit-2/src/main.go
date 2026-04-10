package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"runtime"
	"sync"
	"time"
)

// MonitorState holds the current state of the concurrency monitor.
type MonitorState struct {
	GoroutineCount int `json:"goroutine_count"`
	ChannelOps     map[string]int `json:"channel_ops"` // e.g., "sends", "receives"
	StacksEnabled  bool `json:"stacks_enabled"`
	mu             sync.Mutex
}

var state = MonitorState{
	ChannelOps: make(map[string]int),
}

// ChannelOperation represents a channel operation.
type ChannelOperation string

const (
	SendOperation    ChannelOperation = "sends"
	ReceiveOperation ChannelOperation = "receives"
)

// recordChannelOperation increments the count for a given channel operation.
func recordChannelOperation(op ChannelOperation) {
	state.mu.Lock()
	defer state.mu.Unlock()
	state.ChannelOps[string(op)]++
}

// updateGoroutineCount periodically updates the Goroutine count.
func updateGoroutineCount() {
	for {
		state.mu.Lock()
		state.GoroutineCount = runtime.NumGoroutine()
		state.mu.Unlock()
		time.Sleep(2 * time.Second) // Update every 2 seconds
	}
}

// statusHandler handles requests to get the current monitor status.
func statusHandler(w http.ResponseWriter, r *http.Request) {
	state.mu.Lock()
	defer state.mu.Unlock()

	// Create a snapshot of the state for JSON marshaling
	currentState := struct {
		GoroutineCount int `json:"goroutine_count"`
		ChannelOps     map[string]int `json:"channel_ops"`
		StacksEnabled  bool `json:"stacks_enabled"`
	}{
		GoroutineCount: state.GoroutineCount,
		ChannelOps:     state.ChannelOps,
		StacksEnabled:  state.StacksEnabled,
	}

	w.Header().Set("Content-Type", "application/json")
	json.Enc := json.NewEncoder(w)
	if err := jsonEnc.Encode(currentState);
	err != nil {
		log.Printf("Error encoding status response: %v", err)
		http.Error(w, "Internal Server Error", http.StatusInternalServerError)
	}
}

// stacksEnableHandler enables Goroutine stack trace collection.
func stacksEnableHandler(w http.ResponseWriter, r *http.Request) {
	state.mu.Lock()
	state.StacksEnabled = true
	state.mu.Unlock()

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Goroutine stack traces enabled.\n")
	log.Println("Goroutine stack traces enabled.")
}

// stacksDisableHandler disables Goroutine stack trace collection.
func stacksDisableHandler(w http.ResponseWriter, r *http.Request) {
	state.mu.Lock()
	state.StacksEnabled = false
	state.mu.Unlock()

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "Goroutine stack traces disabled.\n")
	log.Println("Goroutine stack traces disabled.")
}

// mockChannelSender simulates sending data on a channel.
// In a real application, this would be part of your app's logic.
func mockChannelSender(ch chan<- string, data string, delay time.Duration) {
	time.Sleep(delay)
	ch <- data
	recordChannelOperation(SendOperation)
	log.Printf("Sent: %s\n", data)
}

// mockChannelReceiver simulates receiving data from a channel.
// In a real application, this would be part of your app's logic.
func mockChannelReceiver(ch <-chan string, delay time.Duration) {
	time.Sleep(delay)
	msg := <-ch
	recordChannelOperation(ReceiveOperation)
	log.Printf("Received: %s\n", msg)
}

func main() {
	// Start a Goroutine to periodically update the Goroutine count.
	go updateGoroutineCount()

	// Set up HTTP routes.
	http.HandleFunc("/status", statusHandler)
	http.HandleFunc("/stacks/enable", stacksEnableHandler)
	http.HandleFunc("/stacks/disable", stacksDisableHandler)

	// Start a dummy workload to demonstrate channel operations.
	go func() {
		msgChan := make(chan string, 5)
		for i := 0; i < 3; i++ {
			go mockChannelSender(msgChan, fmt.Sprintf("Message %d", i), time.Duration(i)*500*time.Millisecond)
			go mockChannelReceiver(msgChan, time.Duration(i+1)*500*time.Millisecond)
		}
		// Keep this Goroutine alive for a bit to allow messages to flow
		time.Sleep(3 * time.Second)
		close(msgChan)
	}()

	// Start the HTTP server.
	port := "8080"
	log.Printf("ApocalypsAI Concurrency Monitor listening on :%s\n", port)
	if err := http.ListenAndServe(":"+port, nil);
	err != nil {
		log.Fatalf("Server failed to start: %v\n", err)
	}
}
