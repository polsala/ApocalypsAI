package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"time"
)

// sleepFunc is a variable that holds the function to simulate sleep. It defaults to time.Sleep
// but can be overridden for testing purposes to avoid actual time delays.
var sleepFunc = time.Sleep

// nowFunc is a variable that holds the function to get the current time. It defaults to time.Now
// but can be overridden for testing purposes to ensure deterministic timestamps.
var nowFunc = time.Now

func main() {
	port := flag.Int("port", 8080, "Port to listen on")
	delayStr := flag.String("delay", "5s", "Duration for starlight delay (e.g., 5s, 1m30s)")
	flag.Parse()

	delay, err := time.ParseDuration(*delayStr)
	if err != nil {
		log.Fatalf("Invalid delay duration: %v", err)
	}

	log.Printf("🚀 Starlight Signal Relay starting on port %d with a %s delay...", *port, delay)
	if err := startServer(*port, delay); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}

func startServer(port int, delay time.Duration) error {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		return fmt.Errorf("failed to listen: %w", err)
	}
	defer listener.Close()

	log.Printf("🌌 Listening for cosmic whispers on %s", listener.Addr().String())

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("⚠️ Failed to accept connection: %v", err)
			continue
		}
		go handleConnection(conn, delay)
	}
}

func handleConnection(conn net.Conn, delay time.Duration) {
	defer conn.Close()

	remoteAddr := conn.RemoteAddr().String()
	log.Printf("✨ New signal detected from %s", remoteAddr)

	reader := bufio.NewReader(conn)
	message, err := reader.ReadString('\n')
	// Trim newline and carriage return characters
	message = strings.TrimRight(message, "\r\n")

	if err != nil {
		if err != io.EOF {
			log.Printf("❌ Error reading signal from %s: %v", remoteAddr, err)
		}
		return
	}

	receivedAt := nowFunc()
	log.Printf("📥 Message received from %s at %s: '%s'", remoteAddr, receivedAt.Format(time.RFC3339), message)

	// Process the message with a starlight delay in a separate goroutine
	go func(msg string, rcvdAt time.Time) {
		sleepFunc(delay) // Simulate the cosmic journey
		relayedAt := nowFunc()
		logMessage(msg, rcvdAt, relayedAt, delay)
	}(message, receivedAt)
}

func logMessage(message string, receivedAt, relayedAt time.Time, delay time.Duration) {
	fmt.Printf("[%s] Starlight Relay: Message received at %s, traversing cosmic dust for %s... Relayed at %s: '%s'\n",
		relayedAt.Format("2006-01-02 15:04:05"),
		receivedAt.Format("2006-01-02 15:04:05"),
		delay,
		relayedAt.Format("2006-01-02 15:04:05"),
		message,
	)
}
