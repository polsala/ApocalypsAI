package main

import (
	"flag"
	"log"
	"nightly-beacon-broadcast/src/server"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	port := flag.String("port", "8080", "The UDP port to listen on")
	flag.Parse()

	// Channel for received messages is nil for the main application, used by tests.
	serverConn, err := server.StartServer(*port, nil)
	if err != nil {
		log.Fatalf("Failed to start beacon server: %v", err)
	}
	defer serverConn.Close()

	// Keep the server running until an interrupt signal is received
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	log.Println("Shutting down beacon server...")
}
