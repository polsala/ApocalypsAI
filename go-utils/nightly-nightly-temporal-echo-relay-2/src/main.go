package main

import (
	"bufio"
	"fmt"
	"log"
	"math/rand"
	"net"
	"strings"
	"sync"
	"time"
)

const (
	defaultPort  = "8080"
	minEchoDelay = 1 * time.Second
	maxEchoDelay = 5 * time.Second
)

// EchoMessage represents a message to be echoed
type EchoMessage struct {
	Content string
	Origin  net.Addr
}

// Client represents a connected client
type Client struct {
	Conn net.Conn
	ID   string
}

// Hub manages clients and message broadcasting
type Hub struct {
	clients    map[string]*Client
	register   chan *Client
	unregister chan *Client
	broadcast  chan EchoMessage
	mu         sync.RWMutex
	sleeper    func(time.Duration) // For mocking time.Sleep in tests
}

// NewHub creates a new Hub
func NewHub() *Hub {
	return &Hub{
		clients:    make(map[string]*Client),
		register:   make(chan *Client),
		unregister: make(chan *Client),
		broadcast:  make(chan EchoMessage),
		sleeper:    time.Sleep, // Default to actual sleep
	}
}

// Run starts the hub's goroutines for managing clients and broadcasting messages.
func (h *Hub) Run() {
	for {
		select {
		case client := <-h.register:
			h.mu.Lock()
			h.clients[client.ID] = client
			h.mu.Unlock()
			log.Printf("Client %s connected from %s", client.ID, client.Conn.RemoteAddr())
		case client := <-h.unregister:
			h.mu.Lock()
			if _, ok := h.clients[client.ID]; ok {
				delete(h.clients, client.ID)
				client.Conn.Close()
			}
			h.mu.Unlock()
			log.Printf("Client %s disconnected from %s", client.ID, client.Conn.RemoteAddr())
		case message := <-h.broadcast:
			// Simulate temporal echo delay
			delay := time.Duration(rand.Intn(int(maxEchoDelay-minEchoDelay))) + minEchoDelay
			h.sleeper(delay) // Use the configurable sleeper (mocked in tests)

			h.mu.RLock()
			for id, client := range h.clients {
				// Send to all clients, including the origin, with a temporal prefix.
				echoedContent := fmt.Sprintf("[Temporal Echo from %s] %s\n", message.Origin.String(), strings.TrimSpace(message.Content))
				_, err := client.Conn.Write([]byte(echoedContent))
				if err != nil {
					log.Printf("Error sending to client %s: %v", id, err)
					// In a real-world scenario, you might unregister clients on write failure.
				}
			}
			h.mu.RUnlock()
		}
	}
}

// handleConnection reads messages from a client and sends them to the hub for broadcasting.
func (h *Hub) handleConnection(conn net.Conn) {
	client := &Client{Conn: conn, ID: conn.RemoteAddr().String()}
	h.register <- client

	defer func() {
		h.unregister <- client
	}()

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		line := scanner.Text()
		if strings.TrimSpace(line) == "" {
			continue // Ignore empty or whitespace-only lines
		}
		h.broadcast <- EchoMessage{Content: line, Origin: conn.RemoteAddr()}
	}

	if err := scanner.Err(); err != nil {
		log.Printf("Error reading from client %s: %v", client.ID, err)
	}
}

func main() {
	// Seed the random number generator for delay calculation.
	rand.Seed(time.Now().UnixNano())

	port := defaultPort

	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v", port, err)
	}
	defer listener.Close()

	log.Printf("Temporal Echo Relay listening on :%s", port)

	hub := NewHub()
	go hub.Run() // Start the hub's message processing goroutine

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Failed to accept connection: %v", err)
			continue
		}
		go hub.handleConnection(conn) // Handle each new connection in a goroutine
	}
}
