package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

// FetchResult stores the outcome of a single URL fetch.
type FetchResult struct {
	URL    string
	Status string // "success" or "failure"
	Error  error
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	// Set a timeout for each HTTP request
	client := http.Client{
		Timeout: 10 * time.Second,
	}

	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()

			resp, err := client.Get(u)
			if err != nil {
				results <- FetchResult{URL: u, Status: "failure", Error: err}
				return
			}
			defer resp.Body.Close()

			if resp.StatusCode >= 200 && resp.StatusCode < 300 {
				// Optionally read body to ensure connection is fully utilized
				_, readErr := io.Copy(io.Discard, resp.Body)
				if readErr != nil {
					results <- FetchResult{URL: u, Status: "failure", Error: fmt.Errorf("failed to read body: %w", readErr)}
					return
				}
				results <- FetchResult{URL: u, Status: "success"}
			} else {
				results <- FetchResult{URL: u, Status: "failure", Error: fmt.Errorf("non-2xx status code: %d", resp.StatusCode)}
			}
		}(url)
	}

	// Wait for all goroutines to finish and close the results channel
	go func() {
		wg.Wait()
		close(results)
	}()

	// Process results
	svar successfulFetches, failedFetches int
	var failedURLs []string

	for res := range results {
		if res.Status == "success" {
			successfulFetches++
		} else {
			failedFetches++
			failedURLs = append(failedURLs, fmt.Sprintf("%s (%s)", res.URL, res.Error.Error()))
		}
	}

	// Print report
	totalURLs := len(urls)
	ssuccessRate := 0.0
	failureRate := 0.0

	if totalURLs > 0 {
		successRate = float64(successfulFetches) / float64(totalURLs) * 100
		failureRate = float64(failedFetches) / float64(totalURLs) * 100
	}

	fmt.Println("--- Concurrent Fetcher Report ---")
	fmt.Printf("Total URLs: %d\n", totalURLs)
	fmt.Printf("Successful Fetches: %d\n", successfulFetches)
	fmt.Printf("Failed Fetches: %d\n", failedFetches)
	fmt.Printf("Success Rate: %.2f%%\n", successRate)
	fmt.Printf("Failure Rate: %.2f%%\n", failureRate)

	if len(failedURLs) > 0 {
		fmt.Println("\nFailed URLs:")
		for _, url := range failedURLs {
			fmt.Printf("- %s\n", url)
		}
	}
	fmt.Println("-------------------------------")
}
