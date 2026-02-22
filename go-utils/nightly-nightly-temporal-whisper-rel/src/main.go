package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

const (
	defaultPort     = "8080"
	defaultMinDelay = 100 * time.Millisecond
	defaultMaxDelay = 500 * time.Millisecond
)

// Message represents a message received from a client.
type Message struct {
	Sender  net.Conn
	Content string
}

// TemporalWhisperRelay manages client connections and message broadcasting.
type TemporalWhisperRelay struct {
	listener     net.Listener
	clients      map[net.Conn]struct{} // Using struct{} for a set
	clientsMutex sync.Mutex
	messages     chan Message
	broadcast    chan Message
	shutdown     chan struct{}
	minDelay     time.Duration
	maxDelay     time.Duration
	randSource   rand.Source
}

// NewTemporalWhisperRelay creates a new relay instance.
func NewTemporalWhisperRelay(port string, minDelay, maxDelay time.Duration) (*TemporalWhisperRelay, error) {
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		return nil, fmt.Errorf("failed to listen on port %s: %w", port, err)
	}

	log.Printf("Temporal Whisper Relay listening on :%s with delay range %s-%s", port, minDelay, maxDelay)

	return &TemporalWhisperRelay{
		listener:     listener,
		clients:      make(map[net.Conn]struct{}),
		messages:     make(chan Message, 100), // Buffered channel for messages
		broadcast:    make(chan Message, 100), // Buffered channel for broadcasts
		shutdown:     make(chan struct{}),
		minDelay:     minDelay,
		maxDelay:     maxDelay,
		randSource:   rand.NewSource(time.Now().UnixNano()), // Seed for random delays
	}, nil
}

// Start begins accepting connections and processing messages.
func (twr *TemporalWhisperRelay) Start() {
	go twr.acceptConnections()
	go twr.processMessages()
	go twr.broadcastMessages()
}

// Stop shuts down the relay gracefully.
func (twr *TemporalWhisperRelay) Stop() {
	log.Println("Shutting down Temporal Whisper Relay...")
	close(twr.shutdown)
	// Close the listener to unblock acceptConnections
	if err := twr.listener.Close(); err != nil {
		log.Printf("Error closing listener: %v", err)
	}

	// Close all client connections
	twr.clientsMutex.Lock()
	for client := range twr.clients {
		client.Close()
	}
	twr.clients = make(map[net.Conn]struct{}) // Clear the map
	twr.clientsMutex.Unlock()

	// Give some time for goroutines to finish processing remaining messages
	// In a more robust system, a sync.WaitGroup would be used here.
	time.Sleep(200 * time.Millisecond)
	log.Println("Temporal Whisper Relay stopped.")
}

func (twr *TemporalWhisperRelay) acceptConnections() {
	for {
		conn, err := twr.listener.Accept()
		if err != nil {
			select {
			case <-twr.shutdown:
				return // Server is shutting down
			default:
				// Log error unless it's a 'use of closed network connection' error during shutdown
				if !strings.Contains(err.Error(), "use of closed network connection") {
					log.Printf("Error accepting connection: %v", err)
				}
			}
			continue
		}
		log.Printf("New client connected: %s", conn.RemoteAddr())
		twr.addClient(conn)
		go twr.handleConnection(conn)
	}
}

func (twr *TemporalWhisperRelay) addClient(conn net.Conn) {
	twr.clientsMutex.Lock()
	defer twr.clientsMutex.Unlock()
	twr.clients[conn] = struct{}{} // Add to set
}

func (twr *TemporalWhisperRelay) removeClient(conn net.Conn) {
	twr.clientsMutex.Lock()
	defer twr.clientsMutex.Unlock()
	delete(twr.clients, conn)
	conn.Close()
	log.Printf("Client disconnected: %s", conn.RemoteAddr())
}

func (twr *TemporalWhisperRelay) handleConnection(conn net.Conn) {
	defer twr.removeClient(conn)
	reader := bufio.NewReader(conn)

	for {
		select {
		case <-twr.shutdown:
			return
		default:
			// Set a read deadline to prevent indefinite blocking and allow shutdown check
			conn.SetReadDeadline(time.Now().Add(1 * time.Second))
			message, err := reader.ReadString('\n')
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Timeout, check shutdown channel again
				}
				// EOF or other read error, client disconnected
				return
			}
			message = strings.TrimSpace(message)
			if message == "" {
				continue
			}
			log.Printf("Received from %s: %s", conn.RemoteAddr(), message)
			twr.messages <- Message{Sender: conn, Content: message}
		}
	}
}

func (twr *TemporalWhisperRelay) processMessages() {
	// Use a local rand.Rand for goroutine-safe random number generation
	r := rand.New(twr.randSource)

	for {
		select {
		case <-twr.shutdown:
			return
		case msg := <-twr.messages:
			delay := twr.minDelay + time.Duration(r.Int63n(int64(twr.maxDelay-twr.minDelay+1)))
			log.Printf("Scheduling broadcast of '%s' with delay %s", msg.Content, delay)
			go func(m Message, d time.Duration) {
				time.Sleep(d)
				twr.broadcast <- m
			}(msg, delay)
		}
	}
}

func (twr *TemporalWhisperRelay) broadcastMessages() {
	for {
		select {
		case <-twr.shutdown:
			return
		case msg := <-twr.broadcast:
			// Acquire lock only for iterating over clients
			twr.clientsMutex.Lock()
			// Create a slice of active clients to avoid holding the lock during writes
			activeClients := make([]net.Conn, 0, len(twr.clients))
			for client := range twr.clients {
				if client != msg.Sender { // Don't send back to the sender
					activeClients = append(activeClients, client)
				}
			}
			twr.clientsMutex.Unlock()

			// Send to active clients outside the lock
			for _, client := range activeClients {
				_, err := client.Write([]byte(fmt.Sprintf("Echo from the past (%s): %s\n", msg.Sender.RemoteAddr(), msg.Content)))
				if err != nil {
					log.Printf("Error sending to client %s: %v", client.RemoteAddr(), err)
					// Consider removing client here if write fails persistently
					twr.removeClient(client) // Attempt to remove problematic client
				}
			}
			log.Printf("Broadcasted '%s' to %d other clients.", msg.Content, len(activeClients))
		}
	}
}

func main() {
	port := flag.String("port", defaultPort, "Port to listen on")
	minDelayStr := flag.String("min-delay", defaultMinDelay.String(), "Minimum delay for echoes (e.g., 100ms, 1s)")
	maxDelayStr := flag.String("max-delay", defaultMaxDelay.String(), "Maximum delay for echoes (e.g., 500ms, 5s)")
	flag.Parse()

	minDelay, err := time.ParseDuration(*minDelayStr)
	if err != nil {
		log.Fatalf("Invalid min-delay duration: %v", err)
	}
	maxDelay, err := time.ParseDuration(*maxDelayStr)
	if err != nil {
		log.Fatalf("Invalid max-delay duration: %v", err)
	}
	if minDelay > maxDelay {
		log.Fatalf("min-delay (%s) cannot be greater than max-delay (%s)", minDelay, maxDelay)
	}

	relay, err := NewTemporalWhisperRelay(*port, minDelay, maxDelay)
	if err != nil {
		log.Fatalf("Failed to create relay: %v", err)
	}

	relay.Start()

	// Handle OS signals for graceful shutdown
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	<-c // Block until a signal is received

	relay.Stop()
}
