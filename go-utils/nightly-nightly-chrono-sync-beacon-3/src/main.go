package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"time"
)

// BeaconMessage represents the time signal sent to clients.
type BeaconMessage struct {
	Timestamp string `json:"timestamp"`
	Source    string `json:"source"`
}

// handleClient manages a single client connection, sending time signals periodically.
func handleClient(conn net.Conn, interval time.Duration) {
	defer conn.Close()
	log.Printf("Client connected from %s", conn.RemoteAddr())

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	encoder := json.NewEncoder(conn)

	for range ticker.C {
		msg := BeaconMessage{
			Timestamp: time.Now().UTC().Format(time.RFC3339Nano),
			Source:    "ApocalypsAI Chrono-Sync Beacon",
		}
		if err := encoder.Encode(msg); err != nil {
			log.Printf("Error sending message to %s: %v", conn.RemoteAddr(), err)
			return // Client disconnected or error
		}
		// log.Printf("Sent time signal to %s: %s", conn.RemoteAddr(), msg.Timestamp) // Commented out for less verbose logs
	}
}

// runServer starts the TCP listener and accepts client connections.
// It listens for context cancellation to shut down gracefully.
func runServer(ctx context.Context, port int, interval time.Duration) error {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		return fmt.Errorf("failed to start listener on port %d: %v", port, err)
	}
	defer listener.Close() // Ensure listener is closed when runServer exits

	log.Printf("Chrono-Sync Beacon listening on port %d, sending signals every %s", port, interval)

	go func() {
		<-ctx.Done() // Wait for context cancellation
		log.Println("Server context cancelled, shutting down listener.")
		listener.Close() // Close the listener to unblock Accept()
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			select {
			case <-ctx.Done():
				// Listener closed due to context cancellation, expected error
				return nil
			default:
				log.Printf("Error accepting connection: %v", err)
				// If it's a temporary network error, wait a bit before retrying
				if opErr, ok := err.(*net.OpError); ok && opErr.Temporary() {
					time.Sleep(100 * time.Millisecond)
					continue
				}
				return fmt.Errorf("unrecoverable error accepting connection: %v", err)
			}
		}
		go handleClient(conn, interval)
	}
}

func main() {
	portStr := os.Getenv("PORT")
	if portStr == "" {
		portStr = "8080" // Default port
	}
	port, err := strconv.Atoi(portStr)
	if err != nil {
		log.Fatalf("Invalid PORT environment variable: %v", err)
	}

	intervalStr := os.Getenv("INTERVAL_SECONDS")
	if intervalStr == "" {
		intervalStr = "1" // Default to 1 second
	}
	intervalSecs, err := strconv.Atoi(intervalStr)
	if err != nil {
		log.Fatalf("Invalid INTERVAL_SECONDS environment variable: %v", err)
	}
	interval := time.Duration(intervalSecs) * time.Second

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	if err := runServer(ctx, port, interval); err != nil {
		log.Fatalf("Server error: %v", err)
	}
}
