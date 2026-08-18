package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strconv"
	"sync"
	"syscall"
	"time"
)

const (
	defaultPort = 8080
)

// Echo represents a processed temporal echo
type Echo struct {
	ID         int
	Timestamp  time.Time
	Message    string
	ClientAddr string
}

// EchoProcessor handles incoming messages and transforms them into Echo objects
type EchoProcessor struct {
	nextEchoID int
	mu         sync.Mutex
}

// NewEchoProcessor creates a new EchoProcessor
func NewEchoProcessor() *EchoProcessor {
	return &EchoProcessor{
		nextEchoID: 1,
	}
}

// ProcessMessage takes a raw message and client address, returns a processed Echo
func (ep *EchoProcessor) ProcessMessage(message, clientAddr string) Echo {
	ep.mu.Lock()
	defer ep.mu.Unlock()

	echo := Echo{
		ID:         ep.nextEchoID,
		Timestamp:  time.Now(),
		Message:    message,
		ClientAddr: clientAddr,
	}
	ep.nextEchoID++
	return echo
}

// Server holds the server configuration and state
type Server struct {
	port        int
	listener    net.Listener
	processor   *EchoProcessor
	echoChannel chan Echo
	wg          sync.WaitGroup
	shutdown    chan struct{}
}

// NewServer creates a new Server instance
func NewServer(port int) *Server {
	return &Server{
		port:        port,
		processor:   NewEchoProcessor(),
		echoChannel: make(chan Echo, 100), // Buffered channel for echoes
		shutdown:    make(chan struct{}),
	}
}

// Start begins listening for incoming connections
func (s *Server) Start() error {
	addr := fmt.Sprintf(":%d", s.port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return fmt.Errorf("failed to listen on %s: %w", addr, err)
	}
	s.listener = listener
	log.Printf("Temporal Echo Listener started on %s", s.listener.Addr().String())

	// Start echo logger goroutine
	s.wg.Add(1)
	go s.logEchoes()

	// Accept connections in a loop
	s.wg.Add(1)
	go func() {
		defer s.wg.Done()
		for {
			conn, err := s.listener.Accept()
			if err != nil {
				select {
				case <-s.shutdown:
					log.Println("Server listener shutting down.")
					return
				default:
					// If not a graceful shutdown, log the error
					log.Printf("Error accepting connection: %v", err)
					continue
				}
			}
			s.wg.Add(1)
			go s.handleConnection(conn)
		}
	}()
	return nil
}

// Stop gracefully shuts down the server
func (s *Server) Stop() {
	log.Println("Shutting down Temporal Echo Listener...")
	close(s.shutdown) // Signal shutdown to listener goroutine
	if s.listener != nil {
		s.listener.Close() // Close the listener to unblock Accept()
	}
	close(s.echoChannel) // Close the channel to signal logEchoes to exit
	s.wg.Wait()          // Wait for all goroutines to finish
	log.Println("Temporal Echo Listener stopped.")
}

// handleConnection processes a single client connection
func (s *Server) handleConnection(conn net.Conn) {
	defer s.wg.Done()
	defer conn.Close()

	clientAddr := conn.RemoteAddr().String()
	log.Printf("New temporal conduit opened from %s", clientAddr)

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		message := scanner.Text()
		if message == "" {
			continue
		}
		echo := s.processor.ProcessMessage(message, clientAddr)
		s.echoChannel <- echo // Send processed echo to the logging channel
	}

	if err := scanner.Err(); err != nil && err != io.EOF {
		log.Printf("Error reading from %s: %v", clientAddr, err)
	}
	log.Printf("Temporal conduit from %s closed.", clientAddr)
}

// logEchoes consumes echoes from the channel and logs them
func (s *Server) logEchoes() {
	defer s.wg.Done()
	for echo := range s.echoChannel {
		fmt.Printf("[ECHO %d] %s from %s: \"%s\"\n", echo.ID, echo.Timestamp.Format(time.RFC3339), echo.ClientAddr, echo.Message)
	}
	log.Println("Echo logging goroutine stopped.")
}

func main() {
	portStr := os.Getenv("PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port == 0 {
		port = defaultPort
	}

	server := NewServer(port)
	if err := server.Start(); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}

	// Set up a channel to listen for OS signals
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Block until a signal is received
	<-sigChan
	log.Println("OS signal received, initiating shutdown...")
	server.Stop()
}
