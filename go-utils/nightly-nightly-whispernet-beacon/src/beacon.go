package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"sync"
	"time"
)

// Beacon represents a single node in the WhisperNet network.
type Beacon struct {
	ID       string
	Port     int
	Peers    []string
	Messages chan string // Channel for incoming whispers
	Client   *http.Client // HTTP client for sending requests
	Server   *http.Server // HTTP server for receiving requests
}

// NewBeacon creates and initializes a new Beacon instance.
func NewBeacon(id string, port int, peers []string) *Beacon {
	beacon := &Beacon{
		ID:       id,
		Port:     port,
		Peers:    peers,
		Messages: make(chan string, 100), // Buffered channel for messages
		Client:   &http.Client{Timeout: 5 * time.Second},
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/whisper", beacon.handleWhisper)

	beacon.Server = &http.Server{
		Addr:    ":" + strconv.Itoa(port),
		Handler: mux,
	}

	return beacon
}

// StartServer starts the HTTP server for the beacon.
func (b *Beacon) StartServer() error {
	return b.Server.ListenAndServe()
}

// handleWhisper is the HTTP handler for incoming whisper messages.
func (b *Beacon) handleWhisper(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusInternalServerError)
		return
	}

	msg := string(body)
	select {
	case b.Messages <- msg:
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "Whisper received by %s", b.ID)
	case <-time.After(1 * time.Second): // Prevent blocking if channel is full
		log.Printf("[%s] Dropping whisper due to full message channel: %s", b.ID, msg)
		http.Error(w, "Message channel full, whisper dropped", http.StatusServiceUnavailable)
	}
}

// SendWhisper sends a message to a single target URL.
func (b *Beacon) SendWhisper(targetURL, message string) error {
	req, err := http.NewRequest(http.MethodPost, targetURL+"/whisper", bytes.NewBufferString(message))
	if err != nil {
		return fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("Content-Type", "text/plain")

	res, err := b.Client.Do(req)
	if err != nil {
		return fmt.Errorf("failed to send whisper to %s: %w", targetURL, err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		respBody, _ := io.ReadAll(res.Body)
		return fmt.Errorf("failed to send whisper to %s: received status %d, body: %s", targetURL, res.StatusCode, string(respBody))
	}

	log.Printf("[%s] Sent whisper to %s: %s", b.ID, targetURL, message)
	return nil
}

// BroadcastWhisper sends a message to all configured peers concurrently.
func (b *Beacon) BroadcastWhisper(message string) {
	if len(b.Peers) == 0 {
		log.Printf("[%s] No peers configured to broadcast whisper: %s", b.ID, message)
		return
	}

	var wg sync.WaitGroup
	for _, peer := range b.Peers {
		wg.Add(1)
		go func(p string) {
			defer wg.Done()
			if err := b.SendWhisper(p, message); err != nil {
				log.Printf("[%s] Error broadcasting whisper to %s: %v", b.ID, p, err)
			}
		}(peer)
	}
	wg.Wait()
}

// StartHeartbeat begins sending periodic status updates to peers.
func (b *Beacon) StartHeartbeat(interval time.Duration) {
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for range ticker.C {
		b.BroadcastStatus()
	}
}

// BroadcastStatus sends a predefined status message to all peers.
func (b *Beacon) BroadcastStatus() {
	statusMsg := fmt.Sprintf("Beacon %s is online at %s", b.ID, time.Now().Format(time.RFC3339))
	log.Printf("[%s] Broadcasting heartbeat: %s", b.ID, statusMsg)
	b.BroadcastWhisper(statusMsg)
}
