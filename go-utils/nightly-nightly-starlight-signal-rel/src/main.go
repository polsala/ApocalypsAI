package main

import (
	"bufio"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	defaultPort = "8080"
)

// Client represents a connected client
type Client struct {
	conn net.Conn
	id   string
}

// Server holds the server state
type Server struct {
	clients    map[string]Client
	mu         sync.Mutex
	broadcast  chan string
	listener   net.Listener
	wg         sync.WaitGroup
	running    bool
	port       string
}

// NewServer creates a new Server instance
func NewServer(port string) *Server {
	return &Server{
		clients:   make(map[string]Client),
		broadcast: make(chan string),
		running:   false,
		port:      port,
	}
}

// Start begins listening for incoming connections
func (s *Server) Start() error {
	var err error
	s.listener, err = net.Listen("tcp", ":"+s.port)
	if err != nil {
		return fmt.Errorf("failed to listen on port %s: %w", s.port, err)
	}
	s.running = true
	log.Printf("Starlight Signal Relay listening on port %s...", s.port)

	s.wg.Add(1)
	go s.handleBroadcasts()

	s.wg.Add(1)
	go func() {
		defer s.wg.Done()
		for s.running {
			conn, err := s.listener.Accept()
			if err != nil {
				if !s.running { // Server was intentionally shut down
					return
				}
				log.Printf("Error accepting connection: %v", err)
				continue
			}
			s.wg.Add(1)
			go s.handleClient(conn)
		}
	}()
	return nil
}

// Stop shuts down the server
func (s *Server) Stop() {
	// Signal that the server is no longer running
	s.running = false
	// Close the listener to unblock Accept()
	if s.listener != nil {
		s.listener.Close()
	}
	// Close the broadcast channel to signal handleBroadcasts to exit
	close(s.broadcast)
	// Wait for all goroutines to finish
	s.wg.Wait()
	log.Println("Starlight Signal Relay stopped.")
}

// handleClient manages a single client connection
func (s *Server) handleClient(conn net.Conn) {
	defer s.wg.Done()
	defer conn.Close()

	clientID := conn.RemoteAddr().String()
	log.Printf("New client connected: %s", clientID)

	s.mu.Lock()
	s.clients[clientID] = Client{conn: conn, id: clientID}
	s.mu.Unlock()

	// Announce new client
	s.broadcast <- fmt.Sprintf("[Starlight Signal] %s has joined the relay.", clientID)

	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			log.Printf("Client %s disconnected or error: %v", clientID, err)
			break
		}

		processedMessage := s.processMessage(clientID, strings.TrimSpace(message))
		s.broadcast <- processedMessage
	}

	s.mu.Lock()
	delete(s.clients, clientID)
	s.mu.Unlock()
	log.Printf("Client %s disconnected.", clientID)
	// Announce client departure
	s.broadcast <- fmt.Sprintf("[Starlight Signal] %s has left the relay.", clientID)
}

// handleBroadcasts sends messages to all connected clients
func (s *Server) handleBroadcasts() {
	defer s.wg.Done()
	for msg := range s.broadcast {
		s.mu.Lock()
		for _, client := range s.clients {
			_, err := client.conn.Write([]byte(msg + "\n"))
			if err != nil {
				log.Printf("Error sending to client %s: %v", client.id, err)
				// In a real-world scenario, you might want to remove clients that fail to write
				// For this utility, we'll just log the error.
			}
		}
		s.mu.Unlock()
	}
}

// processMessage adds cosmic timestamp and starlight signature
func (s *Server) processMessage(senderID, originalMessage string) string {
	cosmicTimestamp := time.Now().UTC().Format(time.RFC3339Nano)
	
	// Generate starlight signature (deterministic hash for testing)
	hasher := sha256.New()
	hasher.Write([]byte(originalMessage + cosmicTimestamp + senderID))
	starlightSignature := hex.EncodeToString(hasher.Sum(nil))[:12] // Take first 12 chars for brevity

	return fmt.Sprintf("[%s] (From: %s) %s [Signature: %s]", cosmicTimestamp, senderID, originalMessage, starlightSignature)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	server := NewServer(port)
	if err := server.Start(); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}

	// Keep main goroutine alive until interrupted (e.g., Ctrl+C)
	select {}
}
