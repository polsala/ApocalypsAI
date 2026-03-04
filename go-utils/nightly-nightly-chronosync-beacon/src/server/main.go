package main

import (
	"flag"
	"fmt"
	"net"
	"strconv"
	"time"
)

// GetTimeFunc is a function type that returns the current time in Unix nanoseconds.
// Exported for testing purposes.
type GetTimeFunc func() int64

// defaultGetTime provides the actual current time.
func defaultGetTime() int64 {
	return time.Now().UnixNano()
}

// StartServer starts the UDP server on the given port.
// It uses the provided getTime function to get the current time.
// It also accepts a stop channel to allow graceful shutdown during tests.
func StartServer(port int, getTime GetTimeFunc, stopChan <-chan struct{}) error {
	addr := fmt.Sprintf(":%d", port)
	udpAddr, err := net.ResolveUDPAddr("udp", addr)
	if err != nil {
		return fmt.Errorf("failed to resolve UDP address: %w", err)
	}

	conn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		return fmt.Errorf("failed to listen on UDP: %w", err)
	}
	defer conn.Close()

	fmt.Printf("Chronosync Beacon Server listening on UDP %s\n", addr)

	buffer := make([]byte, 1024)
	for {
		select {
		case <-stopChan:
			fmt.Println("Chronosync Beacon Server shutting down.")
			return nil
		default:
			// Set a read deadline to allow checking stopChan periodically
			conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
			n, remoteAddr, err := conn.ReadFromUDP(buffer)
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Timeout, check stopChan again
				}
				// Log other errors but continue
				fmt.Printf("Error reading from UDP: %v\n", err)
				continue
			}

			// Handle the request in a goroutine to allow concurrent processing
			go handleRequest(conn, remoteAddr, getTime, buffer[:n])
		}
	}
}

// handleRequest processes a single UDP request.
func handleRequest(conn *net.UDPConn, remoteAddr *net.UDPAddr, getTime GetTimeFunc, data []byte) {
	currentTime := getTime()
	response := []byte(strconv.FormatInt(currentTime, 10))

	_, err := conn.WriteToUDP(response, remoteAddr)
	if err != nil {
		fmt.Printf("Error sending response to %s: %v\n", remoteAddr, err)
	}
}

func main() {
	port := flag.Int("port", 8080, "UDP port to listen on")
	flag.Parse()

	// In main, the server runs indefinitely, so pass a nil stop channel.
	// A real application would use OS signals (e.g., os.Interrupt) for graceful shutdown.
	if err := StartServer(*port, defaultGetTime, nil); err != nil {
		fmt.Printf("Server error: %v\n", err)
	}
}
