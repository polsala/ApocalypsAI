package client

import (
	"fmt"
	"net"
	"nightly-beacon-broadcast/src/cipher"
)

// SendMessage encrypts and sends a message to the specified UDP server address.
func SendMessage(serverAddr, message string) error {
	conn, err := net.Dial("udp", serverAddr)
	if err != nil {
		return fmt.Errorf("failed to dial UDP server %s: %w", serverAddr, err)
	}
	defer conn.Close()

	encryptedMsg := cipher.Encrypt([]byte(message))
	_, err = conn.Write(encryptedMsg)
	if err != nil {
		return fmt.Errorf("failed to send message: %w", err)
	}

	return nil
}
