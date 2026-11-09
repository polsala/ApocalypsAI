package main

import (
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

// Config holds the application configuration
type Config struct {
	Port     int
	Interval time.Duration
}

// WhisperNetAggregator manages the UDP listener and whisper aggregation
type WhisperNetAggregator struct {
	config        Config
	whisperCh     chan string
	stopCh        chan struct{}
	wg            sync.WaitGroup
	listener      *net.UDPConn // For graceful shutdown
	mu            sync.Mutex   // Protects collectedWhispers
	collectedWhispers []string
}

// NewWhisperNetAggregator creates a new instance of the aggregator
func NewWhisperNetAggregator(cfg Config) *WhisperNetAggregator {
	return &WhisperNetAggregator{
		config:        cfg,
		whisperCh:     make(chan string, 100), // Buffered channel for whispers
		stopCh:        make(chan struct{}),
		collectedWhispers: make([]string, 0),
	}
}

// Start initializes and runs the aggregator service
func (w *WhisperNetAggregator) Start() error {
	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf(":%d", w.config.Port))
	if err != nil {
		return fmt.Errorf("failed to resolve UDP address: %w", err)
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		return fmt.Errorf("failed to listen on UDP port %d: %w", w.config.Port, err)
	}
	w.listener = conn
	log.Printf("WhisperNet Aggregator listening on UDP port %d, aggregating every %s...", w.config.Port, w.config.Interval)

	w.wg.Add(2) // Two goroutines: listener and aggregator
	go w.listenUDP()
	go w.aggregateWhispers()

	return nil
}

// Stop gracefully shuts down the aggregator service
func (w *WhisperNetAggregator) Stop() {
	log.Println("Shutting down WhisperNet Aggregator...")
	close(w.stopCh)
	if w.listener != nil {
		w.listener.Close() // Close the UDP listener
	}
	w.wg.Wait() // Wait for all goroutines to finish
	log.Println("WhisperNet Aggregator stopped.")
}

// listenUDP listens for incoming UDP messages and sends them to the whisper channel
func (w *WhisperNetAggregator) listenUDP() {
	defer w.wg.Done()
	buffer := make([]byte, 1024)

	for {
		select {
		case <-w.stopCh:
			return
		default:
			// Set a read deadline to allow checking stopCh
			w.listener.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
			n, _, err := w.listener.ReadFromUDP(buffer)
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Timeout, check stopCh again
				}
				if strings.Contains(err.Error(), "use of closed network connection") {
					return // Listener closed, graceful exit
				}
				// Log other errors, but don't stop the listener unless it's a fatal bind error
				// or the connection is explicitly closed.
				log.Printf("Warning: Error reading UDP: %v", err)
				continue
			}
			whisper := string(buffer[:n])
			select {
			case w.whisperCh <- whisper:
				// Whisper sent to channel
			case <-w.stopCh:
				return
			default:
				log.Println("Whisper channel full, dropping whisper.")
			}
		}
	}
}

// aggregateWhispers collects whispers over an interval and processes them
func (w *WhisperNetAggregator) aggregateWhispers() {
	defer w.wg.Done()
	ticker := time.NewTicker(w.config.Interval)
	defer ticker.Stop()

	for {
		select {
		case whisper := <-w.whisperCh:
			w.mu.Lock()
			w.collectedWhispers = append(w.collectedWhispers, whisper)
			w.mu.Unlock()
		case <-ticker.C:
			w.processCollectiveThought()
		case <-w.stopCh:
			// Process any remaining whispers before exiting
			w.processCollectiveThought()
			return
		}
	}
}

// processCollectiveThought takes collected whispers and forms a summary
func (w *WhisperNetAggregator) processCollectiveThought() {
	w.mu.Lock()
	defer w.mu.Unlock()

	if len(w.collectedWhispers) == 0 {
		// log.Println("No whispers collected in this interval.")
		return
	}

	// Whimsical aggregation: concatenate, or pick a random one, or count
	var collectiveThought string
	if len(w.collectedWhispers) == 1 {
		collectiveThought = fmt.Sprintf("A lone whisper echoed: \"%s\"", w.collectedWhispers[0])
	} else {
		// Simple concatenation for now, could be more complex
		collectiveThought = fmt.Sprintf("The collective consciousness stirred with %d whispers: \"%s\"",
			len(w.collectedWhispers), strings.Join(w.collectedWhispers, "\", \""))
	}

	log.Printf("[COLLECTIVE THOUGHT] %s\n", collectiveThought)
	w.collectedWhispers = make([]string, 0) // Reset for next interval
}

func main() {
	port := flag.Int("port", 8080, "The UDP port to listen on")
	intervalStr := flag.String("interval", "10s", "The duration to aggregate whispers (e.g., 5s, 1m)")
	flag.Parse()

	interval, err := time.ParseDuration(*intervalStr)
	if err != nil {
		log.Fatalf("Invalid interval duration: %v", err)
	}

	cfg := Config{
		Port:     *port,
		Interval: interval,
	}

	aggregator := NewWhisperNetAggregator(cfg)
	if err := aggregator.Start(); err != nil {
		log.Fatalf("Failed to start WhisperNet Aggregator: %v", err)
	}

	// Set up signal handling for graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// Block until a signal is received
	<-sigCh
	aggregator.Stop()
}
