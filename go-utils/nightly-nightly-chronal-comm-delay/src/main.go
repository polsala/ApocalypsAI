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

// DelayGenerator is a function type for generating a time.Duration delay.
// This allows mocking in tests.
type DelayGenerator func(min, max int) time.Duration

// defaultDelayGenerator provides a random delay within the specified range.
func defaultDelayGenerator(min, max int) time.Duration {
	if min > max {
		min, max = max, min // Ensure min is not greater than max
	}
	if min < 0 {
		min = 0 // Delays should not be negative
	}

	delayMs := rand.Intn(max-min+1) + min
	return time.Duration(delayMs) * time.Millisecond
}

// Server holds the state for the Chronal Comm Delay server.
type Server struct {
	listener     net.Listener
	clients      map[net.Conn]struct{}
	mu           sync.Mutex
	messages     chan string
	delayMinMs   int
	delayMaxMs   int
	delayGen     DelayGenerator
	wg           sync.WaitGroup
	shutdownChan chan struct{}
}

// NewServer creates and initializes a new Server instance.
func NewServer(port, minDelayMs, maxDelayMs int, delayGen DelayGenerator) *Server {
	if delayGen == nil {
		delayGen = defaultDelayGenerator
	}

	s := &Server{
		clients:      make(map[net.Conn]struct{}),
		messages:     make(chan string, 100), // Buffered channel for incoming messages
		delayMinMs:   minDelayMs,
		delayMaxMs:   maxDelayMs,
		delayGen:     delayGen,
		shutdownChan: make(chan struct{}),
	}

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	return s
}

// Start begins listening for connections and processing messages.
func (s *Server) Start(port int) error {
	addr := fmt.Sprintf(":%d", port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return fmt.Errorf("failed to listen on %s: %w", addr, err)
	}
	s.listener = listener
	log.Printf("Chronal Comm Delay server listening on %s (delay: %d-%dms)", addr, s.delayMinMs, s.delayMaxMs)

	s.wg.Add(1)
	go s.acceptConnections()

	s.wg.Add(1)
	go s.processMessages()

	return nil
}

// acceptConnections continuously accepts new client connections.
func (s *Server) acceptConnections() {
	defer s.wg.Done()

	for {
		conn, err := s.listener.Accept()
		if err != nil {
			select {
			case <-s.shutdownChan:
				return // Server is shutting down
			default:
				log.Printf("Error accepting connection: %v", err)
			}
			continue
		}

		log.Printf("New client connected: %s", conn.RemoteAddr())
		s.addClient(conn)

		s.wg.Add(1)
		go s.handleClient(conn)
	}
}

// handleClient reads messages from a client and sends them to the messages channel.
func (s *Server) handleClient(conn net.Conn) {
	defer s.wg.Done()
	defer s.removeClient(conn)

	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			log.Printf("Client %s disconnected or error: %v", conn.RemoteAddr(), err)
			return
		}

		message = strings.TrimSpace(message)
		if message != "" {
			log.Printf("Received from %s: %s", conn.RemoteAddr(), message)
			s.messages <- fmt.Sprintf("[%s] %s", conn.RemoteAddr(), message)
		}
	}
}

// processMessages takes messages from the channel, applies a delay, and then broadcasts them.
func (s *Server) processMessages() {
	defer s.wg.Done()

	for {
		select {
		case msg := <-s.messages:
			delay := s.delayGen(s.delayMinMs, s.delayMaxMs)
			log.Printf("Scheduling broadcast for '%s' with delay %v", msg, delay)
			time.Sleep(delay)
			s.broadcastMessage(msg)
		case <-s.shutdownChan:
			return
		}
	}
}

// broadcastMessage sends a message to all connected clients.
func (s *Server) broadcastMessage(message string) {
	s.mu.Lock()
	defer s.mu.Unlock()

	log.Printf("Broadcasting: %s", message)
	for clientConn := range s.clients {
		_, err := clientConn.Write([]byte(message + "\n"))
		if err != nil {
			log.Printf("Error sending to client %s: %v", clientConn.RemoteAddr(), err)
			// Consider removing client here if write fails, but handleClient already does this on read error.
		}
	}
}

// addClient adds a connection to the active clients map.
func (s *Server) addClient(conn net.Conn) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.clients[conn] = struct{}{}
}

// removeClient removes a connection from the active clients map and closes it.
func (s *Server) removeClient(conn net.Conn) {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.clients, conn)
	conn.Close()
	log.Printf("Client %s removed.", conn.RemoteAddr())
}

// Shutdown gracefully stops the server.
func (s *Server) Shutdown() {
	log.Println("Shutting down server...")
	close(s.shutdownChan) // Signal goroutines to stop

	if s.listener != nil {
		s.listener.Close() // This will cause acceptConnections to return an error
	}

	s.wg.Wait() // Wait for all goroutines to finish

	s.mu.Lock()
	defer s.mu.Unlock()
	for conn := range s.clients {
		conn.Close() // Close all remaining client connections
	}
	log.Println("Server shutdown complete.")
}

func main() {
	port := flag.Int("port", 8080, "The TCP port to listen on")
	minDelay := flag.Int("min-delay", 1000, "Minimum delay in milliseconds before broadcasting a message")
	maxDelay := flag.Int("max-delay", 5000, "Maximum delay in milliseconds before broadcasting a message")
	flag.Parse()

	if *minDelay < 0 || *maxDelay < 0 {
		log.Fatalf("Delay values cannot be negative. Got min: %d, max: %d", *minDelay, *maxDelay)
	}
	if *minDelay > *maxDelay {
		log.Fatalf("Min delay (%dms) cannot be greater than max delay (%dms)", *minDelay, *maxDelay)
	}

	server := NewServer(*port, *minDelay, *maxDelay, nil) // Use default delay generator

	err := server.Start(*port)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	<-sigChan // Block until a signal is received
	server.Shutdown()
}
