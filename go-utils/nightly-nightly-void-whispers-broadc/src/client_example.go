package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run client_example.go <server_address:port>")
		os.Exit(1)
	}
	serverAddr := os.Args[1]

	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		log.Fatalf("Failed to connect to server %s: %v", serverAddr, err)
	}
	defer conn.Close()
	fmt.Printf("Connected to Void Whispers Broadcast Server at %s. Listening for whispers...\n", serverAddr)

	scanner := bufio.NewScanner(conn)
	for scanner.Scan() {
		fmt.Printf("Whisper received: %s\n", scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Printf("Error reading from server: %v", err)
	}
	fmt.Println("Disconnected from server.")
}
