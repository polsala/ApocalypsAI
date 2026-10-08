package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

const (
	defaultTimeout = 5 * time.Second
	bodySnippetLen = 80 // Length of body snippet to display
)

// DroneResult holds the outcome of a single drone's mission
type DroneResult struct {
	URL        string
	StatusCode int
	Status     string
	Latency    time.Duration
	BodySnippet string
	Error      error
}

// fetchURL simulates a scavenger drone fetching resources from a URL
func fetchURL(client *http.Client, url string, results chan<- DroneResult, wg *sync.WaitGroup) {
	defer wg.Done()

	start := time.Now()
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		results <- DroneResult{URL: url, Error: fmt.Errorf("failed to create request: %w", err)}
		return
	}

	resp, err := client.Do(req)
	if err != nil {
		results <- DroneResult{URL: url, Error: fmt.Errorf("failed to fetch URL: %w", err)}
		return
	}
	defer resp.Body.Close()

	latency := time.Since(start)

	bodyBytes, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		results <- DroneResult{URL: url, StatusCode: resp.StatusCode, Status: resp.Status, Latency: latency, Error: fmt.Errorf("failed to read response body: %w", err)}
		return
	}

	bodySnippet := string(bodyBytes)
	if len(bodySnippet) > bodySnippetLen {
		bodySnippet = bodySnippet[:bodySnippetLen] + "..."
	}
	bodySnippet = strings.ReplaceAll(bodySnippet, "\n", "\\n") // Escape newlines for single-line output

	results <- DroneResult{
		URL:        url,
		StatusCode: resp.StatusCode,
		Status:     resp.Status,
		Latency:    latency,
		BodySnippet: bodySnippet,
		Error:      nil,
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: scavenger-dispatcher <url1> <url2> ...")
		os.Exit(1)
	}

	urls := os.Args[1:]
	results := make(chan DroneResult, len(urls))
	var wg sync.WaitGroup

	client := &http.Client{
		Timeout: defaultTimeout,
	}

	fmt.Printf("Dispatching %d scavenger drones...\n", len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(client, url, results, &wg)
	}

	wg.Wait() // Wait for all drones to return
	close(results)

	droneCount := 1
	for result := range results {
		if result.Error != nil {
			fmt.Printf("[DRONE %d] %s - Error: %v\n", droneCount, result.URL, result.Error)
		} else {
			fmt.Printf("[DRONE %d] %s - Status: %d %s, Latency: %s, Body Snippet: \"%s\"\n",
				droneCount, result.URL, result.StatusCode, result.Status, result.Latency.Round(time.Millisecond), result.BodySnippet)
		}
		droneCount++
	}
	fmt.Println("All scavenger drones have returned.")
}
