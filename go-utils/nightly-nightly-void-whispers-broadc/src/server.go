package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

// BroadcastServer manages client connections and broadcasts messages.
type BroadcastServer struct {
	listeners    map[net.Conn]bool
	messages     chan string
	addClient    chan net.Conn
	removeClient chan net.Conn
	quit         chan struct{}
	wg           sync.WaitGroup
	mu           sync.Mutex // Protects listeners map
}

// NewBroadcastServer creates and initializes a new BroadcastServer.
func NewBroadcastServer() *BroadcastServer {
	return &BroadcastServer{
		listeners:    make(map[net.Conn]bool),
		messages:     make(chan string, 100), // Buffered channel for messages
		addClient:    make(chan net.Conn),
		removeClient: make(chan net.Conn),
		quit:         make(chan struct{}),
	}
}

// Start begins the server's main loop, handling client connections and message broadcasting.
func (s *BroadcastServer) Start(port string) {
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}
	defer listener.Close()
	log.Printf("Void Whispers Broadcast Server listening on port %s...", port)

	s.wg.Add(1)
	go s.manageClientsAndBroadcast()

	s.wg.Add(1)
	go func() {
		defer s.wg.Done()
		for {
			conn, err := listener.Accept()
			if err != nil {
				select {
				case <-s.quit:
					return // Server is shutting down
				default:
					// If the listener is closed by Stop(), Accept() will return an error.
					// We check if the quit channel is closed to distinguish graceful shutdown.
					if !isClosed(s.quit) {
						log.Printf("Error accepting connection: %v", err)
					}
					return // Exit the accept loop on error or quit
				}
			}
			log.Printf("New listener connected: %s", conn.RemoteAddr())
			s.addClient <- conn
		}
	}()

	// Wait for quit signal to stop accepting new connections
	<-s.quit
	log.Println("Shutting down server...")
	// Close the listener to prevent new connections
	listener.Close() // This will cause the Accept() loop to error out and exit
	close(s.addClient)
	close(s.removeClient)
	close(s.messages)
	s.wg.Wait() // Wait for all goroutines to finish
	log.Println("Server shut down.")
}

// Stop sends a signal to shut down the server.
func (s *BroadcastServer) Stop() {
	select {
	case <-s.quit:
		// Already closed
	default:
		close(s.quit)
	}
}

// isClosed checks if a channel is closed without blocking.
func isClosed(ch <-chan struct{}) bool {
	select {
	case <-ch:
		return true
	default:
		return false
	}
}

// Broadcast sends a message to all connected listeners.
func (s *BroadcastServer) Broadcast(message string) {
	select {
	case s.messages <- message:
		// Message sent successfully
	case <-s.quit:
		// Server is shutting down, cannot broadcast
		log.Println("Server is shutting down, cannot broadcast message.")
	default:
		// Channel is full, drop message (ephemeral nature)
		log.Println("Message channel full, dropping whisper.")
	}
}

// manageClientsAndBroadcast is the core loop for managing clients and distributing messages.
func (s *BroadcastServer) manageClientsAndBroadcast() {
	defer s.wg.Done()
	for {
		select {
		case conn := <-s.addClient:
			s.mu.Lock()
			s.listeners[conn] = true
			s.mu.Unlock()
			s.wg.Add(1)
			go s.handleClient(conn)
		case conn := <-s.removeClient:
			s.mu.Lock()
			delete(s.listeners, conn)
			s.mu.Unlock()
			log.Printf("Listener disconnected: %s", conn.RemoteAddr())
			conn.Close()
		case msg := <-s.messages:
			s.mu.Lock()
			// Create a slice of connections to avoid iterating over a map that might change
			// if a client disconnects during the broadcast loop.
			connsToSend := make([]net.Conn, 0, len(s.listeners))
			for conn := range s.listeners {
				connsToSend = append(connsToSend, conn)
			}
			s.mu.Unlock()

			for _, conn := range connsToSend {
				// Send message in a non-blocking way or with a timeout
				// For simplicity, we'll block here, but in a real app, for high fan-out,
				// you might use a goroutine per send or a buffered channel per client.
				_, err := conn.Write([]byte(msg + "\n"))
				if err != nil {
					log.Printf("Error sending to %s: %v", conn.RemoteAddr(), err)
					s.removeClient <- conn // Mark for removal
				}
			}
		case <-s.quit:
			// Close all client connections
			s.mu.Lock()
			for conn := range s.listeners {
				conn.Close()
			}
			s.listeners = make(map[net.Conn]bool) // Clear map
			s.mu.Unlock()
			return
		}
	}
}

// handleClient manages a single client connection.
// For this broadcast-only server, it primarily listens for client disconnections.
func (s *BroadcastServer) handleClient(conn net.Conn) {
	defer s.wg.Done()
	// We don't expect clients to send messages to the server in this model,
	// but we need to read to detect disconnects (e.g., client closes connection).
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		// Client sent something, ignore it for this one-way broadcast model
		// Or log it if you want to see unexpected client input
		log.Printf("Client %s sent: %s (ignored)", conn.RemoteAddr(), scanner.Text())
	}
	// If scanner.Err() is io.EOF, it means the client closed the connection gracefully.
	// Other errors indicate network issues.
	// We always remove the client if the loop finishes.
	s.removeClient <- conn // Client disconnected or error occurred
}

func main() {
	server := NewBroadcastServer()
	port := "8080"

	go server.Start(port) // Start server in a goroutine

	// Set up a channel to listen for OS signals
	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	// Block until a signal is received
	<-c
	log.Println("Received shutdown signal, stopping server...")
	server.Stop()

	// Give some time for graceful shutdown (optional, as wg.Wait() handles it)
	time.Sleep(500 * time.Millisecond)
	log.Println("Server application exited.")
}
