package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	defaultPort = 8080
	syncCommand = "SYNC"
)

// Server represents the Chrono-Sync Beacon server.
type Server struct {
	port int
	listener net.Listener
	mu       sync.Mutex // Protects server state if it were more complex
	running  bool
	wg       sync.WaitGroup
}

// NewServer creates a new Server instance.
func NewServer(port int) *Server {
	return &Server{
		port: port,
		running: false,
	}
}

// Start begins listening for incoming connections.
func (s *Server) Start() error {
	s.mu.Lock()
	if s.running {
		s.mu.Unlock()
		return fmt.Errorf("server is already running on port %d", s.port)
	}
	s.running = true
	s.mu.Unlock()

	addr := fmt.Sprintf(":%d", s.port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		s.mu.Lock()
		s.running = false // Mark as not running if listen fails
		s.mu.Unlock()
		return fmt.Errorf("failed to listen on %s: %w", addr, err)
	}
	s.listener = listener
	log.Printf("Chrono-Sync Beacon listening on %s", addr)

	s.wg.Add(1)
	go s.acceptConnections()

	return nil
}

// Stop closes the server listener and waits for active goroutines to finish.
func (s *Server) Stop() {
	s.mu.Lock()
	if !s.running {
		s.mu.Unlock()
		return
	}
	s.running = false
	s.mu.Unlock()

	if s.listener != nil {
		log.Println("Stopping Chrono-Sync Beacon...")
		s.listener.Close() // This will unblock the acceptConnections goroutine
	}
	s.wg.Wait() // Wait for all connection handlers to finish
	log.Println("Chrono-Sync Beacon stopped.")
}

// acceptConnections continuously accepts new client connections.
func (s *Server) acceptConnections() {
	defer s.wg.Done()
	for {
		conn, err := s.listener.Accept()
		if err != nil {
			s.mu.Lock()
			if !s.running { // If server is intentionally stopped, this is expected
				s.mu.Unlock()
				return
			}
			s.mu.Unlock()
			log.Printf("Error accepting connection: %v", err)
			continue
		}
		s.wg.Add(1)
		go s.handleConnection(conn)
	}
}

// handleConnection processes a single client connection.
func (s *Server) handleConnection(conn net.Conn) {
	defer s.wg.Done()
	defer conn.Close()

	log.Printf("Client connected: %s", conn.RemoteAddr())
	reader := bufio.NewReader(conn)

	for {
		conn.SetReadDeadline(time.Now().Add(5 * time.Minute)) // Set a read deadline to prevent indefinite blocking
		message, err := reader.ReadString('\n')
		if err != nil {
			log.Printf("Client %s disconnected or error reading: %v", conn.RemoteAddr(), err)
			return
		}

		command := strings.TrimSpace(message)
		log.Printf("Received command from %s: '%s'", conn.RemoteAddr(), command)

		switch command {
		case syncCommand:
			// Provide the current UTC time in RFC3339Nano format
			currentTime := time.Now().UTC().Format(time.RFC3339Nano)
			response := fmt.Sprintf("%s\n", currentTime)
			_, err := conn.Write([]byte(response))
			if err != nil {
				log.Printf("Error writing response to %s: %v", conn.RemoteAddr(), err)
				return
			}
			log.Printf("Sent sync time to %s: %s", conn.RemoteAddr(), currentTime)
		default:
			response := fmt.Sprintf("UNKNOWN_COMMAND: %s\n", command)
			_, err := conn.Write([]byte(response))
			if err != nil {
				log.Printf("Error writing error response to %s: %v", conn.RemoteAddr(), err)
				return
			}
			log.Printf("Sent error for unknown command to %s: %s", conn.RemoteAddr(), command)
		}
	}
}

func main() {
	portPtr := flag.Int("port", defaultPort, "Port to listen on")
	flag.Parse()

	server := NewServer(*portPtr)
	if err := server.Start(); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}

	// Keep the main goroutine alive until an interrupt signal is received
	// For a production daemon, uncomment signal handling:
	// sigChan := make(chan os.Signal, 1)
	// signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	// <-sigChan // Block until a signal is received

	// For this utility, we'll block indefinitely or rely on external process management
	// to terminate, allowing tests to control server lifecycle directly.
	select{}

	// server.Stop() // This would be called after receiving a signal
}
