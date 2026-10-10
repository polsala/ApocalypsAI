package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"
)

const ()

// Client represents a connected client to the server.
type Client struct {
	conn net.Conn
	send chan string // Channel to send messages to this specific client
	id   int
}

// DelayedMessage represents a message scheduled for future delivery.
type DelayedMessage struct {
	Content   string
	DeliverAt time.Time
}

// Server manages client connections and message delivery.
type Server struct {
	listener net.Listener
	clients  map[*Client]bool // Connected clients
	messages []DelayedMessage // Queue of messages to be delivered
	mu       sync.Mutex       // Mutex to protect shared resources (clients, messages)
	wg       sync.WaitGroup   // WaitGroup to track active goroutines
	quit     chan struct{}    // Channel to signal server shutdown
	nextClientID int
}

// NewServer creates and initializes a new Server instance.
func NewServer() *Server {
	return &Server{
		clients:      make(map[*Client]bool),
		messages:     make([]DelayedMessage, 0),
		quit:         make(chan struct{}),
		nextClientID: 1,
	}
}

// Start begins listening for connections and processing messages.
func (s *Server) Start(port int) error {
	addr := fmt.Sprintf(":%d", port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return fmt.Errorf("failed to listen on %s: %w", addr, err)
	}
	s.listener = listener
	log.Printf("Chronos Courier listening on %s", addr)

	s.wg.Add(1)
	go s.acceptConnections()

	s.wg.Add(1)
	go s.deliverMessages()

	return nil
}

// Stop gracefully shuts down the server.
func (s *Server) Stop() {
	log.Println("Shutting down Chronos Courier...")
	close(s.quit) // Signal goroutines to quit

	if s.listener != nil {
		s.listener.Close() // Close the listener to stop accepting new connections
	}

	s.mu.Lock()
	for client := range s.clients {
		client.conn.Close() // Close all client connections
		close(client.send)
	}
	s.clients = make(map[*Client]bool) // Clear clients map
	s.mu.Unlock()

	s.wg.Wait() // Wait for all goroutines to finish
	log.Println("Chronos Courier stopped.")
}

// acceptConnections accepts incoming client connections.
func (s *Server) acceptConnections() {
	defer s.wg.Done()
	for {
		conn, err := s.listener.Accept()
		if err != nil {
			select {
			case <-s.quit:
				return // Server is quitting
			default:
				log.Printf("Error accepting connection: %v", err)
			}
			continue
		}

		s.mu.Lock()
		clientID := s.nextClientID
		s.nextClientID++
		client := &Client{conn: conn, send: make(chan string, 100), id: clientID}
		s.clients[client] = true
		s.mu.Unlock()

		log.Printf("Client %d connected from %s", client.id, conn.RemoteAddr())

		s.wg.Add(1)
		go s.handleClient(client)
	}
}

// handleClient manages communication with a single client.
func (s *Server) handleClient(client *Client) {
	defer s.wg.Done()
	defer func() {
		client.conn.Close()
		s.mu.Lock()
		delete(s.clients, client)
		close(client.send)
		s.mu.Unlock()
		log.Printf("Client %d disconnected from %s", client.id, client.conn.RemoteAddr())
	}()

	// Goroutine to send messages to the client
	s.wg.Add(1)
	go func() {
		defer s.wg.Done()
		for {
			select {
			case msg, ok := <-client.send:
				if !ok {
					return // Channel closed, client disconnected
				}
				_, err := client.conn.Write([]byte(msg + "\n"))
				if err != nil {
					log.Printf("Error sending to client %d: %v", client.id, err)
					return // Stop sending to this client
				}
			case <-s.quit:
				return
			}
		}
	}()

	// Read incoming messages from the client
	scanner := bufio.NewScanner(client.conn)
	for scanner.Scan() {
		line := scanner.Text()
		log.Printf("Client %d sent: %s", client.id, line)
		s.processIncomingMessage(line)
	}

	if err := scanner.Err(); err != nil {
		log.Printf("Error reading from client %d: %v", client.id, err)
	}
}

var delayRegex = regexp.MustCompile(`^DELAY=(\d+(?:ms|s|m|h)):(.*)$`)

// processIncomingMessage parses and schedules an incoming message.
func (s *Server) processIncomingMessage(rawMessage string) {
	delay := 0 * time.Second
	content := rawMessage

	matches := delayRegex.FindStringSubmatch(rawMessage)
	if len(matches) == 3 {
		durationStr := matches[1]
		parsedDelay, err := time.ParseDuration(durationStr)
		if err != nil {
			log.Printf("Warning: Invalid delay format '%s', sending immediately. Error: %v", durationStr, err)
		} else {
			delay = parsedDelay
			content = strings.TrimSpace(matches[2])
		}
	}

	deliverAt := time.Now().Add(delay)
	msg := DelayedMessage{Content: content, DeliverAt: deliverAt}

	s.mu.Lock()
	s.messages = append(s.messages, msg)
	// Keep messages sorted by DeliverAt for efficient processing
	// (simple insertion sort for small slices, could be more optimized for large queues)
	for i := len(s.messages) - 1; i > 0 && s.messages[i].DeliverAt.Before(s.messages[i-1].DeliverAt); i-- {
		s.messages[i], s.messages[i-1] = s.messages[i-1], s.messages[i]
	}
	s.mu.Unlock()
	log.Printf("Message scheduled for delivery at %s: %s", deliverAt.Format(time.RFC3339), content)
}

// deliverMessages periodically checks the message queue and delivers ready messages.
func (s *Server) deliverMessages() {
	defer s.wg.Done()
	ticker := time.NewTicker(100 * time.Millisecond) // Check every 100ms
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			s.mu.Lock()
			now := time.Now()
			var deliveredMessages []string
			var remainingMessages []DelayedMessage

			for _, msg := range s.messages {
				if msg.DeliverAt.Before(now) || msg.DeliverAt.Equal(now) {
					deliveredMessages = append(deliveredMessages, msg.Content)
				} else {
					remainingMessages = append(remainingMessages, msg)
				}
			}
			s.messages = remainingMessages
			s.mu.Unlock()

			if len(deliveredMessages) > 0 {
				for _, content := range deliveredMessages {
					s.broadcastMessage(content)
				}
			}
		case <-s.quit:
			return
		}
	}
}

// broadcastMessage sends a message to all connected clients.
func (s *Server) broadcastMessage(message string) {
	log.Printf("Broadcasting message: %s", message)
	// Create a copy of clients to avoid holding mutex during potentially slow network writes
	s.mu.Lock()
	clientsToSend := make([]*Client, 0, len(s.clients))
	for client := range s.clients {
		clientsToSend = append(clientsToSend, client)
	}
	s.mu.Unlock()

	for _, client := range clientsToSend {
		select {
		case client.send <- message:
			// Message sent to client's send channel
		default:
			// Client's send channel is full, skip for now to avoid blocking
			log.Printf("Warning: Client %d send channel full, dropping message: %s", client.id, message)
		}
	}
}

func main() {
	port := flag.Int("port", 8080, "Port to listen on")
	flag.Parse()

	server := NewServer()
	if err := server.Start(*port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}

	// Handle graceful shutdown
	c := make(chan os.Signal, 1)
	// signal.Notify(c, os.Interrupt, syscall.SIGTERM)
	// <-c
	// For simplicity in this utility, we'll just let it run until killed or for tests.
	// In a real-world app, uncomment the above and call server.Stop() here.

	// Keep main goroutine alive for demonstration purposes.
	// In a production environment, you'd use signal handling to call server.Stop()
	// For this utility, we'll just block indefinitely or until tests stop it.
	select {}
}
