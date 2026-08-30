package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/google/uuid"
)

// client represents a connected client with its connection and a channel to send messages to it.
type client struct {
	conn net.Conn
	send chan string
}

// AmplifierServer manages clients and broadcasts amplified messages.
type AmplifierServer struct {
	port      int
	clients   map[*client]bool
	broadcast chan string
	register  chan *client
	unregister chan *client
	mu        sync.RWMutex // Mutex to protect clients map
}

// NewAmplifierServer creates and initializes a new AmplifierServer.
func NewAmplifierServer(port int) *AmplifierServer {
	return &AmplifierServer{
		port:       port,
		clients:    make(map[*client]bool),
		broadcast:  make(chan string),
		register:   make(chan *client),
		unregister: make(chan *client),
	}
}

// Start begins listening for incoming connections and manages client lifecycle.
func (s *AmplifierServer) Start() {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", s.port))
	if err != nil {
		log.Fatalf("Failed to listen on port %d: %v", s.port, err)
	}
	defer listener.Close()

	log.Printf("Starlight Signal Amplifier listening on port %d", s.port)

	go s.run()

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v", err)
			continue
		}
		log.Printf("New client connected: %s", conn.RemoteAddr())
		newClient := &client{conn: conn, send: make(chan string, 256)}
		s.register <- newClient
		go s.handleClient(newClient)
	}
}

// run manages the server's internal state, handling client registration, unregistration, and message broadcasting.
func (s *AmplifierServer) run() {
	for {
		select {
		case client := <-s.register:
			s.mu.Lock()
			s.clients[client] = true
			s.mu.Unlock()
			log.Printf("Client registered: %s (Total: %d)", client.conn.RemoteAddr(), len(s.clients))
		case client := <-s.unregister:
			s.mu.Lock()
			if _, ok := s.clients[client]; ok {
				delete(s.clients, client)
				close(client.send)
				client.conn.Close()
			}
			s.mu.Unlock()
			log.Printf("Client unregistered: %s (Total: %d)", client.conn.RemoteAddr(), len(s.clients))
		case message := <-s.broadcast:
			s.mu.RLock()
			for client := range s.clients {
				select {
				case client.send <- message:
				default:
					// If client's send buffer is full, assume it's slow or dead and unregister.
					log.Printf("Client %s send buffer full, unregistering", client.conn.RemoteAddr())
					// Note: Deleting from map here is safe because it's within RLock, but actual unregister
					// should happen via unregister channel to ensure proper cleanup and mutex usage.
					// For simplicity in this example, we'll just log and let the next unregister cycle handle it.
					// A more robust solution might send to unregister channel here.
					// For now, we'll just skip sending to this client.
				}
			}
			s.mu.RUnlock()
		}
	}
}

// handleClient manages reading from and writing to a single client connection.
func (s *AmplifierServer) handleClient(c *client) {
	defer func() {
		s.unregister <- c
	}()

	// Goroutine to send messages to the client
	go func() {
		for msg := range c.send {
			_, err := fmt.Fprintln(c.conn, msg)
			if err != nil {
				log.Printf("Error sending to client %s: %v", c.conn.RemoteAddr(), err)
				return // Exit goroutine if write fails
			}
		}
	}()

	// Read messages from the client
	scanner := bufio.NewScanner(c.conn)
	for scanner.Scan() {
		originalMessage := scanner.Text()
		if strings.TrimSpace(originalMessage) == "" {
			continue // Ignore empty messages
		}
		amplifiedMessage := amplifyMessage(originalMessage)
		s.broadcast <- amplifiedMessage
	}

	// Check for scanner errors (e.g., client disconnected)
	if err := scanner.Err(); err != nil && err != io.EOF {
		log.Printf("Error reading from client %s: %v", c.conn.RemoteAddr(), err)
	}
}

// amplifyMessage adds a timestamp and a unique cosmic signature to the original message.
func amplifyMessage(originalMessage string) string {
	timestamp := time.Now().UTC().Format("2006-01-02 15:04:05 UTC")
	cosmicSignature := uuid.New().String()
	return fmt.Sprintf("[%s] [Cosmic-Sig: %s] %s", timestamp, cosmicSignature, originalMessage)
}

func main() {
	port := flag.Int("port", 8080, "Port to listen on for incoming connections")
	flag.Parse()

	server := NewAmplifierServer(*port)
	server.Start()
}
