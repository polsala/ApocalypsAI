package main

import (
	"flag"
	"fmt"
	"math/rand"
	"strings"
	"sync"
	"time"
)

var (
	nodes = flag.Int("nodes", 3, "Number of simulated network nodes")
	delay = flag.Duration("delay", 100*time.Millisecond, "Base network delay per node")
	loss  = flag.Int("loss", 5, "Simulated packet loss percentage")
)

func main() {
	flag.Parse()
	seedMessages := []string{
		"Echo from the void...",
		"Whispers in the wasteland...",
		"Signal from the beyond...",
		"Ripple through time...",
	}

	message := seedMessages[rand.Intn(len(seedMessages))]
	fmt.Printf("[Broadcaster] Transmitting: %q\n", message)

	var wg sync.WaitGroup
	for i := 1; i <= *nodes; i++ {
		wg.Add(1)
		go func(nodeID int) {
			defer wg.Done()
			transmit(nodeID, message)
		}(i)
	}
	wg.Wait()
}

func transmit(nodeID int, message string) {
	// Simulate network delay
	d := time.Duration(rand.Int63n(int64(*delay * 2)))
	time.Sleep(d)

	// Simulate packet loss
	if rand.Intn(100) < *loss {
		fmt.Printf("[Node %d] Packet lost\n", nodeID)
		return
	}

	// Simulate receiving message
	if strings.Contains(message, "void") {
		message = strings.Replace(message, "void", "void [repeated]", 1)
	}

	fmt.Printf("[Node %d] Received: %q (delay: %v)\n", nodeID, message, d)
}
