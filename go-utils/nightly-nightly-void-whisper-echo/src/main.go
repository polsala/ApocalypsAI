package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"strconv"
)

const defaultPort = 8080
const echoPrefix = "The void echoes: "
const bufferSize = 1024 // Maximum size for UDP packets

func main() {
	portStr := os.Getenv("PORT")
	port := defaultPort
	if portStr != "" {
		p, err := strconv.Atoi(portStr)
		if err != nil {
			log.Printf("Warning: Invalid PORT environment variable '%s', using default port %d. Error: %v", portStr, defaultPort, err)
		} else {
			port = p
		}
	}

	addr := fmt.Sprintf(":%d", port)
	conn, err := net.ListenPacket("udp", addr)
	if err != nil {
		log.Fatalf("Failed to listen on UDP port %s: %v", addr, err)
	}
	defer conn.Close()

	log.Printf("Nightly Void Whisper Echo server listening on UDP %s", addr)

	buffer := make([]byte, bufferSize)
	for {
		n, clientAddr, err := conn.ReadFrom(buffer)
		if err != nil {
			log.Printf("Error reading UDP packet: %v", err)
			continue
		}

		receivedMsg := string(buffer[:n])
		log.Printf("Received %d bytes from %s: \"%s\"", n, clientAddr, receivedMsg)

		responseMsg := echoPrefix + receivedMsg
		// Ensure the response doesn't exceed UDP packet size limits if possible
		if len(responseMsg) > bufferSize {
			responseMsg = responseMsg[:bufferSize]
		}

		_, err = conn.WriteTo([]byte(responseMsg), clientAddr)
		if err != nil {
			log.Printf("Error writing UDP response to %s: %v", clientAddr, err)
		} else {
			log.Printf("Echoed to %s: \"%s\"", clientAddr, responseMsg)
		}
	}
}
