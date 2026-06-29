package main

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	defaultPort       = 8080
	defaultEchoDelay  = 0 * time.Millisecond
	defaultEchoReverse = false
)

type Config struct {
	Port        int
	EchoDelay   time.Duration
	EchoReverse bool
}

// loadConfig reads configuration from environment variables.
func loadConfig() Config {
	portStr := os.Getenv("PORT")
	port, err := strconv.Atoi(portStr)
	if err != nil || port <= 0 {
		port = defaultPort
	}

	delayStr := os.Getenv("ECHO_DELAY_MS")
	delayMs, err := strconv.Atoi(delayStr)
	if err != nil || delayMs < 0 {
		delayMs = int(defaultEchoDelay / time.Millisecond)
	}
	echoDelay := time.Duration(delayMs) * time.Millisecond

	echoReverse := defaultEchoReverse
	if os.Getenv("ECHO_REVERSE") == "true" {
		echoReverse = true
	}

	return Config{
		Port:        port,
		EchoDelay:   echoDelay,
		EchoReverse: echoReverse,
	}
}

// reverseString reverses a UTF-8 string.
func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

// applyDistortion applies configured temporal distortions to a message.
func applyDistortion(message string, cfg Config) string {
	if cfg.EchoDelay > 0 {
		time.Sleep(cfg.EchoDelay)
	}
	if cfg.EchoReverse {
		return reverseString(message)
	}
	return message
}

// handleConnection processes a single client connection.
func handleConnection(conn net.Conn, cfg Config) {
	defer conn.Close()
	log.Printf("New connection from %s", conn.RemoteAddr())

	reader := bufio.NewReader(conn)
	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			if err.Error() == "EOF" {
				log.Printf("Connection closed by %s", conn.RemoteAddr())
			} else {
				log.Printf("Error reading from %s: %v", conn.RemoteAddr(), err)
			}
			return
		}

		message = strings.TrimSpace(message)
		if message == "" {
			continue // Ignore empty lines
		}

		log.Printf("Received from %s: %s", conn.RemoteAddr(), message)

		distortedMessage := applyDistortion(message, cfg)
		_, err = conn.Write([]byte(distortedMessage + "\n"))
		if err != nil {
			log.Printf("Error writing to %s: %v", conn.RemoteAddr(), err)
			return
		}
		log.Printf("Sent to %s: %s", conn.RemoteAddr(), distortedMessage)
	}
}

// startServer sets up and runs the TCP listener.
func startServer(ctx context.Context, cfg Config, wg *sync.WaitGroup, errChan chan<- error) {
	defer wg.Done()

	addr := fmt.Sprintf(":%d", cfg.Port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		errChan <- fmt.Errorf("failed to listen on %s: %w", addr, err)
		return
	}
	defer listener.Close()
	log.Printf("Temporal Echo Listener started on %s with delay %v, reverse %t", addr, cfg.EchoDelay, cfg.EchoReverse)

	go func() {
		<-ctx.Done()
		log.Println("Shutting down server...")
		listener.Close() // This will unblock the Accept() call
	}()

	for {
		conn, err := listener.Accept()
		if err != nil {
			select {
			case <-ctx.Done():
				return // Server is shutting down gracefully
			default:
				errChan <- fmt.Errorf("error accepting connection: %w", err)
				return // Propagate error and stop server goroutine
			}
		}
		go handleConnection(conn, cfg)
	}
}

func main() {
	config := loadConfig()
	log.Printf("Configuration: Port=%d, Delay=%v, Reverse=%t", config.Port, config.EchoDelay, config.EchoReverse)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel() // Ensure cancel is called on exit

	var wg sync.WaitGroup
	wg.Add(1)
	errChan := make(chan error, 1) // Buffer 1 error
	go startServer(ctx, config, &wg, errChan)

	select {
	case err := <-errChan:
		log.Fatalf("Server failed: %v", err)
	case <-ctx.Done():
		log.Println("Main context cancelled, shutting down.")
		// In a real application, you'd listen for OS signals here
		// sigChan := make(chan os.Signal, 1)
		// signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
		// <-sigChan
		// log.Println("Received shutdown signal, cancelling context...")
		// cancel()
	}

	wg.Wait() // Wait for the server goroutine to finish
	log.Println("Server gracefully shut down.")
}
