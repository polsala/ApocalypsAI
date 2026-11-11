package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"time"
)

func main() {
	var id string
	var port int
	var peersStr string
	var heartbeatIntervalStr string

	flag.StringVar(&id, "id", "", "Unique identifier for this beacon")
	flag.IntVar(&port, "port", 8080, "Port for this beacon to listen on")
	flag.StringVar(&peersStr, "peers", "", "Comma-separated list of peer beacon URLs (e.g., http://localhost:8081,http://localhost:8082)")
	flag.StringVar(&heartbeatIntervalStr, "heartbeat-interval", "10s", "Interval for sending heartbeats (e.g., 5s, 1m)")
	flag.Parse()

	if id == "" {
		log.Fatal("Beacon ID is required. Use -id flag.")
	}

	peers := []string{}
	if peersStr != "" {
		peers = strings.Split(peersStr, ",")
	}

	heartbeatInterval, err := time.ParseDuration(heartbeatIntervalStr)
	if err != nil {
		log.Fatalf("Invalid heartbeat interval format: %v", err)
	}

	beacon := NewBeacon(id, port, peers)

	// Start HTTP server in a goroutine
	go func() {
		log.Printf("Beacon %s starting HTTP server on :%d", beacon.ID, beacon.Port)
		if err := beacon.StartServer(); err != nil {
			log.Fatalf("Beacon %s server failed: %v", beacon.ID, err)
		}
	}()

	// Start periodic heartbeats in a goroutine
	go beacon.StartHeartbeat(heartbeatInterval)

	// Listen for incoming messages and print them
	for msg := range beacon.Messages {
		log.Printf("[%s] Received whisper: %s", beacon.ID, msg)
	}
}
