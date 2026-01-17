package main

import (
	"flag"
	"fmt"
	"net"
	"os"
)

func main() {
	var (
		message string
		group   string
		listen  bool
	)

	flag.StringVar(&message, "message", "", "Message to broadcast")
	flag.StringVar(&group, "group", "224.0.0.1:9999", "Multicast group address")
	flag.BoolVar(&listen, "listen", false, "Listen for messages")
	flag.Parse()

	addr, err := net.ResolveUDPAddr("udp", group)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to resolve address: %v\n", err)
		os.Exit(1)
	}

	if listen {
		listenForMessages(addr)
	} else {
		broadcastMessage(message, addr)
	}
}

func broadcastMessage(message string, addr *net.UDPAddr) {
	conn, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to dial UDP: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	_, err = conn.Write([]byte(message))
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to send message: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("Message sent: %s\n", message)
}

func listenForMessages(addr *net.UDPAddr) {
	conn, err := net.ListenMulticastUDP("udp", nil, addr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to listen: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close()

	fmt.Println("Listening for messages...")
	buffer := make([]byte, 1024)
	for {
		n, _, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Read error: %v\n", err)
			continue
		}
		fmt.Printf("Received: %s\n", string(buffer[:n]))
	}
}
