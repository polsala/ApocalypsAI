package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

type FetchResult struct {
	URL   string
	Error error
}

func main() {
	urls := os.Args[1:]

	// Use default URLs if none are provided
	if len(urls) == 0 {
		urls = []string{
			"https://www.google.com",
			"https://www.github.com",
			"http://httpbin.org/delay/2", // Simulates a slow response
			"https://invalid.domain.for.testing", // Simulates a DNS error
		}
		fmt.Println("No URLs provided, using default test URLs.")
	}

	fmt.Printf("Processing %d URLs...\n\n", len(urls))

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	// Set a timeout for each HTTP request
	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
		
			resp, err := client.Get(u)
			if err != nil {
				results <- FetchResult{URL: u, Error: err}
				return
			}
			defer resp.Body.Close()

			// Read the body to ensure the request is fully processed
			_, err = io.ReadAll(resp.Body)
			if err != nil {
				results <- FetchResult{URL: u, Error: fmt.Errorf("failed to read body: %w", err)}
				return
			}

			if resp.StatusCode < 200 || resp.StatusCode >= 300 {
				results <- FetchResult{URL: u, Error: fmt.Errorf("received non-success status code: %d", resp.StatusCode)}
				return
			}

			results <- FetchResult{URL: u, Error: nil}
		}(url)
	}

	wg.Wait()
	close(results)

	var successfulCount int
	var failedFetches []FetchResult

	for res := range results {
		if res.Error != nil {
			failedFetches = append(failedFetches, res)
		} else {
			successfulCount++
		}
	}

	fmt.Println("--- Fetch Summary ---")
	fmt.Printf("Total URLs: %d\n", len(urls))
	fmt.Printf("Successful: %d\n", successfulCount)
	fmt.Printf("Failed: %d\n", len(failedFetches))

	if len(failedFetches) > 0 {
		fmt.Println("\n--- Failed URLs ---")
		for _, fail := range failedFetches {
			fmt.Printf("- %s: %v\n", fail.URL, fail.Error)
		}
	}
}
