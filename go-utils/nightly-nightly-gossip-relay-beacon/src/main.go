package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"strings"
	"sync"
	"time"
)

var ()

func main() {
	port := flag.String("port", "8080", "Port for the beacon to listen on")
	peersStr := flag.String("peers", "", "Comma-separated list of peer addresses (host:port)")
	flag.Parse()

	peers := []string{}
	if *peersStr != "" {
		peers = strings.Split(*peersStr, ",")
	}

	log.Printf("Gossip Relay Beacon starting on port %s with peers: %v\n", *port, peers)
	startServer(*port, peers)
}

// startServer initializes and starts the TCP server.
func startServer(port string, peers []string) {
	listener, err := net.Listen("tcp", ":"+port)
	if err != nil {
		log.Fatalf("Failed to listen on port %s: %v\n", port, err)
	}
	defer listener.Close()

	log.Printf("Listening for whispers on :%s\n", port)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v\n", err)
			continue
		}
		go handleConnection(conn, peers)
	}
}

// handleConnection reads a message from an incoming connection and relays it to peers.
func handleConnection(conn net.Conn, peers []string) {
	defer conn.Close()

	reader := bufio.NewReader(conn)
	message, err := reader.ReadString('\n')
	if err != nil {
		log.Printf("Error reading message from %s: %v\n", conn.RemoteAddr(), err)
		return
	}

	message = strings.TrimSpace(message)
	if message == "" {
		return // Ignore empty messages
	}

	log.Printf("Received whisper from %s: \"%s\"\n", conn.RemoteAddr(), message)

	// Relay the message to all known peers concurrently
	if len(peers) > 0 {
		var wg sync.WaitGroup
		for _, peerAddr := range peers {
			wg.Add(1)
			go func(addr, msg string) {
				defer wg.Done()
				relayMessage(addr, msg)
			}(peerAddr, message)
		}
		wg.Wait()
	}
}

// relayMessage attempts to send a message to a single peer.
func relayMessage(peerAddr, message string) {
	conn, err := net.DialTimeout("tcp", peerAddr, 2*time.Second)
	if err != nil {
		log.Printf("Failed to connect to peer %s: %v\n", peerAddr, err)
		return
	}
	defer conn.Close()

	_, err = fmt.Fprintf(conn, "%s\n", message)
	if err != nil {
		log.Printf("Failed to send whisper to peer %s: %v\n", peerAddr, err)
		return
	}
	log.Printf("Relayed whisper to %s: \"%s\"\n", peerAddr, message)
}
