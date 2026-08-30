package main

import (
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// HTTPClient defines an interface for making HTTP GET requests.
// This allows for easy mocking in tests.
type HTTPClient interface {
	Get(url string) (*http.Response, error)
}

// RealHTTPClient implements HTTPClient using the standard http.Client.
type RealHTTPClient struct {
	Client *http.Client
}

// Get performs an HTTP GET request.
func (c *RealHTTPClient) Get(url string) (*http.Response, error) {
	return c.Client.Get(url)
}

// RippleResult holds the outcome of a single ripple check.
type RippleResult struct {
	URL     string
	Status  string
	Latency time.Duration
	Error   error
}

// checkRipple sends a 'temporal ping' (HTTP GET) to a given URL
// and reports its status and latency via a channel.
func checkRipple(client HTTPClient, url string, results chan<- RippleResult, wg *sync.WaitGroup) {
	defer wg.Done()

	start := time.Now()
	resp, err := client.Get(url)
	latency := time.Since(start)

	if err != nil {
		// Check for specific network errors like timeout or connection refused
		errorMsg := err.Error()
		if strings.Contains(errMsg, "context deadline exceeded") || strings.Contains(errMsg, "timeout") {
			results <- RippleResult{URL: url, Status: "TIMEOUT", Latency: latency, Error: err}
		} else if strings.Contains(errMsg, "connection refused") || strings.Contains(errMsg, "no such host") || strings.Contains(errMsg, "dial tcp") {
			results <- RippleResult{URL: url, Status: "FAILED", Latency: latency, Error: err}
		} else {
			results <- RippleResult{URL: url, Status: "ERROR", Latency: latency, Error: err}
		}
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		results <- RippleResult{URL: url, Status: "OK", Latency: latency}
	} else {
		results <- RippleResult{URL: url, Status: fmt.Sprintf("ERROR %d", resp.StatusCode), Latency: latency}
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: reality-ripple-monitor <URL1> [URL2] ...")
		os.Exit(1)
	}

	urls := os.Args[1:]
	fmt.Printf("Monitoring %d endpoints...\n\n", len(urls))

	// Configure a real HTTP client with a reasonable timeout
	client := &RealHTTPClient{
		Client: &http.Client{
			Timeout: 5 * time.Second,
		},
	}

	var wg sync.WaitGroup
	results := make(chan RippleResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go checkRipple(client, url, results, &wg)
	}

	wg.Wait() // Wait for all goroutines to complete
	close(results) // Close the channel once all results are sent

	fmt.Println("--- Reality Ripple Report ---")

	allOK := true
	for res := range results {
		if res.Error != nil {
			fmt.Printf("[%s] %s (Error: %v) (Latency: %.2fms)\n", res.Status, res.URL, res.Error, float64(res.Latency)/float64(time.Millisecond))
			allOK = false
		} else {
			fmt.Printf("[%s] %s (Latency: %.2fms)\n", res.Status, res.URL, float64(res.Latency)/float64(time.Millisecond))
			if res.Status != "OK" {
				allOK = false
			}
		}
	}

	fmt.Println("")
	if allOK {
		fmt.Println("Overall Status: All ripples are stable.")
	} else {
		fmt.Println("Overall Status: Some ripples are unstable.")
		os.Exit(1)
	}
}
