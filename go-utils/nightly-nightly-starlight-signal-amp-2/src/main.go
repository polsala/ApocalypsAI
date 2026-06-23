package main

import (
	"bufio"
	"fmt"
	"io"
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
	SignalKeyword = "STARLIGHT_PING"
	Port          = "8080" // Default port
)

var (
	whimsicalResponses = []string{
		"The cosmos hums with your brilliance!",
		"A ripple in the fabric of spacetime! Magnificent!",
		"Your signal has transcended the void!",
		"Behold! The stars align for your message!",
		"Echoes of ancient light confirm your presence!",
		"The celestial dance acknowledges your input!",
	}
)

// Server represents the Starlight Signal Amplifier server.
type Server struct {
	listener    net.Listener
	clients     map[net.Conn]struct{}
	broadcastCh chan string
	mu          sync.Mutex // Protects clients map
	wg          sync.WaitGroup
	running     bool
}

// NewServer creates and initializes a new Server.
func NewServer(listener net.Listener) *Server {
	return &Server{
		listener:    listener,
		clients:     make(map[net.Conn]struct{}),
		broadcastCh: make(chan string),
		running:     false,
	}
}

// Start begins listening for incoming connections and handling messages.
func (s *Server) Start() {
	s.mu.Lock()
	if s.running {
		s.mu.Unlock()
		return
	}
	s.running = true
	s.mu.Unlock()

	log.Printf("Starlight Signal Amplifier listening on %s", s.listener.Addr())

	s.wg.Add(1)
	go s.broadcastLoop()

	for {
		conn, err := s.listener.Accept()
		if err != nil {
			s.mu.Lock()
			isRunning := s.running
			s.mu.Unlock()
			if !isRunning { // If server is intentionally stopped
				log.Println("Listener closed, server shutting down.")
				return
			}
			log.Printf("Error accepting connection: %v", err)
			continue
		}

		s.addClient(conn)
		s.wg.Add(1)
		go s.handleClient(conn)
	}
}

// Stop closes the listener and all client connections.
func (s *Server) Stop() {
	s.mu.Lock()
	if !s.running {
		s.mu.Unlock()
		return
	}
	s.running = false
	s.mu.Unlock()

	log.Println("Stopping Starlight Signal Amplifier...")
	if s.listener != nil {
		s.listener.Close()
	}

	// Close all client connections
	s.mu.Lock()
	for conn := range s.clients {
		conn.Close()
		delete(s.clients, conn)
	}
	s.mu.Unlock()

	close(s.broadcastCh) // Close broadcast channel to signal broadcastLoop to exit
	s.wg.Wait()          // Wait for all goroutines to finish
	log.Println("Starlight Signal Amplifier stopped.")
}

// addClient adds a new client connection to the server.
func (s *Server) addClient(conn net.Conn) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.clients[conn] = struct{}{}
	log.Printf("Client connected: %s", conn.RemoteAddr())
}

// removeClient removes a client connection from the server.
func (s *Server) removeClient(conn net.Conn) {
	s.mu.Lock()
	defer s.mu.Unlock()
	delete(s.clients, conn)
	log.Printf("Client disconnected: %s", conn.RemoteAddr())
}

// handleClient reads messages from a client and processes them.
func (s *Server) handleClient(conn net.Conn) {
	defer s.wg.Done()
	defer s.removeClient(conn)
	defer conn.Close()

	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			if err != io.EOF {
				log.Printf("Error reading from client %s: %v", conn.RemoteAddr(), err)
			}
			return // Client disconnected or error
		}

		message = strings.TrimSpace(message)
		log.Printf("Received from %s: %s", conn.RemoteAddr(), message)

		if strings.Contains(strings.ToUpper(message), SignalKeyword) {
			response := s.getRandomWhimsicalResponse()
			s.broadcastCh <- fmt.Sprintf("✨ AMPLIFIED SIGNAL DETECTED! ✨ %s (from %s)\n", response, conn.RemoteAddr())
		} else {
			// Optionally, echo back or ignore non-signal messages
			conn.Write([]byte(fmt.Sprintf("Starlight Amplifier received: %s\n", message)))
		}
	}
}

// broadcastLoop sends messages from the broadcast channel to all connected clients.
func (s *Server) broadcastLoop() {
	defer s.wg.Done()
	for msg := range s.broadcastCh {
		s.mu.Lock()
		for clientConn := range s.clients {
			_, err := clientConn.Write([]byte(msg))
			if err != nil {
				log.Printf("Error writing to client %s: %v", clientConn.RemoteAddr(), err)
				// Consider removing client if write fails persistently, but for simplicity, we'll just log.
			}
		}
		s.mu.Unlock()
	}
	log.Println("Broadcast loop stopped.")
}

// getRandomWhimsicalResponse returns a random response from the predefined list.
func (s *Server) getRandomWhimsicalResponse() string {
	return whimsicalResponses[rand.Intn(len(whimsicalResponses))]
}

func main() {
	rand.Seed(time.Now().UnixNano()) // Seed for random responses, once at startup

	listener, err := net.Listen("tcp", ":"+Port)
	if err != nil {
		log.Fatalf("Failed to start listener: %v", err)
	}

	server := NewServer(listener)
	go server.Start()

	// Handle graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
	<-sigCh // Block until a signal is received

	server.Stop() // Stop the server gracefully
}
