package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"
)

// Config holds the application configuration.
type Config struct {
	ListenPort    int
	EchoTarget    string // IP:Port to send whispers to
	WhisperInterval time.Duration
	WhisperMessage  string
}

// NewConfig creates a default configuration.
func NewConfig() *Config {
	return &Config{
		ListenPort:    8080,
		EchoTarget:    "", // No target by default
		WhisperInterval: 30 * time.Second,
		WhisperMessage:  "A faint cosmic whisper...",
	}
}

// LoadConfigFromEnv loads configuration from environment variables.
func LoadConfigFromEnv() *Config {
	cfg := NewConfig()

	if portStr := os.Getenv("LISTEN_PORT"); portStr != "" {
		if port, err := strconv.Atoi(portStr); err == nil {
			cfg.ListenPort = port
		} else {
			log.Printf("Warning: Invalid LISTEN_PORT '%s', using default %d. Error: %v", portStr, cfg.ListenPort, err)
		}
	}
	if target := os.Getenv("ECHO_TARGET"); target != "" {
		cfg.EchoTarget = target
	}
	if intervalStr := os.Getenv("WHISPER_INTERVAL_SECONDS"); intervalStr != "" {
		if interval, err := strconv.Atoi(intervalStr); err == nil {
			cfg.WhisperInterval = time.Duration(interval) * time.Second
		} else {
			log.Printf("Warning: Invalid WHISPER_INTERVAL_SECONDS '%s', using default %s. Error: %v", intervalStr, cfg.WhisperInterval, err)
		}
	}
	if msg := os.Getenv("WHISPER_MESSAGE"); msg != "" {
		cfg.WhisperMessage = msg
	}
	return cfg
}

// listenForEchoes starts a UDP listener for incoming messages.
func listenForEchoes(ctx context.Context, port int) {
	addr := fmt.Sprintf(":%d", port)
	conn, err := net.ListenPacket("udp", addr)
	if err != nil {
		log.Printf("Failed to listen for cosmic echoes on %s: %v", addr, err)
		return
	}
	defer conn.Close()
	log.Printf("Listening for cosmic echoes on UDP port %d...", port)

	buffer := make([]byte, 1024)
	for {
		select {
		case <-ctx.Done():
			log.Println("Cosmic echo listener shutting down.")
			return
		default:
			// Set a short deadline to allow the select statement to check ctx.Done regularly
			conn.SetReadDeadline(time.Now().Add(500 * time.Millisecond))
			n, remoteAddr, err := conn.ReadFrom(buffer)
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Timeout, check context again
				}
				log.Printf("Error reading cosmic echo: %v", err)
				continue
			}
			log.Printf("Received cosmic echo from %s: \"%s\"", remoteAddr, string(buffer[:n]))
		}
	}
}

// sendWhispers periodically sends UDP messages to a target address.
func sendWhispers(ctx context.Context, target string, interval time.Duration, message string) {
	if target == "" {
		log.Println("No ECHO_TARGET configured. Not sending whispers.")
		return
	}

	conn, err := net.Dial("udp", target)
	if err != nil {
		log.Printf("Failed to dial echo target %s: %v", target, err)
		return
	}
	defer conn.Close()
	log.Printf("Sending cosmic whispers to %s every %s...", target, interval)

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			log.Println("Cosmic whisper sender shutting down.")
			return
		case <-ticker.C:
			_, err := conn.Write([]byte(message))
			if err != nil {
				log.Printf("Error sending cosmic whisper to %s: %v", target, err)
			} else {
				log.Printf("Sent cosmic whisper to %s: \"%s\"", target, message)
			}
		}
	}
}

func main() {
	cfg := LoadConfigFromEnv()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Start listener
	go listenForEchoes(ctx, cfg.ListenPort)

	// Start sender if target is configured
	if cfg.EchoTarget != "" {
		go sendWhispers(ctx, cfg.EchoTarget, cfg.WhisperInterval, cfg.WhisperMessage)
	} else {
		log.Println("ECHO_TARGET not set. This instance will only listen for echoes.")
	}

	// Handle graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan // Block until a signal is received

	log.Println("Initiating graceful shutdown...")
	cancel() // Signal goroutines to stop

	// Give goroutines a moment to clean up
	time.Sleep(2 * time.Second) // Allow goroutines to finish their current loop and exit
	log.Println("ApocalypsAI Cosmic Echo Listener shut down.")
}
