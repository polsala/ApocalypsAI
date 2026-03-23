package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

// exitFunc is a variable to allow mocking os.Exit in tests.
var exitFunc = os.Exit

// applyEcho applies a temporal echo effect to the message.
// For deterministic testing, it reverses the first two words (if present)
// and appends "(echo)" based on the echoLevel.
func applyEcho(message string, echoLevel int) string {
	parts := strings.Fields(message)
	if len(parts) >= 2 {
		// Deterministic distortion: reverse first two words
		parts[0], parts[1] = parts[1], parts[0]
	}

	echoedMessage := strings.Join(parts, " ")

	for i := 0; i < echoLevel; i++ {
		echoedMessage += " (echo)"
	}
	return echoedMessage
}

// simulateForward prints the echoed message and the next hop.
func simulateForward(echoedMessage, nextHop string) {
	fmt.Printf("Relaying message: \"%s\"\n", echoedMessage)
	fmt.Printf("Next hop: %s\n", nextHop)
}

// run contains the main logic of the CLI tool, returning an exit code.
func run() int {
	messagePtr := flag.String("message", "", "The message to send through the echo network.")
	echoLevelPtr := flag.Int("level", 1, "The echo level (integer, 0 for no echo, 1 for basic, etc.).")
	nextHopPtr := flag.String("next-hop", "Unknown Relay", "The simulated next relay node or final recipient.")

	flag.Parse()

	if *messagePtr == "" {
		fmt.Println("Error: A message is required. Use -message \"Your message here\".")
		flag.Usage()
		return 1 // Indicate error
	}

	echoed := applyEcho(*messagePtr, *echoLevelPtr)
	simulateForward(echoed, *nextHopPtr)
	return 0 // Indicate success
}

func main() {
	code := run()
	exitFunc(code)
}
