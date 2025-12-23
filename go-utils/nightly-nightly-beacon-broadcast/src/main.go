package main

import (
	"bytes"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"strings"
	"time"
)

const defaultPort = 8080
const defaultInterval = 5 * time.Second
const defaultKey = "apocalypsai"

// xorCipher performs a simple XOR encryption/decryption.
// It's for whimsical obfuscation, not real security.
func xorCipher(data []byte, key string) []byte {
	if len(key) == 0 {
		return data // No key, no encryption
	}
	result := make([]byte, len(data))
	for i := 0; i < len(data); i++ {
		result[i] = data[i] ^ key[i%len(key)]
	}
	return result
}

// startBroadcaster sends encrypted beacon messages to target addresses.
// The 'done' channel allows for graceful shutdown in tests.
func startBroadcaster(port int, interval time.Duration, key string, targets []string, done <-chan struct{}) {
	log.Printf("Starting Beacon Broadcaster on port %d, interval %s, targets: %v", port, interval, targets)

	conn, err := net.ListenUDP("udp", &net.UDPAddr{Port: port})
	if err != nil {
		log.Fatalf("Broadcaster: Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			message := fmt.Sprintf("Beacon heartbeat from %s at %s", getHostname(), time.Now().Format(time.RFC3339))
			encryptedMessage := xorCipher([]byte(message), key)

			for _, target := range targets {
				addr, err := net.ResolveUDPAddr("udp", target)
				if err != nil {
					log.Printf("Broadcaster: Failed to resolve target address %s: %v", target, err)
					continue
				}
				_, err = conn.WriteToUDP(encryptedMessage, addr)
				if err != nil {
					log.Printf("Broadcaster: Failed to send message to %s: %v", target, err)
				} else {
					log.Printf("Broadcaster: Sent beacon to %s (encrypted size: %d)", target, len(encryptedMessage))
				}
			}
		case <-done:
			log.Println("Broadcaster: Shutting down.")
			return
		}
	}
}

// startListener listens for encrypted beacon messages and decrypts them.
// The 'done' channel allows for graceful shutdown in tests.
func startListener(port int, key string, done <-chan struct{}) {
	log.Printf("Starting Beacon Listener on port %d", port)

	addr, err := net.ResolveUDPAddr("udp", fmt.Sprintf(":%d", port))
	if err != nil {
		log.Fatalf("Listener: Failed to resolve UDP address for port %d: %v", port, err)
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatalf("Listener: Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()

	buffer := make([]byte, 1024) // Max UDP packet size for this simple utility

	for {
		select {
		case <-done:
			log.Println("Listener: Shutting down.")
			return
		default:
			// Set a read deadline to allow the select statement to check the 'done' channel periodically
			conn.SetReadDeadline(time.Now().Add(100 * time.Millisecond))
			n, remoteAddr, err := conn.ReadFromUDP(buffer)
			if err != nil {
				if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
					continue // Timeout, check done channel again
				}
				log.Printf("Listener: Error reading from UDP: %v", err)
				continue
			}

			received := buffer[:n]
			decrypted := xorCipher(received, key)

			fmt.Printf("Received encrypted beacon from %s (size: %d):\n", remoteAddr, n)
			fmt.Printf("  Encrypted: %x\n", received)
			fmt.Printf("  Decrypted: %s\n", string(decrypted))
		}
	}
}

// getHostname safely retrieves the hostname or returns a default.
func getHostname() string {
	name, err := os.Hostname()
	if err != nil {
		return "unknown-host"
	}
	return name
}

func main() {
	mode := flag.String("mode", "broadcaster", "Mode to run: 'broadcaster' or 'listener'")
	port := flag.Int("port", defaultPort, "UDP port to listen on or send from")
	intervalStr := flag.String("interval", defaultInterval.String(), "Broadcast interval (e.g., '5s', '1m')")
	key := flag.String("key", defaultKey, "Encryption key for XOR cipher")
	targetsStr := flag.String("targets", "127.0.0.1:8080", "Comma-separated list of target addresses for broadcaster (e.g., '127.0.0.1:8080,192.168.1.100:8080')")

	flag.Parse()

	interval, err := time.ParseDuration(*intervalStr)
	if err != nil {
		log.Fatalf("Invalid interval format: %v", err)
	}

	targets := strings.Split(*targetsStr, ",")
	if *mode == "broadcaster" && len(targets) == 0 {
		log.Fatal("Broadcaster mode requires at least one target address.")
	}

	// In main, we run indefinitely, so pass a nil done channel
	// The application will exit on Ctrl+C or process termination.
	
	if *mode == "broadcaster" {
		startBroadcaster(*port, interval, *key, targets, nil)
	} else if *mode == "listener" {
		startListener(*port, *key, nil)
	} else {
		log.Fatalf("Invalid mode: %s. Must be 'broadcaster' or 'listener'.", *mode)
	}
}
