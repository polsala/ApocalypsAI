package main

import (
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"strings"
	"time"
)

const (
	multicastAddr     = "224.0.0.1:9000" // Standard multicast address
	broadcastInterval = 5 * time.Second
)

var whimsicalPhrases = []string{
	"The cosmic clock ticks, marking the current epoch:",
	"A temporal ripple confirms the true time:",
	"The void whispers the precise moment:",
	"Synchronize your chronometers to the celestial hum:",
	"Behold, the unyielding march of time:",
	"The fabric of reality aligns to this temporal marker:",
}

func init() {
	rand.Seed(time.Now().UnixNano()) // Seed for randomness, called once at package init
}

// getRandomWhimsicalMessage generates a random whimsical message with the given timestamp.
func getRandomWhimsicalMessage(t time.Time) string {
	phrase := whimsicalPhrases[rand.Intn(len(whimsicalPhrases))]
	return fmt.Sprintf("%s %s", phrase, t.Format(time.RFC3339))
}

// runServer starts the Chrono-Sync Beacon server.
// It broadcasts the current time wrapped in a whimsical message to a multicast address.
func runServer(conn net.PacketConn) {
	log.Printf("Chrono-Sync Beacon Server starting on %s...", multicastAddr)
	ticker := time.NewTicker(broadcastInterval)
	defer ticker.Stop()

	addr, err := net.ResolveUDPAddr("udp", multicastAddr)
	if err != nil {
		log.Fatalf("Error resolving multicast address: %v", err)
	}

	for range ticker.C {
		currentTime := time.Now().UTC()
		message := getRandomWhimsicalMessage(currentTime)

		_, err := conn.WriteTo([]byte(message), addr)
		if err != nil {
			log.Printf("Error sending broadcast: %v", err)
		} else {
			log.Printf("Broadcasted: \"%s\"", message)
		}
	}
}

// runClient starts the Chrono-Sync Beacon client.
// It listens for multicast time broadcasts and prints the synchronized time.
func runClient(conn net.PacketConn) {
	log.Printf("Chrono-Sync Beacon Client listening on %s...", multicastAddr)

	buffer := make([]byte, 1024)
	for {
		n, _, err := conn.ReadFrom(buffer)
		if err != nil {
			// If the connection is closed, ReadFrom might return an error.
			// For a long-running client, we'd typically handle specific errors or use a context.
			log.Printf("Error reading from connection: %v", err)
			continue
		}

		receivedMessage := string(buffer[:n])
		log.Printf("Received: \"%s\"", receivedMessage)

		// Attempt to parse the time from the message
		parts := strings.Split(receivedMessage, " ")
		if len(parts) > 0 {
			// Find the last part that looks like a timestamp
			for i := len(parts) - 1; i >= 0; i-- {
				if t, err := time.Parse(time.RFC3339, parts[i]); err == nil {
					log.Printf("  Synchronized Time: %s (UTC)", t.Format(time.RFC3339))
					break
				}
			}
		}
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-chrono-sync-beacon <server|client>")
		os.Exit(1)
	}

	mode := os.Args[1]

	// Resolve UDP address for multicast
	addr, err := net.ResolveUDPAddr("udp", multicastAddr)
	if err != nil {
		log.Fatalf("Error resolving UDP address: %v", err)
	}

	// Create a UDP connection for multicast. nil for laddr means listen on all available interfaces.
	conn, err := net.ListenMulticastUDP("udp", nil, addr)
	if err != nil {
		log.Fatalf("Error listening for multicast: %v", err)
	}
	defer conn.Close()

	// Set a reasonable buffer size for the UDP connection
	if err := conn.SetReadBuffer(1024 * 1024); err != nil {
		log.Printf("Warning: Failed to set read buffer size: %v", err)
	}
	if err := conn.SetWriteBuffer(1024 * 1024); err != nil {
		log.Printf("Warning: Failed to set write buffer size: %v", err)
	}


	switch mode {
	case "server":
		runServer(conn)
	case "client":
		runClient(conn)
	default:
		fmt.Println("Invalid mode. Usage: nightly-chrono-sync-beacon <server|client>")
		os.Exit(1)
	}
}
