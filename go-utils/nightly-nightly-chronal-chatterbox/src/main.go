package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	defaultPort = "8080"
	minDelayMs  = 1000 // Minimum delay in milliseconds (1 second)
	maxDelayMs  = 6000 // Maximum delay in milliseconds (6 seconds)
)

// handleConnection processes an incoming client connection.
// It reads a message, applies a random delay, and echoes it back.
func handleConnection(conn net.Conn) {
	defer conn.Close()

	reader := bufio.NewReader(conn)

	// Set a read deadline to prevent goroutines from hanging indefinitely
	// if a client connects but sends no data.
	conn.SetReadDeadline(time.Now().Add(time.Duration(maxDelayMs*2) * time.Millisecond))

	message, err := reader.ReadString('\n')
	if err != nil {
		if !strings.Contains(err.Error(), "use of closed network connection") {
			fmt.Printf("Error reading from %s: %v\n", conn.RemoteAddr(), err)
		}
		return
	}

	// Remove newline character for cleaner output and echo
	trimmedMessage := strings.TrimSpace(message)

	// Generate a random delay between minDelayMs and maxDelayMs
	rand.Seed(time.Now().UnixNano())
	delayMs := rand.Intn(maxDelayMs-minDelayMs+1) + minDelayMs
	delay := time.Duration(delayMs) * time.Millisecond

	fmt.Printf("[%s] Received: \"%s\" (delaying for %v)\n", conn.RemoteAddr(), trimmedMessage, delay)

	// Simulate temporal distortion (delay)
	time.Sleep(delay)

	// Prepare the echoed response
	response := fmt.Sprintf("[Echoed from Chronal Chatterbox after %v]: %s\n", delay, message)

	// Write the response back to the client
	_, err = conn.Write([]byte(response))
	if err != nil {
		fmt.Printf("Error writing to %s: %v\n", conn.RemoteAddr(), err)
	}
	fmt.Printf("[%s] Echoed: \"%s\"\n", conn.RemoteAddr(), trimmedMessage)
}

func main() {
	// Initialize random seed for delays
	rand.Seed(time.Now().UnixNano())

	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		fmt.Printf("Error listening on port %s: %v\n", port, err)
		os.Exit(1)
	}
	defer listener.Close()

	fmt.Printf("Chronal Chatterbox listening on port %s\n", port)

	for {
		// Accept new connections
		conn, err := listener.Accept()
		if err != nil {
			// If the listener is closed, Accept will return an error. Handle gracefully.
			if strings.Contains(err.Error(), "use of closed network connection") {
				fmt.Println("Listener closed, shutting down.")
				break
			}
			fmt.Printf("Error accepting connection: %v\n", err)
			continue
		}

		// Handle each connection in a new goroutine
		go handleConnection(conn)
	}
}
