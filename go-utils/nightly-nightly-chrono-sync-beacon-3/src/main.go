package main

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

const defaultPort = 8080

// handleConnection processes a single client connection.
func handleConnection(conn net.Conn, logger *log.Logger) {
	defer conn.Close()
	logger.Printf("New client connected: %s", conn.RemoteAddr().String())

	reader := bufio.NewReader(conn)
	for {
		conn.SetReadDeadline(time.Now().Add(5 * time.Second)) // Set a read deadline to prevent hanging
		message, err := reader.ReadString('\n')
		if err != nil {
			if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
				logger.Printf("Client %s read timeout, disconnecting.", conn.RemoteAddr().String())
			} else if err == io.EOF {
				logger.Printf("Client %s disconnected.", conn.RemoteAddr().String())
			} else {
				logger.Printf("Error reading from client %s: %v", conn.RemoteAddr().String(), err)
			}
			return
		}

		trimmedMessage := strings.TrimSpace(message)
		if trimmedMessage == "TIME" {
			currentTime := time.Now().UTC().Format(time.RFC3339)
			response := fmt.Sprintf("%s\n", currentTime)
			_, err := conn.Write([]byte(response))
			if err != nil {
				logger.Printf("Error writing to client %s: %v", conn.RemoteAddr().String(), err)
				return
			}
			logger.Printf("Sent time '%s' to %s", currentTime, conn.RemoteAddr().String())
		} else {
			response := "ERROR: Unknown command. Send 'TIME'\n"
			_, err := conn.Write([]byte(response))
			if err != nil {
				logger.Printf("Error writing error to client %s: %v", conn.RemoteAddr().String(), err)
				return
			}
			logger.Printf("Sent error to %s for command '%s'", conn.RemoteAddr().String(), trimmedMessage)
		}
	}
}

// runServer starts the TCP server on the given listener.
// It returns an error if the server cannot start or encounters a fatal issue.
func runServer(listener net.Listener, logger *log.Logger) error {
	logger.Printf("Chrono-Sync Beacon listening on %s", listener.Addr().String())

	for {
		conn, err := listener.Accept()
		if err != nil {
			// If the listener was closed, Accept will return an error.
			// This is how we gracefully shut down the server in tests.
			if strings.Contains(err.Error(), "use of closed network connection") {
				logger.Printf("Listener closed, shutting down server.")
				return nil
			}
			logger.Printf("Error accepting connection: %v", err)
			continue
		}
		go handleConnection(conn, logger)
	}
}

func main() {
	portStr := os.Getenv("PORT")
	port := defaultPort
	if portStr != "" {
		p, err := strconv.Atoi(portStr)
		if err != nil {
			log.Fatalf("Invalid PORT environment variable: %v", err)
		}
		port = p
	}

	listenAddr := fmt.Sprintf(":%d", port)
	listener, err := net.Listen("tcp", listenAddr)
	if err != nil {
		log.Fatalf("Failed to listen on %s: %v", listenAddr, err)
	}
	defer listener.Close() // Ensure listener is closed on main exit

	// Use a standard logger for the main application
	appLogger := log.New(os.Stdout, "[SERVER] ", log.Ldate|log.Ltime|log.Lshortfile)
	if err := runServer(listener, appLogger); err != nil {
		appLogger.Fatalf("Server stopped with error: %v", err)
	}
}
