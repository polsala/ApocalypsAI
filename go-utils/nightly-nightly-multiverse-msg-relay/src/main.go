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

var (
	listenAddr   string
	destinations string
)

func init() {
	flag.StringVar(&listenAddr, "listen", ":8080", "Address for the relay to listen on (e.g., :8080)")
	flag.StringVar(&destinations, "destinations", "", "Comma-separated list of destination addresses (e.g., :8081,:8082)")
}

func main() {
	flag.Parse()

	if destinations == "" {
		log.Fatal("Error: --destinations flag is required.")
	}

	log.Printf("Starting Multiverse Message Relay on %s", listenAddr)
	log.Printf("Broadcasting to dimensions: %s", destinations)

	listener, err := net.Listen("tcp", listenAddr)
	if err != nil {
		log.Fatalf("Failed to start listener: %v", err)
	}
	defer listener.Close()

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v", err)
			continue
		}
		go handleConnection(conn, strings.Split(destinations, ","))
	}
}

func handleConnection(conn net.Conn, destAddrs []string) {
	defer conn.Close()
	log.Printf("Received connection from %s", conn.RemoteAddr())

	message, err := bufio.NewReader(conn).ReadString('\n')
	if err != nil {
		log.Printf("Error reading message from %s: %v", conn.RemoteAddr(), err)
		return
	}
	message = strings.TrimSpace(message)
	log.Printf("Relaying message: \"%s\"", message)

	var wg sync.WaitGroup
	for _, dest := range destAddrs {
		wg.Add(1)
		go func(d string) {
			defer wg.Done()
			broadcastMessage(d, message)
		}(dest)
	}
	wg.Wait()
	log.Printf("Message \"%s\" relayed to all dimensions.", message)
}

func broadcastMessage(destAddr string, message string) {
	conn, err := net.DialTimeout("tcp", destAddr, 2*time.Second) // Add a timeout for dialing
	if err != nil {
		log.Printf("Failed to connect to dimension %s: %v", destAddr, err)
		return
	}
	defer conn.Close()

	_, err = fmt.Fprintf(conn, "%s\n", message)
	if err != nil {
		log.Printf("Failed to send message to dimension %s: %v", destAddr, err)
		return
	}
	log.Printf("Successfully relayed to dimension %s", destAddr)
}
