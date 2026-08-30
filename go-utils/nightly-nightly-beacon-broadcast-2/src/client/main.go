package main

import (
	"flag"
	"log"
	"nightly-beacon-broadcast/src/client"
)

func main() {
	serverAddr := flag.String("server", "127.0.0.1:8080", "The address (IP:Port) of the beacon server")
	message := flag.String("message", "", "The message to send as a beacon")
	flag.Parse()

	if *message == "" {
		log.Fatal("Message cannot be empty. Use --message \"Your message here\"")
	}

	err := client.SendMessage(*serverAddr, *message)
	if err != nil {
		log.Fatalf("Failed to send beacon message: %v", err)
	}

	log.Printf("Beacon message sent to %s: \"%s\"", *serverAddr, *message)
}
