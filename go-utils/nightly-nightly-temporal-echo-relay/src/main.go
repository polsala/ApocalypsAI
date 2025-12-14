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
	"strconv"
	"strings"
	"sync"
	"time"
)

// Server configuration
type ServerConfig struct {
	Port        int
	Delay       time.Duration
	LossProb    float64
}

// Client configuration
type ClientConfig struct {
	Addr        string
	Messages    int
	Interval    time.Duration
}

func main() {
	rand.Seed(time.Now().UnixNano())

	serverCmd := flag.NewFlagSet("server", flag.ExitOnError)
	serverPort := serverCmd.Int("port", 8080, "Port to listen on")
	serverDelayStr := serverCmd.String("delay", "0s", "Artificial delay to introduce, e.g., 100ms, 1s")
	serverLossProb := serverCmd.Float64("loss", 0.0, "Probability of dropping a message (0.0 to 1.0)")

	clientCmd := flag.NewFlagSet("client", flag.ExitOnError)
	clientAddr := clientCmd.String("addr", "localhost:8080", "Address of the echo relay server")
	clientMessages := clientCmd.Int("messages", 5, "Number of messages to send")
	clientIntervalStr := clientCmd.String("interval", "1s", "Interval between sending messages, e.g., 200ms, 1s")

	if len(os.Args) < 2 {
		fmt.Println("Usage: echo-relay <command> [arguments]")
		fmt.Println("Commands:")
		fmt.Println("  server - Start the echo relay server")
		fmt.Println("  client - Start the echo relay client")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "server":
		serverCmd.Parse(os.Args[2:])
		serverDelay, err := time.ParseDuration(*serverDelayStr)
		if err != nil {
			log.Fatalf("Invalid delay duration: %v", err)
		}
		if *serverLossProb < 0.0 || *serverLossProb > 1.0 {
			log.Fatalf("Loss probability must be between 0.0 and 1.0")
		}
		config := ServerConfig{
			Port:        *serverPort,
			Delay:       serverDelay,
			LossProb:    *serverLossProb,
		}
		startServer(config)
	case "client":
		clientCmd.Parse(os.Args[2:])
		clientInterval, err := time.ParseDuration(*clientIntervalStr)
		if err != nil {
			log.Fatalf("Invalid interval duration: %v", err)
		}
		config := ClientConfig{
			Addr:        *clientAddr,
			Messages:    *clientMessages,
			Interval:    clientInterval,
		}
		startClient(config)
	default:
		fmt.Printf("Unknown command: %s\n", os.Args[1])
		fmt.Println("Run 'echo-relay' for usage.")
		os.Exit(1)
	}
}

func startServer(config ServerConfig) {
	listener, err := net.Listen("tcp", fmt.Sprintf(":%d", config.Port))
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
	defer listener.Close()

	log.Printf("Temporal Echo Relay Server listening on port %d with delay %s and loss probability %.2f", config.Port, config.Delay, config.LossProb)

	for {
		conn, err := listener.Accept()
		if err != nil {
			if !strings.Contains(err.Error(), "use of closed network connection") {
				log.Printf("Error accepting connection: %v", err)
			}
			continue
		}
		go handleConnection(conn, config)
	}
}

func handleConnection(conn net.Conn, config ServerConfig) {
	defer conn.Close()
	log.Printf("New connection from %s", conn.RemoteAddr())

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)

	for {
		message, err := reader.ReadString('\n')
		if err != nil {
			if err != io.EOF {
				log.Printf("Error reading from %s: %v", conn.RemoteAddr(), err)
			}
			break
		}

		message = strings.TrimSpace(message)
		log.Printf("Received from %s: \"%s\"", conn.RemoteAddr(), message)

		if rand.Float64() < config.LossProb {
			log.Printf("Message \"%s\" from %s dropped due to %.2f loss probability", message, conn.RemoteAddr(), config.LossProb)
			continue // Simulate packet loss
		}

		if config.Delay > 0 {
			time.Sleep(config.Delay)
			log.Printf("Applied %s delay for message \"%s\"", config.Delay, message)
		}

		echoMessage := fmt.Sprintf("Echo: %s\n", message)
		_, err = writer.WriteString(echoMessage)
		if err != nil {
			log.Printf("Error writing to %s: %v", conn.RemoteAddr(), err)
			break
		}
		writer.Flush()
		log.Printf("Sent echo to %s: \"%s\"", conn.RemoteAddr(), strings.TrimSpace(echoMessage))
	}
	log.Printf("Connection from %s closed", conn.RemoteAddr())
}

func startClient(config ClientConfig) {
	log.Printf("Temporal Echo Relay Client connecting to %s to send %d messages with %s interval", config.Addr, config.Messages, config.Interval)

	conn, err := net.Dial("tcp", config.Addr)
	if err != nil {
		log.Fatalf("Failed to connect to server: %v", err)
	}
	defer conn.Close()

	reader := bufio.NewReader(conn)
	writer := bufio.NewWriter(conn)

	for i := 1; i <= config.Messages; i++ {
		message := fmt.Sprintf("Hello from client #%d", i)
		start := time.Now()

		_, err := writer.WriteString(message + "\n")
		if err != nil {
			log.Printf("Error sending message #%d: %v", i, err)
			break
		}
		writer.Flush()
		log.Printf("Client sent: \"%s\"", message)

		conn.SetReadDeadline(time.Now().Add(config.Interval * 2 + 5 * time.Second)) // Give some buffer for delay + network
		received, err := reader.ReadString('\n')
		if err != nil {
			if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
				log.Printf("Message #%d timed out. Likely dropped or delayed too long.", i)
			} else {
				log.Printf("Error receiving response for message #%d: %v", i, err)
			}
		} else {
			duration := time.Since(start)
			log.Printf("Client received: \"%s\" (Latency: %s)", strings.TrimSpace(received), duration)
		}

		if i < config.Messages {
			time.Sleep(config.Interval)
		}
	}
	log.Println("Client finished sending messages.")
}
