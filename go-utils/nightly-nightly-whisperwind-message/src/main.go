package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

const defaultPort = "8080"

type RelayRequest struct {
	Message json.RawMessage `json:"message"` // Allow any JSON structure
}

type RelayResult struct {
	URL    string `json:"url"`
	Status string `json:"status"`
	Error  string `json:"error,omitempty"`
}

type RelayResponse struct {
	Results []RelayResult `json:"results"`
}

var targetURLs []string

func init() {
	// Load target URLs from environment variable
	loadTargetURLsFromEnv()
}

// loadTargetURLsFromEnv is a helper to load/reload target URLs from the environment.
// This is useful for testing where environment variables might change.
func loadTargetURLsFromEnv() {
	urls := os.Getenv("TARGET_URLS")
	if urls == "" {
		log.Println("WARNING: TARGET_URLS environment variable not set. No messages will be relayed.")
		targetURLs = []string{}
	} else {
		targetURLs = strings.Split(urls, ",")
		for i, url := range targetURLs {
			targetURLs[i] = strings.TrimSpace(url)
		}
		log.Printf("Configured to relay messages to: %v\n", targetURLs)
	}
}

func relayHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST requests are accepted", http.StatusMethodNotAllowed)
		return
	}

	var req RelayRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Invalid JSON request body", http.StatusBadRequest)
		return
	}

	// Ensure targetURLs is up-to-date, especially for tests or dynamic reconfig (though not fully dynamic here)
	loadTargetURLsFromEnv()

	if len(targetURLs) == 0 {
		log.Println("No target URLs configured, skipping relay.")
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(RelayResponse{Results: []RelayResult{
			{URL: "N/A", Status: "skipped", Error: "No target URLs configured"},
		}})
		return
	}

	var wg sync.WaitGroup
	resultsChan := make(chan RelayResult, len(targetURLs))

	for _, url := range targetURLs {
		wg.Add(1)
		go func(targetURL string, message []byte) {
			defer wg.Done()
			result := relayMessage(targetURL, message)
			resultsChan <- result
		}(url, req.Message)
	}

	wg.Wait()
	close(resultsChan)

	var relayResults []RelayResult
	for res := range resultsChan {
		relayResults = append(relayResults, res)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(RelayResponse{Results: relayResults})
}

func relayMessage(targetURL string, message []byte) RelayResult {
	client := &http.Client{Timeout: 5 * time.Second} // Short timeout for relays
	req, err := http.NewRequest(http.MethodPost, targetURL, bytes.NewBuffer(message))
	if err != nil {
		log.Printf("Error creating request for %s: %v\n", targetURL, err)
		return RelayResult{URL: targetURL, Status: "failed", Error: fmt.Sprintf("Failed to create request: %v", err)}
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Error relaying message to %s: %v\n", targetURL, err)
		return RelayResult{URL: targetURL, Status: "failed", Error: fmt.Sprintf("Network error: %v", err)}
	}
	defer resp.Body.Close()

	body, _ := ioutil.ReadAll(resp.Body) // Read body for logging/debugging, ignore error
	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		log.Printf("Successfully relayed message to %s (Status: %d, Body: %s)\n", targetURL, resp.StatusCode, string(body))
		return RelayResult{URL: targetURL, Status: "success"}
	} else {
		log.Printf("Failed to relay message to %s (Status: %d, Body: %s)\n", targetURL, resp.StatusCode, string(body))
		return RelayResult{URL: targetURL, Status: "failed", Error: fmt.Sprintf("Target responded with status %d: %s", resp.StatusCode, string(body))}
	}
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = defaultPort
	}

	http.HandleFunc("/relay", relayHandler)

	log.Printf("Whisperwind Message Relay listening on :%s/relay\n", port)
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
