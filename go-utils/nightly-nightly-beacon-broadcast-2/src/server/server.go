package server

import (
	"fmt"
	"log"
	"net"
	"nightly-beacon-broadcast/src/cipher"
)

const maxUDPBufferSize = 1024

// StartServer starts the UDP beacon server on the specified port.
// It sends decrypted messages to the receivedMessages channel for testing/monitoring.
// If receivedMessages is nil, messages are only logged.
func StartServer(port string, receivedMessages chan<- string) (*net.UDPConn, error) {
	addr, err := net.ResolveUDPAddr("udp", ":"+port)
	if err != nil {
		return nil, fmt.Errorf("failed to resolve UDP address: %w", err)
	}

	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		return nil, fmt.Errorf("failed to listen on UDP port %s: %w", port, err)
	}
	log.Printf("Beacon server listening on UDP port %s", port)

	go func() {
		defer conn.Close()
		for {
			buffer := make([]byte, maxUDPBufferSize)
			n, remoteAddr, err := conn.ReadFromUDP(buffer)
			if err != nil {
				// Check if the error is due to the connection being closed
				if opErr, ok := err.(*net.OpError); ok && opErr.Err.Error() == "use of closed network connection" {
					log.Println("Server connection closed, stopping listener.")
					return
				}
				log.Printf("Error reading from UDP: %v", err)
				continue
			}

			encryptedMsg := buffer[:n]
			decryptedMsg := cipher.Decrypt(encryptedMsg)
			msgStr := string(decryptedMsg)

			log.Printf("Received beacon from %s: \"%s\"", remoteAddr.String(), msgStr)
			if receivedMessages != nil {
				receivedMessages <- fmt.Sprintf("From %s: %s", remoteAddr.String(), msgStr)
			}
		}
	}()

	return conn, nil
}
