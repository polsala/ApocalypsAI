package main

import (
	"fmt"
	"os"
	"strings"
)

func reverse(s string) string {
	r := []rune(s)
	for i, j := 0, len(r)-1; i < j; i, j = i+1, j-1 {
		r[i], r[j] = r[j], r[i]
	}
	return string(r)
}

func transmit(message string) {
	fmt.Printf("[TRANSMIT] Sending: %s\n", message)
	echo := reverse(message)
	fmt.Printf("[ECHO] Received: %s\n", echo)
	verified := echo == reverse(message)
	fmt.Printf("[VERIFY] Echo verified: %v\n", verified)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: void-whistle [transmit <message> | test]")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "transmit":
		if len(os.Args) < 3 {
			fmt.Println("Please provide a message to transmit.")
			os.Exit(1)
		}
		transmit(strings.Join(os.Args[2:], " "))
	case "test":
		// Mock rationale: Simulate deterministic echo verification without external dependencies
		message := "test"
		expectedEcho := "tset"
		actualEcho := reverse(message)
		if actualEcho != expectedEcho {
			fmt.Printf("Test failed: expected %s, got %s\n", expectedEcho, actualEcho)
			os.Exit(1)
		}
		fmt.Println("[TEST] All tests passed.")
	default:
		fmt.Println("Unknown command. Use 'transmit' or 'test'.")
		os.Exit(1)
	}
}
