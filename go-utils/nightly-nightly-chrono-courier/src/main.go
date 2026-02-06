package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
)

// RelayRequest defines the structure of the incoming request
type RelayRequest struct {
	DestinationURL string          `json:"destination_url"`
	MessageBody    json.RawMessage `json:"message_body"`
	DelaySeconds   int             `json:"delay_seconds"`
}

// CourierService holds the HTTP client for relaying messages
type CourierService struct {
	client *http.Client
}

// NewCourierService creates a new CourierService
func NewCourierService(client *http.Client) *CourierService {
	if client == nil {
		client = &http.Client{Timeout: 30 * time.Second}
	}
	return &CourierService{client: client}
}

// handleRelay receives a message, schedules its delayed delivery
func (cs *CourierService) handleRelay(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is supported", http.StatusMethodNotAllowed)
		return
	}

	var req RelayRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, fmt.Sprintf("Invalid request body: %v", err), http.StatusBadRequest)
		return
	}

	if req.DestinationURL == "" {
		http.Error(w, "destination_url is required", http.StatusBadRequest)
		return
	}
	if req.MessageBody == nil {
		http.Error(w, "message_body is required", http.StatusBadRequest)
		return
	}

	delay := req.DelaySeconds
	if delay == 0 {
		defaultDelayStr := os.Getenv("DEFAULT_DELAY_SECONDS")
		if defaultDelayStr != "" {
			parsedDelay, parseErr := strconv.Atoi(defaultDelayStr)
			if parseErr == nil && parsedDelay > 0 {
				delay = parsedDelay
			}
		}
		if delay == 0 { // Fallback to hardcoded default if env var is missing or invalid
			delay = 5 // Default to 5 seconds
		}
	}

	log.Printf("Received message for %s with delay %d seconds. Scheduling delivery...", req.DestinationURL, delay)

	// Schedule the delivery in a new goroutine
	go cs.deliverMessage(req.DestinationURL, req.MessageBody, time.Duration(delay)*time.Second)

	w.WriteHeader(http.StatusAccepted)
	fmt.Fprintf(w, "Message received and scheduled for delivery to %s in %d seconds.\n", req.DestinationURL, delay)
}

// deliverMessage waits for the specified delay and then sends the message
func (cs *CourierService) deliverMessage(destinationURL string, messageBody json.RawMessage, delay time.Duration) {
	time.Sleep(delay)

	log.Printf("Delivering message to %s after %s delay...", destinationURL, delay)

	reqBody := bytes.NewBuffer(messageBody)
	req, err := http.NewRequest(http.MethodPost, destinationURL, reqBody)
	if err != nil {
		log.Printf("Error creating relay request for %s: %v", destinationURL, err)
		return
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := cs.client.Do(req)
	if err != nil {
		log.Printf("Error relaying message to %s: %v", destinationURL, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 400 {
		log.Printf("Failed to relay message to %s. Status: %s", destinationURL, resp.Status)
	} else {
		log.Printf("Successfully relayed message to %s. Status: %s", destinationURL, resp.Status)
	}
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	courierService := NewCourierService(nil) // Use default http.Client

	http.HandleFunc("/relay", courierService.handleRelay)

	log.Printf("Nightly Chrono-Courier starting on :%s", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
