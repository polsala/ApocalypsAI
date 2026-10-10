package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"time"
)

func main() {
	serverAddr := flag.String("serverAddr", "localhost:8080", "Chronos Courier server address (host:port)")
	flag.Parse()

	conn, err := net.Dial("tcp", *serverAddr)
	if err != nil {
		log.Fatalf("Failed to connect to server %s: %v", *serverAddr, err)
	}
	defer conn.Close()

	log.Printf("Connected to Chronos Courier at %s", *serverAddr)

	// Goroutine to read incoming messages from the server
	go func() {
		scanner := bufio.NewScanner(conn)
		for scanner.Scan() {
			fmt.Printf("\n[RECEIVED]: %s\n> ", scanner.Text())
		}
		if err := scanner.Err(); err != nil {
			log.Printf("Error reading from server: %v", err)
		}
		log.Println("Server connection closed.")
		os.Exit(0)
	}()

	// Send some example messages
	messages := []string{
		"Hello from the present!",
		"DELAY=2s:This message will appear in 2 seconds.",
		"Another immediate thought.",
		"DELAY=5s:A message from 5 seconds into the future!",
		"Final immediate message.",
	}

	writer := bufio.NewWriter(conn)

	for i, msg := range messages {
		fmt.Printf("> Sending: %s\n", msg)
		_, err := writer.WriteString(msg + "\n")
		if err != nil {
			log.Fatalf("Failed to send message %d: %v", i, err)
		}
		writer.Flush()
		time.Sleep(500 * time.Millisecond) // Small pause between sends
	}

	fmt.Println("Sent all initial messages. Waiting for incoming messages...")

	// Keep the main goroutine alive to receive messages
	select {}
}
