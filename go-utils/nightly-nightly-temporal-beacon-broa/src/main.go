package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"sync"
	"time"
)

// BroadcastRequest represents the payload sent to a temporal relay.
type BroadcastRequest struct {
	Message string `json:"message"`
}

// BroadcastResponse represents the response received from a temporal relay.
type BroadcastResponse struct {
	Status           string  `json:"status"`
	TemporalDistortion float64 `json:"temporal_distortion"`
	RelayMessage     string  `json:"relay_message,omitempty"`
	Error            string  `json:"error,omitempty"`
}

// BroadcastResult stores the outcome for a single relay.
type BroadcastResult struct {
	RelayURL         string
	Success          bool
	TemporalDistortion float64
	RelayMessage     string
	Error            string
}

// HTTPClient interface for mocking HTTP requests.
type HTTPClient interface {
	Do(req *http.Request) (*http.Response, error)
}

// sendToRelay sends a message to a single temporal relay.
func sendToRelay(relayURL, message string, client HTTPClient) BroadcastResult {
	requestBody, err := json.Marshal(BroadcastRequest{Message: message})
	if err != nil {
		return BroadcastResult{RelayURL: relayURL, Success: false, Error: fmt.Sprintf("Failed to marshal request: %v", err)}
	}

	req, err := http.NewRequest("POST", relayURL, bytes.NewBuffer(requestBody))
	if err != nil {
		return BroadcastResult{RelayURL: relayURL, Success: false, Error: fmt.Sprintf("Failed to create request: %v", err)}
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		return BroadcastResult{RelayURL: relayURL, Success: false, Error: fmt.Sprintf("Failed to send request: %v", err)}
	}
	defer resp.Body.Close()

	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return BroadcastResult{RelayURL: relayURL, Success: false, Error: fmt.Sprintf("Failed to read response body: %v", err)}
	}

	if resp.StatusCode != http.StatusOK {
		return BroadcastResult{RelayURL: relayURL, Success: false, Error: fmt.Sprintf("Relay responded with status %d: %s", resp.StatusCode, string(bodyBytes))}
	}

	var response BroadcastResponse
	if err := json.Unmarshal(bodyBytes, &response); err != nil {
		return BroadcastResult{RelayURL: relayURL, Success: false, Error: fmt.Sprintf("Failed to unmarshal response: %v, Body: %s", err, string(bodyBytes))}
	}

	return BroadcastResult{
		RelayURL:         relayURL,
		Success:          true,
		TemporalDistortion: response.TemporalDistortion,
		RelayMessage:     response.RelayMessage,
		Error:            response.Error,
	}
}

// Broadcast sends a message concurrently to multiple temporal relays.
func Broadcast(message string, relayURLs []string, httpClient HTTPClient) []BroadcastResult {
	var wg sync.WaitGroup
	resultsChan := make(chan BroadcastResult, len(relayURLs))

	for _, url := range relayURLs {
		wg.Add(1)
		go func(url string) {
			defer wg.Done()
			result := sendToRelay(url, message, httpClient)
			resultsChan <- result
		}(url)
	}

	wg.Wait()
	close(resultsChan)

	var results []BroadcastResult
	for res := range resultsChan {
		results = append(results, res)
	}
	return results
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: nightly-temporal-beacon-broadcaster <message> <relay_url_1> [relay_url_2 ...]")
		os.Exit(1)
	}

	message := os.Args[1]
	relayURLs := os.Args[2:]

	fmt.Printf("Broadcasting message \"%s\" to %d temporal relays...\n", message, len(relayURLs))

	// Use a default HTTP client with a timeout for actual network calls
	defaultHTTPClient := &http.Client{Timeout: 5 * time.Second}
	results := Broadcast(message, relayURLs, defaultHTTPClient)

	fmt.Println("\n--- Broadcast Results ---")
	for _, res := range results {
		if res.Success {
			fmt.Printf("  [SUCCESS] Relay: %s, Distortion: %.2f, Message: \"%s\"\n", res.RelayURL, res.TemporalDistortion, res.RelayMessage)
		} else {
			fmt.Printf("  [FAILURE] Relay: %s, Error: %s\n", res.RelayURL, res.Error)
		}
	}
}
