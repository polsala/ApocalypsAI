package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

// Client represents a connected client
type Client struct {
	conn net.Conn
	id   string
}

// EchoServer manages clients and message broadcasting
type EchoServer struct {
	listener    net.Listener
	clients     sync.Map // map[string]*Client
	messages    chan string
	minDelay    time.Duration
	maxDelay    time.Duration
	distortMsgs bool
	shutdown    chan struct{}
	wg          sync.WaitGroup
}

// NewEchoServer creates a new EchoServer instance
func NewEchoServer(port int, minDelay, maxDelay time.Duration, distortMsgs bool) (*EchoServer, error) {
	addr := fmt.Sprintf(":%d", port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return nil, fmt.Errorf("failed to listen on port %d: %w", port, err)
	}

	log.Printf("Temporal Echo Chamber listening on %s", addr)

	return &EchoServer{
		listener:    listener,
		messages:    make(chan string, 100), // Buffered channel for messages
		minDelay:    minDelay,
		maxDelay:    maxDelay,
		distortMsgs: distortMsgs,
		shutdown:    make(chan struct{}),
	}, nil
}

// Start begins accepting connections and processing messages
func (s *EchoServer) Start() {
	// Start message processor goroutine
	s.wg.Add(1)
	go s.processMessages()

	// Start accepting client connections
	s.wg.Add(1)
	go func() {
		defer s.wg.Done()
		for {
			conn, err := s.listener.Accept()
			if err != nil {
				select {
				case <-s.shutdown:
					return // Server is shutting down
				default:
					log.Printf("Error accepting connection: %v", err)
				}
				continue
			}

			s.wg.Add(1)
			go s.handleClient(conn)
		}
	}()
}

// Stop gracefully shuts down the server
func (s *EchoServer) Stop() {
	log.Println("Shutting down Temporal Echo Chamber...")
	close(s.shutdown)
	s.listener.Close()
	s.wg.Wait() // Wait for all goroutines to finish
	close(s.messages)
	log.Println("Temporal Echo Chamber stopped.")
}

// handleClient manages a single client connection
func (s *EchoServer) handleClient(conn net.Conn) {
	defer s.wg.Done()
	defer conn.Close()

	clientID := conn.RemoteAddr().String()
	client := &Client{conn: conn, id: clientID}
	s.clients.Store(clientID, client)
	log.Printf("Client %s connected.", clientID)

	reader := bufio.NewReader(conn)
	for {
		select {
		case <-s.shutdown:
			return
		default:
			// Set a read deadline to allow checking shutdown channel
			conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
			message, err := reader.ReadString('\n')
			if err != nil {
				if err == io.EOF {
					log.Printf("Client %s disconnected.", clientID)
				} else if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Timeout, check shutdown again
				} else {
					log.Printf("Error reading from client %s: %v", clientID, err)
				}
				break // Exit loop on error
			}
			message = strings.TrimSpace(message)
			if message != "" {
				log.Printf("Received from %s: %s", clientID, message)
				s.messages <- fmt.Sprintf("[%s] %s", clientID, message)
			}
		}
	}

	s.clients.Delete(clientID)
}

// processMessages reads from the message channel, applies delay, and broadcasts
func (s *EchoServer) processMessages() {
	defer s.wg.Done()
	for {
		select {
		case <-s.shutdown:
			return
		case msg, ok := <-s.messages:
			if !ok {
				return // Channel closed
			}

			// Apply randomized temporal delay
			delay := s.minDelay + time.Duration(rand.Int63n(int64(s.maxDelay-s.minDelay+1)))
			log.Printf("Delaying message '%s' for %v", msg, delay)
			time.Sleep(delay)

			// Apply distortion if enabled
			if s.distortMsgs {
				msg = distortMessage(msg)
				log.Printf("Distorted message: %s", msg)
			}

			s.broadcastMessage(msg)
		}
	}
}

// broadcastMessage sends a message to all connected clients
func (s *EchoServer) broadcastMessage(message string) {
	message = message + "\n" // Ensure newline for client readers
	s.clients.Range(func(key, value interface{}) bool {
		client := value.(*Client)
		_, err := client.conn.Write([]byte(message))
		if err != nil {
			log.Printf("Error writing to client %s: %v", client.id, err)
			// Consider removing client if write fails persistently
			// s.clients.Delete(key)
		}
		return true // Continue iteration
	})
}

// distortMessage applies a simple, deterministic distortion (string reversal)
func distortMessage(msg string) string {
	runes := []rune(msg)
	for i, j := 0; i < len(runes)/2; i, j = i+1, len(runes)-1-i {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func main() {
	port := flag.Int("port", 8080, "Port to listen on")
	minDelayStr := flag.String("min-delay", "500ms", "Minimum delay before echoing (e.g., 1s, 500ms)")
	maxDelayStr := flag.String("max-delay", "2s", "Maximum delay before echoing (e.g., 5s, 2s)")
	distort := flag.Bool("distort", false, "Enable message distortion (reverses the message)")
	flag.Parse()

	minDelay, err := time.ParseDuration(*minDelayStr)
	if err != nil {
		log.Fatalf("Invalid min-delay duration: %v", err)
	}
	maxDelay, err := time.ParseDuration(*maxDelayStr)
	if err != nil {
		log.Fatalf("Invalid max-delay duration: %v", err)
	}

	if minDelay > maxDelay {
		log.Fatalf("min-delay cannot be greater than max-delay")
	}

	rand.Seed(time.Now().UnixNano()) // Seed random number generator

	server, err := NewEchoServer(*port, minDelay, maxDelay, *distort)
	if err != nil {
		log.Fatalf("Failed to create server: %v", err)
	}

	server.Start()

	// Keep main goroutine alive until interrupted
	select {}
}
