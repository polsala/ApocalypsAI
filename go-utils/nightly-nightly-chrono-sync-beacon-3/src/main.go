package main

import (
	"bytes"
	"encoding/gob"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"
)

// BeaconMessage represents a single status beacon.
type BeaconMessage struct {
	ID        string
	Timestamp int64
	Payload   string
}

// encodeBeacon serializes a BeaconMessage into a byte slice.
func encodeBeacon(msg BeaconMessage) ([]byte, error) {
	var buf bytes.Buffer
	encoder := gob.NewEncoder(&buf)
	if err := encoder.Encode(msg); err != nil {
		return nil, fmt.Errorf("failed to encode beacon: %w", err)
	}
	return buf.Bytes(), nil
}

// decodeBeacon deserializes a byte slice into a BeaconMessage.
func decodeBeacon(data []byte) (BeaconMessage, error) {
	var msg BeaconMessage
	buf := bytes.NewReader(data)
	decoder := gob.NewDecoder(buf)
	if err := decoder.Decode(&msg); err != nil {
		return BeaconMessage{}, fmt.Errorf("failed to decode beacon: %w", err)
	}
	return msg, nil
}

// startBeaconSender continuously sends beacon messages.
func startBeaconSender(addrStr string, interval time.Duration, id, payload string) {
	log.Printf("Starting beacon sender (ID: %s) to %s every %s with payload: '%s'", id, addrStr, interval, payload)

	conn, err := net.Dial("udp", addrStr)
	if err != nil {
		log.Fatalf("Failed to dial UDP address %s: %v", addrStr, err)
	}
	defer conn.Close()

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for range ticker.C {
		msg := BeaconMessage{
			ID:        id,
			Timestamp: time.Now().UnixNano(),
			Payload:   payload,
		}
		encodedMsg, err := encodeBeacon(msg)
		if err != nil {
			log.Printf("Error encoding beacon: %v", err)
			continue
		}

		_, err = conn.Write(encodedMsg)
		if err != nil {
			log.Printf("Error sending beacon to %s: %v", addrStr, err)
		}
	}
}

// startBeaconListener listens for and processes incoming beacon messages.
func startBeaconListener(addrStr string) {
	log.Printf("Starting beacon listener on %s", addrStr)

	addr, err := net.ResolveUDPAddr("udp", addrStr)
	if err != nil {
		log.Fatalf("Failed to resolve UDP address %s: %v", addrStr, err)
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		log.Fatalf("Failed to listen on UDP address %s: %v", addrStr, err)
	}
	defer conn.Close()

	// Handle multicast group joining if applicable
	if addr.IP.IsMulticast() {
		var iface *net.Interface
		// Try common interface names first
		iface, err = net.InterfaceByName("eth0")
		if err != nil {
			iface, err = net.InterfaceByName("en0") // macOS common
		}
		if err != nil {
			// Fallback: try to find any suitable interface
			interfaces, _ := net.Interfaces()
			for _, i := range interfaces {
				if (i.Flags&net.FlagUp != 0) && (i.Flags&net.FlagMulticast != 0) {
					iface = &i
					break
				}
			}
		}

		if iface != nil {
			if err := conn.JoinGroup(addr.IP, iface); err != nil {
				log.Printf("Warning: Failed to join multicast group %s on interface %s: %v", addr.IP, iface.Name, err)
			} else {
				log.Printf("Joined multicast group %s on interface %s", addr.IP, iface.Name)
			}
		} else {
			log.Printf("Warning: Multicast address %s detected, but no suitable interface found to join group. May not receive messages.", addr.IP)
		}
	}

	buffer := make([]byte, 1024) // Max UDP packet size
	for {
		n, _, err := conn.ReadFromUDP(buffer)
		if err != nil {
			// If the connection is closed, ReadFromUDP will return an error, exit gracefully.
			if strings.Contains(err.Error(), "use of closed network connection") {
				return
			}
			log.Printf("Error reading from UDP: %v", err)
			continue
		}

		msg, err := decodeBeacon(buffer[:n])
		if err != nil {
			log.Printf("Error decoding beacon: %v", err)
			continue
		}

		log.Printf("Received beacon from %s (Timestamp: %s): %s", msg.ID, time.Unix(0, msg.Timestamp).Format(time.RFC3339), msg.Payload)
	}
}

func main() {
	mode := flag.String("mode", "", "Operation mode: 'beacon' or 'listen'")
	addr := flag.String("addr", "", "UDP address to send to or listen on (e.g., 127.0.0.1:9000, 224.0.0.1:9000)")
	id := flag.String("id", "", "Unique ID for the beacon sender (required in beacon mode)")
	payload := flag.String("payload", "", "Message payload for the beacon (required in beacon mode)")
	intervalStr := flag.String("interval", "5s", "Beacon broadcast interval (e.g., 1s, 10s, 1m) (required in beacon mode)")

	flag.Parse()

	if *mode == "" {
		fmt.Println("Error: --mode is required. Use 'beacon' or 'listen'.")
		flag.Usage()
		os.Exit(1)
	}

	if *addr == "" {
		fmt.Println("Error: --addr is required.")
		flag.Usage()
		os.Exit(1)
	}

	c := make(chan os.Signal, 1)
	signal.Notify(c, os.Interrupt, syscall.SIGTERM)

	switch *mode {
	case "beacon":
		if *id == "" || *payload == "" {
			fmt.Println("Error: --id and --payload are required in beacon mode.")
			flag.Usage()
			os.Exit(1)
		}
		interval, err := time.ParseDuration(*intervalStr)
		if err != nil {
			log.Fatalf("Invalid interval format: %v", err)
		}
		go startBeaconSender(*addr, interval, *id, *payload)
	case "listen":
		go startBeaconListener(*addr)
	default:
		fmt.Printf("Error: Unknown mode '%s'. Use 'beacon' or 'listen'.\n", *mode)
		flag.Usage()
		os.Exit(1)
	}

	<-c // Wait for interrupt signal
	log.Println("Shutting down...")
}
