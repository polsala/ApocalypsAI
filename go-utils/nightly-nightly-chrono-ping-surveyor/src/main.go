package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// PingResult holds the outcome of a single ping operation.
type PingResult struct {
	URL      string
	Duration time.Duration
	Error    error
	IsDistorted bool
}

// pingURL performs an HTTP GET request to the given URL and measures the response time.
func pingURL(client *http.Client, url string, timeout time.Duration, threshold time.Duration, results chan<- PingResult, wg *sync.WaitGroup) {
	defer wg.Done()

	start := time.Now()
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		results <- PingResult{URL: url, Error: fmt.Errorf("failed to create request: %w", err)}
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		results <- PingResult{URL: url, Error: fmt.Errorf("failed to connect: %w", err)}
		return
	}
	defer resp.Body.Close()

	// Read the body to ensure full response is received and measured
	_, err = io.Copy(io.Discard, resp.Body)
	if err != nil {
		results <- PingResult{URL: url, Error: fmt.Errorf("failed to read response body: %w", err)}
		return
	}

	duration := time.Since(start)
	isDistorted := duration > threshold

	results <- PingResult{
		URL:      url,
		Duration: duration,
		Error:    nil,
		IsDistorted: isDistorted,
	}
}

// parseDuration parses a duration string with a default value.
func parseDuration(s string, defaultVal time.Duration) (time.Duration, error) {
	if s == "" {
		return defaultVal, nil
	}
	d, err := time.ParseDuration(s)
	if err != nil {
		return 0, fmt.Errorf("invalid duration format: %s", s)
	}
	return d, nil
}

func main() {
	// Default values
	defaultTimeout := 5 * time.Second
	defaultThreshold := 100 * time.Millisecond

	// Parse command-line arguments
	args := os.Args[1:]
	urls := []string{}
	var timeoutStr, thresholdStr string

	for i := 0; i < len(args); i++ {
		arg := args[i]
		switch arg {
		case "-timeout":
			if i+1 < len(args) {
				timeoutStr = args[i+1]
				i++
			} else {
				log.Fatalf("Error: -timeout requires a duration value.")
			}
		case "-threshold":
			if i+1 < len(args) {
				thresholdStr = args[i+1]
				i++
			} else {
				log.Fatalf("Error: -threshold requires a duration value.")
			}
		default:
			urls = append(urls, arg)
		}
	}

	if len(urls) == 0 {
		fmt.Println("Usage: chrono-ping-surveyor [-timeout <duration>] [-threshold <duration>] <url1> [url2...]")
		fmt.Println("Example: chrono-ping-surveyor -timeout 5s -threshold 200ms https://example.com http://localhost:8080")
		os.Exit(1)
	}

	timeout, err := parseDuration(timeoutStr, defaultTimeout)
	if err != nil {
		log.Fatalf("Error parsing timeout: %v", err)
	}
	threshold, err := parseDuration(thresholdStr, defaultThreshold)
	if err != nil {
		log.Fatalf("Error parsing threshold: %v", err)
	}

	client := &http.Client{
		Timeout: timeout,
	}

	results := make(chan PingResult, len(urls))
	var wg sync.WaitGroup
	distortionsFound := 0

	fmt.Printf("[%s] Chrono-Ping Survey Report:\n", time.Now().Format("2006-01-02 15:04:05"))
	fmt.Println(strings.Repeat("-", 50))

	for _, url := range urls {
		wg.Add(1)
		go pingURL(client, url, timeout, threshold, results, &wg)
	}

	wg.Wait() // Wait for all pings to complete
	close(results) // Close the channel after all goroutines are done

	// Collect and print results
	for res := range results {
		if res.Error != nil {
			fmt.Printf("[ERROR] %s - %v\n", res.URL, res.Error)
		} else if res.IsDistorted {
			fmt.Printf("[DISTORTION!] %s - %s (Threshold: %s)\n", res.URL, res.Duration, threshold)
			distortionsFound++
		} else {
			fmt.Printf("[OK] %s - %s\n", res.URL, res.Duration)
		}
	}

	fmt.Println(strings.Repeat("-", 50))
	if distortionsFound > 0 {
		fmt.Printf("Survey Complete. Detected %d Temporal Distortion(s).\n", distortionsFound)
	} else {
		fmt.Println("Survey Complete. No Temporal Distortions detected.")
	}
}
