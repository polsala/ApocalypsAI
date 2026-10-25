package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"log"
	"math/rand"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

// Global sleep function for mocking in tests
var sleep = time.Sleep

// TemporalEffects holds the configuration for network and temporal distortions.
type TemporalEffects struct {
	Latency             time.Duration
	PacketLossProb      float64
	DistortionIntensity int
	Rand                *rand.Rand // Injectable random source for determinism in tests
}

func main() {
	// Subcommands for server and client
	serverCmd := flag.NewFlagSet("server", flag.ExitOnError)
	serverPort := serverCmd.Int("port", 8080, "Port for the server to listen on")
	serverLatency := serverCmd.Duration("latency", 0, "Simulated delay for each message (e.g., 100ms, 2s)")
	serverPacketLossProb := serverCmd.Float64("packet-loss-prob", 0.0, "Probability (0.0 to 1.0) of a message being 'lost'")
	serverDistortionIntensity := serverCmd.Int("distortion-intensity", 0, "Level of temporal distortion (0 = none, 1 = light, 2 = moderate, 3 = heavy)")

	clientCmd := flag.NewFlagSet("client", flag.ExitOnError)
	clientHost := clientCmd.String("host", "localhost", "Hostname or IP address of the server")
	clientPort := clientCmd.Int("port", 8080, "Port of the server")
	clientMessage := clientCmd.String("message", "", "Message to send to the server")

	if len(os.Args) < 2 {
		fmt.Println("Usage: chronal-chatterbox <command> [arguments]")
		fmt.Println("Commands:")
		fmt.Println("  server - Start the chronal chatterbox server")
		fmt.Println("  client - Send a message to the chronal chatterbox server")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "server":
		serverCmd.Parse(os.Args[2:])
		te := &TemporalEffects{
			Latency:             *serverLatency,
			PacketLossProb:      *serverPacketLossProb,
			DistortionIntensity: *serverDistortionIntensity,
			Rand:                rand.New(rand.NewSource(time.Now().UnixNano())),
		}
		startServer(*serverPort, te)
	case "client":
		clientCmd.Parse(os.Args[2:])
		if *clientMessage == "" {
			log.Fatal("Client message cannot be empty")
		}
		startClient(*clientHost, *clientPort, *clientMessage)
	default:
		fmt.Printf("Unknown command: %s\n", os.Args[1])
		os.Exit(1)
	}
}

func startServer(port int, te *TemporalEffects) {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", port))
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
	defer listener.Close()
	log.Printf("Chronal Chatterbox server listening on port %d with latency=%v, packet_loss_prob=%.2f, distortion_intensity=%d",
		port, te.Latency, te.PacketLossProb, te.DistortionIntensity)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v", err)
			continue
		}
		go handleConnection(conn, te)
	}
}

func handleConnection(conn net.Conn, te *TemporalEffects) {
	defer conn.Close()
	log.Printf("Handling connection from %s", conn.RemoteAddr())

	reader := bufio.NewReader(conn)
	message, err := reader.ReadString('\n')
	if err != nil {
		if err != io.EOF {
			log.Printf("Error reading from connection %s: %v", conn.RemoteAddr(), err)
		}
		return
	}

	message = strings.TrimSpace(message)
	log.Printf("Received from %s: %q", conn.RemoteAddr(), message)

	// Apply temporal effects
	if te.Latency > 0 {
		sleep(te.Latency)
	}

	response, lost := te.applyPacketLoss(message)
	if lost {
		log.Printf("Message from %s lost due to simulated packet loss.", conn.RemoteAddr())
		return // Don't send a response
	}

	response = te.applyTemporalDistortion(response)

	// Send response
	_, err = conn.Write([]byte(response + "\n"))
	if err != nil {
		log.Printf("Error writing to connection %s: %v", conn.RemoteAddr(), err)
	}
	log.Printf("Sent to %s: %q", conn.RemoteAddr(), response)
}

func startClient(host string, port int, message string) {
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", host, port))
	if err != nil {
		log.Fatalf("Failed to connect to server: %v", err)
	}
	defer conn.Close()

	log.Printf("Connected to %s:%d", host, port)

	// Send message
	_, err = conn.Write([]byte(message + "\n"))
	if err != nil {
		log.Fatalf("Error sending message: %v", err)
	}
	log.Printf("Sent: %q", message)

	// Read response
	reader := bufio.NewReader(conn)
	response, err := reader.ReadString('\n')
	if err != nil {
		if err == io.EOF {
			fmt.Println("Connection closed by server (possibly due to packet loss).")
			return
		}
		log.Fatalf("Error reading response: %v", err)
	}

	fmt.Printf("Received echo: %q\n", strings.TrimSpace(response))
}

// applyPacketLoss determines if a message is lost based on probability.
func (te *TemporalEffects) applyPacketLoss(message string) (string, bool) {
	if te.PacketLossProb > 0 && te.Rand.Float64() < te.PacketLossProb {
		return "", true // Message lost
	}
	return message, false // Message not lost
}

// applyTemporalDistortion applies various distortions based on intensity.
func (te *TemporalEffects) applyTemporalDistortion(message string) string {
	if te.DistortionIntensity == 0 || len(message) < 2 {
		return message
	}

	runes := []rune(message)
	numDistortions := te.DistortionIntensity

	for i := 0; i < numDistortions; i++ {
		switch te.Rand.Intn(3) { // 0: swap, 1: insert, 2: delete
		case 0: // Swap two random characters
			if len(runes) >= 2 {
				a := te.Rand.Intn(len(runes))
				b := te.Rand.Intn(len(runes))
				runes[a], runes[b] = runes[b], runes[a]
			}
		case 1: // Insert a random character from the message at a random position
			if len(runes) > 0 {
				insertChar := runes[te.Rand.Intn(len(runes))]
				insertPos := te.Rand.Intn(len(runes) + 1)
				runes = append(runes[:insertPos], append([]rune{insertChar}, runes[insertPos:]...)...)
			}
		case 2: // Delete a random character
			if len(runes) > 0 {
				deletePos := te.Rand.Intn(len(runes))
				runes = append(runes[:deletePos], runes[deletePos+1:]...)
			}
		}
	}

	return string(runes)
}
