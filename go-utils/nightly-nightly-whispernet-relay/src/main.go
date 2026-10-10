package main

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// Config holds the application configuration
type Config struct {
	Port            string
	TargetURLs      []string
	RetryAttempts   int
	RetryDelaySecs  int
}

// Default configuration values
const (
	defaultPort            = "8080"
	defaultRetryAttempts   = 3
	defaultRetryDelaySecs  = 1
)

// httpClient is used for making HTTP requests. Can be mocked in tests.
var httpClient *http.Client = &http.Client{Timeout: 10 * time.Second}

func main() {
	config := loadConfig()

	http.HandleFunc("/relay", func(w http.ResponseWriter, r *http.Request) {
		handleRelay(w, r, config)
	})
	http.HandleFunc("/status", handleStatus)

	log.Printf("WhisperNet Relay starting on port %s...", config.Port)
	log.Printf("Target URLs: %s", strings.Join(config.TargetURLs, ", "))
	log.Printf("Retry Attempts: %d, Initial Retry Delay: %d seconds", config.RetryAttempts, config.RetryDelaySecs)

	err := http.ListenAndServe(":"+config.Port, nil)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}

// loadConfig loads configuration from environment variables
func loadConfig() Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	targetURLsStr := os.Getenv("TARGET_URLS")
	if targetURLsStr == "" {
		log.Fatal("TARGET_URLS environment variable is required (comma-separated list of URLs)")
	}
	targetURLs := strings.Split(targetURLsStr, ",")
	for i := range targetURLs {
		targetURLs[i] = strings.TrimSpace(targetURLs[i])
	}

	retryAttemptsStr := os.Getenv("RETRY_ATTEMPTS")
	retryAttempts, err := strconv.Atoi(retryAttemptsStr)
	if err != nil || retryAttempts <= 0 {
		retryAttempts = defaultRetryAttempts
	}

	retryDelaySecsStr := os.Getenv("RETRY_DELAY_SECONDS")
	retryDelaySecs, err := strconv.Atoi(retryDelaySecsStr)
	if err != nil || retryDelaySecs <= 0 {
		retryDelaySecs = defaultRetryDelaySecs
	}

	return Config{
		Port:            port,
		TargetURLs:      targetURLs,
		RetryAttempts:   retryAttempts,
		RetryDelaySecs:  retryDelaySecs,
	}
}

// handleRelay processes incoming messages and dispatches them to targets
func handleRelay(w http.ResponseWriter, r *http.Request, config Config) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is supported", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	if len(body) == 0 {
		http.Error(w, "Request body cannot be empty", http.StatusBadRequest)
		return
	}

	log.Printf("Received message for relay: %s", string(body))

	// Dispatch message to all targets concurrently
	go relayMessage(body, config.TargetURLs, config.RetryAttempts, config.RetryDelaySecs)

	w.WriteHeader(http.StatusOK)
	fmt.Fprint(w, "Message received and queued for relay.")
}

// handleStatus provides a simple health check endpoint
func handleStatus(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "WhisperNet Relay is operational.")
}

// relayMessage dispatches a message to multiple target URLs concurrently
func relayMessage(message []byte, targetURLs []string, maxRetries, initialDelaySecs int) {
	var wg sync.WaitGroup
	for _, targetURL := range targetURLs {
		wg.Add(1)
		go func(url string) {
			defer wg.Done()
			sendToTarget(message, url, maxRetries, initialDelaySecs)
		}(targetURL)
	}
	wg.Wait() // Wait for all goroutines to finish their initial send/retry cycles
	log.Println("All relay attempts completed for message.")
}

// sendToTarget attempts to send a message to a single target URL with retries
func sendToTarget(message []byte, targetURL string, maxRetries, initialDelaySecs int) {
	currentDelay := time.Duration(initialDelaySecs) * time.Second
	for i := 0; i < maxRetries; i++ {
		log.Printf("Attempt %d to send message to %s", i+1, targetURL)
		req, err := http.NewRequest(http.MethodPost, targetURL, bytes.NewReader(message))
		if err != nil {
			log.Printf("Error creating request for %s: %v", targetURL, err)
			break // Unrecoverable error
		}
		req.Header.Set("Content-Type", "text/plain")

		resp, err := httpClient.Do(req)
		if err != nil {
			log.Printf("Error sending message to %s: %v. Retrying in %v...", targetURL, err, currentDelay)
			time.Sleep(currentDelay)
			currentDelay *= 2 // Exponential backoff
			continue
		}
		defer resp.Body.Close()

		if resp.StatusCode >= 200 && resp.StatusCode < 300 {
			log.Printf("Successfully relayed message to %s (Status: %d)", targetURL, resp.StatusCode)
			return
		}

		log.Printf("Failed to relay message to %s (Status: %d). Retrying in %v...", targetURL, resp.StatusCode, currentDelay)
		time.Sleep(currentDelay)
		currentDelay *= 2 // Exponential backoff
	}
	log.Printf("Failed to relay message to %s after %d attempts.", targetURL, maxRetries)
}
