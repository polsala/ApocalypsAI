package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	defaultPort          = "8080"
	defaultSimulatedLatencyMs = 100 // Default simulated network latency in milliseconds
)

// Config holds server configuration
type Config struct {
	Port             string
	SimulatedLatency time.Duration
	NowFunc          func() time.Time // For testability
}

// NewDefaultConfig creates a default server configuration, optionally overridden by environment variables.
func NewDefaultConfig() Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	simulatedLatencyMsStr := os.Getenv("SIMULATED_LATENCY_MS")
	simulatedLatencyMs := defaultSimulatedLatencyMs
	if simulatedLatencyMsStr != "" {
		if val, err := strconv.Atoi(simulatedLatencyMsStr); err == nil {
			simulatedLatencyMs = val
		} else {
			log.Printf("Warning: Invalid SIMULATED_LATENCY_MS environment variable '%s'. Using default %dms. Error: %v", simulatedLatencyMsStr, defaultSimulatedLatencyMs, err)
		}
	}

	return Config{
		Port:             port,
		SimulatedLatency: time.Duration(simulatedLatencyMs) * time.Millisecond,
		NowFunc:          time.Now,
	}
}

func main() {
	config := NewDefaultConfig()
	log.Printf("Starting Chrono-Drift Detector on port %s with simulated latency of %s...", config.Port, config.SimulatedLatency)

	listener, err := net.Listen("tcp", ":"+config.Port)
	if err != nil {
		log.Fatalf("Failed to listen: %v", err)
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Failed to accept connection: %v", err)
			continue
		}
		go func(c net.Conn) {
			defer c.Close()
			clientAddr := c.RemoteAddr().String()
			log.Printf("Client connected: %s", clientAddr)
			processClientRequest(c, c, config)
			log.Printf("Client disconnected: %s", clientAddr)
		}(conn)
	}
}

// processClientRequest handles a single client request, reading from r and writing to w.
// This function is designed to be easily testable by passing mock io.Reader and io.Writer.
func processClientRequest(r io.Reader, w io.Writer, config Config) {
	reader := bufio.NewReader(r)
	writer := bufio.NewWriter(w)

	// Read client's timestamp
	clientMessage, err := reader.ReadString('\n')
	if err != nil {
		writeResponse(writer, fmt.Sprintf("ERROR: Failed to read client message: %v\n", err))
		return
	}
	clientMessage = strings.TrimSpace(clientMessage)

	clientUnixNano, err := strconv.ParseInt(clientMessage, 10, 64)
	if err != nil {
		writeResponse(writer, fmt.Sprintf("ERROR: Invalid timestamp format. Send Unix nanoseconds. %v (received: '%s')\n", err, clientMessage))
		return
	}
	clientTime := time.Unix(0, clientUnixNano)

	// Get server's current time before applying simulated latency
	serverTimeBeforeLatency := config.NowFunc()

	// Simulate network latency (actual sleep happens here in the real server)
	time.Sleep(config.SimulatedLatency)

	// Get server's current time after applying simulated latency
	serverTimeAfterLatency := config.NowFunc()

	// Calculate drift: client's time minus server's time at the moment the message was *received*.
	// A positive drift means the client's clock is ahead of the server's.
	// We use serverTimeBeforeLatency for drift calculation as that's when the message arrived.
	drift := clientTime.Sub(serverTimeBeforeLatency)

	response := fmt.Sprintf("OK: Client Time: %s, Server Time (pre-latency): %s, Server Time (post-latency): %s, Clock Drift: %s, Simulated Latency: %s\n",
		clientTime.Format(time.RFC3339Nano),
		serverTimeBeforeLatency.Format(time.RFC3339Nano),
		serverTimeAfterLatency.Format(time.RFC3339Nano),
		drift,
		config.SimulatedLatency,
	)
	writeResponse(writer, response)
}

func writeResponse(writer *bufio.Writer, message string) {
	_, err := writer.WriteString(message)
	if err != nil {
		log.Printf("Error writing response: %v", err) // Log error, but don't fail the server
		return
	}
	err = writer.Flush()
	if err != nil {
		log.Printf("Error flushing writer: %v", err) // Log error
	}
}
