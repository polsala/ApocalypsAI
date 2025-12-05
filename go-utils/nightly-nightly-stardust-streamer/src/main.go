package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

const (
	defaultPort = "8080"
	prefix      = "[Stardust Particle]"
)

// handleConnection processes incoming stardust particles from a connection.
// It reads lines, adds a prefix, and writes them to the provided logger.
func handleConnection(conn net.Conn, logger *log.Logger) {
	defer conn.Close()
	addr := conn.RemoteAddr().String()
	logger.Printf("New stardust stream from %s", addr)

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		particle := scanner.Text()
		processedParticle := fmt.Sprintf("%s %s (received from %s at %s)", prefix, particle, addr, time.Now().Format(time.RFC3339))
		logger.Println(processedParticle)
	}

	if err := scanner.Err(); err != nil && err != io.EOF {
		logger.Printf("Error reading from %s: %v", addr, err)
	}
	logger.Printf("Stardust stream from %s closed.", addr)
}

// startServer sets up and runs the stardust streamer server.
// It listens on the specified port and handles connections concurrently.
func startServer(port string, logger *log.Logger, wg *sync.WaitGroup, stopChan chan struct{}) {
	defer wg.Done()

	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		logger.Fatalf("Failed to listen on port %s: %v", port, err)
	}
	defer listener.Close()
	logger.Printf("Stardust Streamer listening on :%s", port)

	go func() {
		<-stopChan // Wait for stop signal
		logger.Println("Shutting down Stardust Streamer...")
		listener.Close() // Close the listener to stop accepting new connections
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			if strings.Contains(err.Error(), "use of closed network connection") {
				break // Listener was closed, graceful shutdown
			}
			logger.Printf("Error accepting connection: %v", err)
			continue
		}
		wg.Add(1) // Increment for each new connection handler
		go func() {
			handleConnection(conn, logger)
			wg.Done() // Decrement when handler finishes
		}()
	}
	logger.Println("Stardust Streamer stopped accepting new connections.")
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	// Setup logger to stdout
	logger := log.New(os.Stdout, "STREAMER: ", log.LstdFlags)

	var wg sync.WaitGroup
	stopChan := make(chan struct{}) // Channel to signal server to stop accepting new connections

	// Handle OS signals for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	wg.Add(1) // Add for the server goroutine itself
	go startServer(port, logger, &wg, stopChan)

	// Wait for interrupt signal
	<-sigChan
	logger.Println("Received shutdown signal. Initiating graceful shutdown...")

	close(stopChan) // Signal server to stop accepting new connections
	wg.Wait()       // Wait for all active connections and the server goroutine to finish
	logger.Println("All stardust streams processed. Stardust Streamer gracefully shut down.")
}
