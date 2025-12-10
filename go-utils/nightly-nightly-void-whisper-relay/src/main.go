package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	PORT = "8080"
)

// Client represents a connected client with its connection and an incoming message channel.
type Client struct {
	conn     net.Conn
	incoming chan string
}

var (
	clients    = make(map[net.Conn]*Client) // Map of active clients
	messages   = make(chan string)          // Channel for incoming messages from any client
	register   = make(chan *Client)         // Channel to register new clients
	unregister = make(chan *Client)       // Channel to unregister clients
	mu         sync.Mutex                 // Mutex to protect access to the clients map
)

// distortMessage applies a whimsical, deterministic distortion to a message.
// # Mock rationale: This function is designed to be deterministic for testing purposes.
// In a more complex scenario, it could incorporate randomness or more elaborate transformations.
func distortMessage(msg string) string {
	return msg + " ~void echo~"
}

// handleClient reads messages from a client and writes broadcasted messages to it.
func handleClient(client *Client) {
	defer func() {
		unregister <- client
		client.conn.Close()
	}()

	// Goroutine to send messages to the client
	go func() {
		for msg := range client.incoming {
			_, err := client.conn.Write([]byte(msg + "\n"))
			if err != nil {
				log.Printf("Error writing to client %s: %v", client.conn.RemoteAddr(), err)
				return
			}
		}
	}()

	// Read messages from the client
	scanner := bufio.NewScanner(client.conn)
	for scanner.Scan() {
		msg := scanner.Text()
		if strings.TrimSpace(msg) != "" {
			log.Printf("Received from %s: %s", client.conn.RemoteAddr(), msg)
			messages <- msg // Send to the central message channel for broadcasting
		}
	}

	if err := scanner.Err(); err != nil {
		log.Printf("Error reading from client %s: %v", client.conn.RemoteAddr(), err)
	}
}

// broadcaster manages client connections and message distribution.
func broadcaster() {
	for {
		select {
		case client := <-register:
			mu.Lock()
			clients[client.conn] = client
			mu.Unlock()
			log.Printf("Client %s connected. Total clients: %d", client.conn.RemoteAddr(), len(clients))

		case client := <-unregister:
			mu.Lock()
			if _, ok := clients[client.conn]; ok {
				delete(clients, client.conn)
				close(client.incoming) // Close the client's incoming channel
			}
			mu.Unlock()
			log.Printf("Client %s disconnected. Total clients: %d", client.conn.RemoteAddr(), len(clients))

		case msg := <-messages:
			distortedMsg := distortMessage(msg)
			log.Printf("Broadcasting distorted message: %s", distortedMsg)
			mu.Lock()
			for _, client := range clients {
				select {
				case client.incoming <- distortedMsg:
					// Message sent successfully
				default:
					// Client's incoming channel is blocked, skip or handle error
					log.Printf("Warning: Client %s channel blocked, dropping message.", client.conn.RemoteAddr())
				}
			}
			mu.Unlock()
		}
	}
}

// startServer sets up the TCP listener and accepts incoming connections.
func startServer() {
	listener, err := net.Listen("tcp", ":"+PORT)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
	defer listener.Close()

	log.Printf("Void Whisper Relay listening on :%s", PORT)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v", err)
			continue
		}

		client := &Client{conn: conn, incoming: make(chan string, 100)) // Buffered channel
		register <- client
		go handleClient(client)
	}
}

func main() {
	log.SetOutput(os.Stdout)
	log.SetFlags(log.LstdFlags | log.Lshortfile)

	go broadcaster()
	startServer()
}
