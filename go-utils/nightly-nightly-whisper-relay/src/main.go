package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"sync"
	"time"
)

// client represents a single connected client.
type client struct {
	conn net.Conn
	send chan string // Channel to send messages to this client
}

// Hub manages the set of active clients and broadcasts messages.
type Hub struct {
	clients    map[*client]bool
	broadcast  chan string // Inbound messages from clients
	register   chan *client  // Register requests from clients
	unregister chan *client  // Unregister requests from clients
	mu         sync.Mutex
}

// NewHub creates and returns a new Hub instance.
func NewHub() *Hub {
	return &Hub{
		broadcast:  make(chan string),
		register:   make(chan *client),
		unregister: make(chan *client),
		clients:    make(map[*client]bool),
	}
}

// Run starts the hub's message processing loop.
func (h *Hub) Run() {
	for {
		select {
		case client := <-h.register:
			h.mu.Lock()
			h.clients[client] = true
			h.mu.Unlock()
			log.Printf("Client registered: %s (Total: %d)", client.conn.RemoteAddr(), len(h.clients))

		case client := <-h.unregister:
			h.mu.Lock()
			if _, ok := h.clients[client]; ok {
				delete(h.clients, client)
				close(client.send)
			}
			h.mu.Unlock()
			log.Printf("Client unregistered: %s (Total: %d)", client.conn.RemoteAddr(), len(h.clients))

		case message := <-h.broadcast:
			h.mu.Lock()
			for client := range h.clients {
				select {
				case client.send <- message:
				// Message sent successfully
				default:
					// Client's send buffer is full, assume it's slow or disconnected
					log.Printf("Dropping message for slow client: %s", client.conn.RemoteAddr())
					close(client.send)
					delete(h.clients, client)
				}
			}
			h.mu.Unlock()
		}
	}
}

// handleClient manages a single client connection.
func (h *Hub) handleClient(conn net.Conn) {
	client := &client{conn: conn, send: make(chan string, 256)} // Buffered channel
	h.register <- client

	// Goroutine to write messages to the client
	go func() {
		defer conn.Close()
		for message := range client.send {
			_, err := fmt.Fprintln(conn, message)
			if err != nil {
				log.Printf("Error writing to client %s: %v", conn.RemoteAddr(), err)
				return // Exit writer goroutine on error
			}
		}
		log.Printf("Client writer for %s stopped.", conn.RemoteAddr())
	}()

	// Read messages from the client
	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		message := scanner.Text()
		log.Printf("Received from %s: %s", conn.RemoteAddr(), message)
		// Only broadcast if there are other clients to send to
		h.mu.Lock()
		if len(h.clients) > 1 {
			h.broadcast <- fmt.Sprintf("[%s] %s", conn.RemoteAddr().String(), message)
		}
		h.mu.Unlock()
	}

	// Handle scanner errors or EOF
	if err := scanner.Err(); err != nil {
		log.Printf("Error reading from client %s: %v", conn.RemoteAddr(), err)
	}

	h.unregister <- client
	log.Printf("Client handler for %s stopped.", conn.RemoteAddr())
}

func main() {
	port := flag.Int("port", 8080, "Port to listen on")
	flag.Parse()

	log.SetOutput(os.Stdout)
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	hub := NewHub()
	go hub.Run()

	addr := fmt.Sprintf(":%d", *port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("Failed to listen on %s: %v", addr, err)
	}
	defer listener.Close()

	log.Printf("Nightly Whisper Relay listening on %s", addr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v", err)
			continue
		}
		go hub.handleClient(conn)
	}
}
