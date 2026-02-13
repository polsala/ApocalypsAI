package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/spf13/pflag"
)

// GossipMessage represents a message exchanged between goblins.
type GossipMessage struct {
	Sender    string    `json:"sender"`
	Content   string    `json:"content"`
	Timestamp time.Time `json:"timestamp"`
}

// GossipGoblin represents a single node in the gossip network.
type GossipGoblin struct {
	Addr      string
	Peers     []string
	MessageLog []GossipMessage
	logMutex  sync.Mutex
	httpClient *http.Client
}

// NewGossipGoblin creates a new GossipGoblin instance.
func NewGossipGoblin(addr string, peers []string) *GossipGoblin {
	return &GossipGoblin{
		Addr:      addr,
		Peers:     peers,
		MessageLog: make([]GossipMessage, 0),
		httpClient: &http.Client{Timeout: 5 * time.Second},
	}
}

// StartServer initializes and starts the HTTP server for the goblin.
func (gg *GossipGoblin) StartServer() {
	http.HandleFunc("/gossip", gg.handleGossip)
	log.Printf("Gossip Goblin listening on %s\n", gg.Addr)
	log.Fatal(http.ListenAndServe(gg.Addr, nil))
}

// handleGossip processes incoming gossip messages.
func (gg *GossipGoblin) handleGossip(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	var msg GossipMessage
	err := json.NewDecoder(r.Body).Decode(&msg)
	if err != nil {
		http.Error(w, "Invalid message format", http.StatusBadRequest)
		return
	}

	gg.logMessage(msg)
	log.Printf("[%s] Received gossip from %s: %s\n", gg.Addr, msg.Sender, msg.Content)

	// Asynchronously propagate the message to peers
	go gg.propagateGossip(msg)

	w.WriteHeader(http.StatusOK)
}

// logMessage adds a message to the goblin's local log.
func (gg *GossipGoblin) logMessage(msg GossipMessage) {
	gg.logMutex.Lock()
	defer gg.logMutex.Unlock()
	gg.MessageLog = append(gg.MessageLog, msg)
}

// propagateGossip sends a message to all known peers.
func (gg *GossipGoblin) propagateGossip(msg GossipMessage) {
	msg.Sender = gg.Addr // Ensure sender is current goblin for propagation
	for _, peer := range gg.Peers {
		if peer == gg.Addr { // Don't gossip to self
			continue
		}
		go func(peerURL string) {
			log.Printf("[%s] Gossiping to %s: %s\n", gg.Addr, peerURL, msg.Content)
			jsonMsg, err := json.Marshal(msg)
			if err != nil {
				log.Printf("[%s] Error marshalling message for %s: %v\n", gg.Addr, peerURL, err)
				return
			}

			ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer cancel()

			req, err := http.NewRequestWithContext(ctx, http.MethodPost, peerURL+"/gossip", bytes.NewBuffer(jsonMsg))
			if err != nil {
				log.Printf("[%s] Error creating request for %s: %v\n", gg.Addr, peerURL, err)
				return
			}
			req.Header.Set("Content-Type", "application/json")

			res, err := gg.httpClient.Do(req)
			if err != nil {
				log.Printf("[%s] Error gossiping to %s: %v\n", gg.Addr, peerURL, err)
				return
			}
			defer res.Body.Close()

			if res.StatusCode != http.StatusOK {
				body, _ := ioutil.ReadAll(res.Body)
				log.Printf("[%s] Failed to gossip to %s, status: %d, body: %s\n", gg.Addr, peerURL, res.StatusCode, string(body))
			}
		}(peer)
	}
}

// sendMessage sends a message from a client to a target goblin.
func sendMessage(targetURL, content string) error {
	msg := GossipMessage{
		Sender:    "client", // Or could be derived from hostname/user
		Content:   content,
		Timestamp: time.Now(),
	}

	jsonMsg, err := json.Marshal(msg)
	if err != nil {
		return fmt.Errorf("error marshalling message: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, targetURL+"/gossip", bytes.NewBuffer(jsonMsg))
	if err != nil {
		return fmt.Errorf("error creating request: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	hc := &http.Client{Timeout: 5 * time.Second}
	res, err := hc.Do(req)
	if err != nil {
		return fmt.Errorf("error sending message to %s: %w", targetURL, err)
	}
	defer res.Body.Close()

	if res.StatusCode != http.StatusOK {
		body, _ := ioutil.ReadAll(res.Body)
		return fmt.Errorf("failed to send message to %s, status: %d, body: %s", targetURL, res.StatusCode, string(body))
	}

	log.Printf("Message '%s' sent successfully to %s\n", content, targetURL)
	return nil
}

func main() {
	var port int
	var peersStr string
	var targetURL string
	var messageContent string

	serverCmd := pflag.NewFlagSet("server", pflag.ExitOnError)
	serverCmd.IntVar(&port, "port", 8080, "Port for the goblin server to listen on")
	serverCmd.StringVar(&peersStr, "peers", "", "Comma-separated list of peer URLs (e.g., http://localhost:8081)")

	sendCmd := pflag.NewFlagSet("send", pflag.ExitOnError)
	sendCmd.StringVar(&targetURL, "target", "", "URL of the target goblin server (e.g., http://localhost:8080)")
	sendCmd.StringVar(&messageContent, "message", "", "Content of the gossip message")

	if len(os.Args) < 2 {
		fmt.Println("Usage: gossip-goblin <command> [flags]")
		fmt.Println("Commands:")
		fmt.Println("  server  Start a gossip goblin server")
		fmt.Println("  send    Send a message to a gossip goblin")
		os.Exit(1)
	}

	command := os.Args[1]
	switch command {
	case "server":
		serverCmd.Parse(os.Args[2:])
		if port == 0 {
			log.Fatal("Port must be specified for server mode.")
		}
		addr := fmt.Sprintf(":%d", port)
		var peers []string
		if peersStr != "" {
			peers = strings.Split(peersStr, ",")
		}
		
		// Remove self from peers list if present
		filteredPeers := []string{}
		for _, p := range peers {
			if !strings.HasSuffix(p, addr) {
				filteredPeers = append(filteredPeers, p)
			}
		}

		goblin := NewGossipGoblin(addr, filteredPeers)
		goblin.StartServer()
	case "send":
		sendCmd.Parse(os.Args[2:])
		if targetURL == "" || messageContent == "" {
			log.Fatal("Target URL and message content must be specified for send mode.")
		}
		err := sendMessage(targetURL, messageContent)
		if err != nil {
			log.Fatalf("Failed to send message: %v\n", err)
		}
	default:
		fmt.Printf("Unknown command: %s\n", command)
		os.Exit(1)
	}
}
