package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"sync"
	"time"
)

const (
	defaultPort     = 8080
	defaultInterval = 5 * time.Second
	xorKey          = byte(0xAB) // Whimsical "encryption" key
)

// BeaconMessage represents a message broadcast by a beacon.
type BeaconMessage struct {
	SenderID  string `json:"sender_id"`
	Message   string `json:"message"`
	Timestamp int64  `json:"timestamp"`
}

// xorEncrypt performs a simple XOR encryption.
func xorEncrypt(data []byte, key byte) []byte {
	encrypted := make([]byte, len(data))
	for i, b := range data {
		encrypted[i] = b ^ key
	}
	return encrypted
}

// xorDecrypt performs a simple XOR decryption.
func xorDecrypt(data []byte, key byte) []byte {
	return xorEncrypt(data, key) // XOR is its own inverse
}

// handleIncomingMessages listens for and processes incoming beacon messages.
func handleIncomingMessages(conn *net.UDPConn, wg *sync.WaitGroup) {
	defer wg.Done()
	buffer := make([]byte, 1024)
	for {
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			// Check if the error is due to the connection being closed
			if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
				continue // Timeout, keep listening
			}
			if err.Error() == "use of closed network connection" {
				log.Println("Listener connection closed.")
				return
			}
			log.Printf("Error reading UDP: %v\n", err)
			continue
		}

		decryptedData := xorDecrypt(buffer[:n], xorKey)
		var msg BeaconMessage
		if err := json.Unmarshal(decryptedData, &msg); err != nil {
			log.Printf("Error unmarshalling message from %s: %v\n", addr, err)
			continue
		}
		fmt.Printf("Received whisper from %s (%s): \"%s\" (at %s)\n",
			msg.SenderID, addr, msg.Message, time.Unix(msg.Timestamp, 0).Format(time.RFC3339))
	}
}

// startBeacon starts a beacon that broadcasts messages and listens for others.
func startBeacon(port int, senderID, message string, interval time.Duration) {
	addr := fmt.Sprintf(":%d", port)
	broadcastAddr := fmt.Sprintf("255.255.255.255:%d", port) // Broadcast address

	// Listen for incoming messages
	listenAddr, err := net.ResolveUDPAddr("udp", addr)
	if err != nil {
		log.Fatalf("Failed to resolve listen address: %v", err)
	}
	conn, err := net.ListenUDP("udp", listenAddr)
	if err != nil {
		log.Fatalf("Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()
	log.Printf("Beacon '%s' listening on UDP port %d and broadcasting every %v...\n", senderID, port, interval)

	var wg sync.WaitGroup
	wg.Add(1)
	go handleIncomingMessages(conn, &wg) // Start a goroutine to handle incoming messages

	// Prepare broadcast connection
	bcastAddr, err := net.ResolveUDPAddr("udp", broadcastAddr)
	if err != nil {
		log.Fatalf("Failed to resolve broadcast address: %v", err)
	}
	bcastConn, err := net.DialUDP("udp", nil, bcastAddr)
	if err != nil {
		log.Fatalf("Failed to dial broadcast address: %v", err)
	}
	defer bcastConn.Close()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for range ticker.C {
		msg := BeaconMessage{
			SenderID:  senderID,
			Message:   message,
			Timestamp: time.Now().Unix(),
		}
		jsonMsg, err := json.Marshal(msg)
		if err != nil {
			log.Printf("Error marshalling message: %v\n", err)
			continue
		}
		encryptedMsg := xorEncrypt(jsonMsg, xorKey)

		_, err = bcastConn.Write(encryptedMsg)
		if err != nil {
			log.Printf("Error broadcasting message: %v\n", err)
		} else {
			log.Printf("Broadcasted whisper: \"%s\"\n", message)
		}
	}
	wg.Wait() // Wait for the listener goroutine to finish (though in a beacon, it runs indefinitely)
}

// startListener starts a listener that only receives and displays messages.
func startListener(port int) {
	addr := fmt.Sprintf(":%d", port)
	listenAddr, err := net.ResolveUDPAddr("udp", addr)
	if err != nil {
		log.Fatalf("Failed to resolve listen address: %v", err)
	}
	conn, err := net.ListenUDP("udp", listenAddr)
	if err != nil {
		log.Fatalf("Failed to listen on UDP port %d: %v", port, err)
	}
	defer conn.Close()
	log.Printf("Listener active on UDP port %d, awaiting whispers...\n", port)

	var wg sync.WaitGroup
	wg.Add(1)
	go handleIncomingMessages(conn, &wg) // Now correctly in a goroutine
	wg.Wait() // This will wait until handleIncomingMessages exits (e.g., conn.Close() is called)
}

func main() {
	mode := flag.String("mode", "listen", "Operation mode: 'beacon' or 'listen'")
	port := flag.Int("port", defaultPort, "UDP port to use")
	senderID := flag.String("id", "ApocalypsAI-Beacon", "Sender ID for beacon messages")
	message := flag.String("msg", "All clear. Hope endures.", "Message to broadcast (beacon mode only)")
	intervalStr := flag.String("interval", "5s", "Broadcast interval (e.g., 1s, 30s, 1m) (beacon mode only)")

	flag.Parse()

	interval, err := time.ParseDuration(*intervalStr)
	if err != nil {
		log.Fatalf("Invalid interval format: %v", err)
	}

	switch *mode {
	case "beacon":
		startBeacon(*port, *senderID, *message, interval)
	case "listen":
		startListener(*port)
	default:
		fmt.Println("Invalid mode. Use 'beacon' or 'listen'.")
		flag.PrintDefaults()
		os.Exit(1)
	}
}
