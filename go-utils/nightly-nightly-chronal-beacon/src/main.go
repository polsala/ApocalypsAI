package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/google/uuid"
)

type ChronalSignature struct {
	ID        string    `json:"id"`
	Timestamp time.Time `json:"timestamp"`
}

func main() {
	beaconID := flag.String("id", uuid.New().String(), "Unique identifier for this beacon instance")
	intervalStr := flag.String("interval", "5s", "Broadcast interval (e.g., 1s, 500ms)")
	port := flag.Int("port", 9999, "UDP port for multicast")
	multicastAddr := flag.String("multicast-addr", "224.0.0.1", "Multicast IP address")
	flag.Parse()

	interval, err := time.ParseDuration(*intervalStr)
	if err != nil {
		log.Fatalf("Invalid interval format: %v", err)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Handle graceful shutdown
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-c
		log.Println("\nReceived shutdown signal, stopping beacon...")
		cancel()
	}()

	log.Printf("Starting Chronal Beacon (ID: %s) on udp://%s:%d with interval %s",
		*beaconID, *multicastAddr, *port, interval)

	if err := startBeacon(ctx, *beaconID, interval, *multicastAddr, *port); err != nil {
		log.Fatalf("Beacon failed: %v", err)
	}

	log.Println("Chronal Beacon stopped.")
}

func startBeacon(ctx context.Context, id string, interval time.Duration, multicastAddr string, port int) error {
	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf("%s:%d", multicastAddr, port))
	if err != nil {
		return fmt.Errorf("failed to resolve UDP address: %w", err)
	}

	conn, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		return fmt.Errorf("failed to dial UDP: %w", err)
	}
	defer conn.Close()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case <-ticker.C:
			signature := ChronalSignature{
				ID:        id,
				Timestamp: time.Now().UTC(),
			}
			msg, err := json.Marshal(signature)
			if err != nil {
				log.Printf("Error marshaling signature: %v", err)
				continue
			}

			_, err = conn.Write(msg)
			if err != nil {
				log.Printf("Error sending beacon: %v", err)
			}
			// log.Printf("Beacon sent: %s", msg) // Uncomment for verbose logging
		}
	}
}
