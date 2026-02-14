package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	defaultPort            = 8080
	bufferSize             = 1024
	duplicateWindow        = 5 * time.Second  // Time window to consider an echo a duplicate
	temporalDriftThreshold = 10 * time.Second // How far in future/past an echo can be
)

// EchoMessage represents a temporal echo received.
type EchoMessage struct {
	Timestamp time.Time
	MessageID string
	Payload   string
}

// EchoProcessor handles incoming echoes and detects anomalies.
type EchoProcessor struct {
	mu                  sync.Mutex
	recentEchoes        map[string]time.Time // messageID -> last received time
	driftThreshold      time.Duration
	duplicateWindow     time.Duration
	currentTimeProvider func() time.Time // For testability
}

// NewEchoProcessor creates a new EchoProcessor.
func NewEchoProcessor(driftThreshold, duplicateWindow time.Duration, currentTimeProvider func() time.Time) *EchoProcessor {
	if currentTimeProvider == nil {
		currentTimeProvider = time.Now
	}
	return &EchoProcessor{
		recentEchoes:        make(map[string]time.Time),
		driftThreshold:      driftThreshold,
		duplicateWindow:     duplicateWindow,
		currentTimeProvider: currentTimeProvider,
	}
}

// ParseEchoMessage parses a raw UDP message into an EchoMessage.
// Format: timestamp_ms|message_id|payload
func ParseEchoMessage(data []byte) (*EchoMessage, error) {
	parts := strings.SplitN(string(data), "|", 3)
	if len(parts) != 3 {
		return nil, fmt.Errorf("invalid echo message format: %s", string(data))
	}

	timestampMs, err := strconv.ParseInt(parts[0], 10, 64)
	if err != nil {
		return nil, fmt.Errorf("invalid timestamp: %s", parts[0])
	}
	timestamp := time.UnixMilli(timestampMs)

	return &EchoMessage{
		Timestamp: timestamp,
		MessageID: parts[1],
		Payload:   parts[2],
	},
}

// DetectAnomalies checks an EchoMessage for temporal drift and duplication.
func (ep *EchoProcessor) DetectAnomalies(echo *EchoMessage) {
	ep.mu.Lock()
	defer ep.mu.Unlock()

	now := ep.currentTimeProvider()

	// Temporal Drift Check
	timeDiff := now.Sub(echo.Timestamp)
	if timeDiff > ep.driftThreshold {
		log.Printf("[ANOMALY: Temporal Drift] Echo from the past detected: %s (received %s, sent %s, %s ago)",
			echo.MessageID, now.Format(time.RFC3339), echo.Timestamp.Format(time.RFC3339), timeDiff)
	} else if timeDiff < -ep.driftThreshold {
		log.Printf("[ANOMALY: Temporal Drift] Echo from the future detected: %s (received %s, sent %s, %s in the future)",
			echo.MessageID, now.Format(time.RFC3339), echo.Timestamp.Format(time.RFC3339), -timeDiff)
	}

	// Duplication Check
	if lastReceived, ok := ep.recentEchoes[echo.MessageID]; ok {
		if now.Sub(lastReceived) < ep.duplicateWindow {
			log.Printf("[ANOMALY: Echo Duplication] Duplicate echo detected for %s within %s (last received %s, now %s)",
				echo.MessageID, ep.duplicateWindow, lastReceived.Format(time.RFC3339), now.Format(time.RFC3339))
		}
	}
	ep.recentEchoes[echo.MessageID] = now
}

// runListener sets up and runs the UDP listener and echo processing.
func runListener(conn net.PacketConn, processor *EchoProcessor) {
	echoChan := make(chan *EchoMessage, 100) // Buffered channel for incoming echoes

	// Goroutine to read UDP packets
	go func() {
		buf := make([]byte, bufferSize)
		for {
			n, _, err := conn.ReadFrom(buf) // Use ReadFrom for PacketConn
			if err != nil {
				// Check if the error is due to the connection being closed
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					// Timeout, continue listening
					continue
				}
				if strings.Contains(err.Error(), "use of closed network connection") {
					log.Println("Listener shutting down due to closed connection.")
					close(echoChan) // Signal processor to stop
					return
				}
				log.Printf("Error reading UDP: %v", err)
				continue
			}
			echo, err := ParseEchoMessage(buf[:n])
			if err != nil {
				log.Printf("Failed to parse echo: %v", err)
				continue
			}
			echoChan <- echo
		}
	}()

	// Goroutine to process echoes
	for echo := range echoChan {
		processor.DetectAnomalies(echo)
	}
	log.Println("Echo processing goroutine stopped.")
}

func main() {
	portStr := os.Getenv("PORT")
	port := defaultPort
	if portStr != "" {
		p, err := strconv.Atoi(portStr)
		if err != nil {
			log.Fatalf("Invalid PORT environment variable: %v", err)
		}
		port = p
	}

	addr := net.UDPAddr{
		Port: port,
		IP:   net.ParseIP("0.0.0.0"),
	}

	conn, err := net.ListenUDP("udp", &addr)
	if err != nil {
		log.Fatalf("Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()

	log.Printf("ApocalypsAI Temporal Echo Listener active on UDP port %d. Awaiting whispers from the void...", port)

	processor := NewEchoProcessor(temporalDriftThreshold, duplicateWindow, nil)
	runListener(conn, processor)
}
