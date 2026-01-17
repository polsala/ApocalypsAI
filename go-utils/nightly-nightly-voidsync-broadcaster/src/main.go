package main

import (
	"flag"
	"fmt"
	"net"
	"time"
)

func main() {
	var (
		message = flag.String("message", "ping", "Message to broadcast")
		group  = flag.String("group", "224.0.0.1:9999", "Multicast group address")
	)
	flag.Parse()

	addr, err := net.ResolveUDPAddr("udp", *group)
	if err != nil {
		fmt.Println("Failed to resolve address:", err)
		return
	}

	conn, err := net.DialUDP("udp", nil, addr)
	if err != nil {
		fmt.Println("Failed to dial UDP:", err)
		return
	}
	defer conn.Close()

	conn.SetWriteDeadline(time.Now().Add(5 * time.Second))

	_, err = conn.Write([]byte(*message))
	if err != nil {
		fmt.Println("Failed to send message:", err)
		return
	}

	fmt.Printf("Sent: %s to %s\n", *message, *group)
}
