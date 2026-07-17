package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

type FetchResult struct {
	URL           string
	StatusCode    int
	ResponseTime  time.Duration
	Error         error
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	startTime := time.Now()

	resp, err := http.Get(url)
	if err != nil {
		results <- FetchResult{
			URL:          url,
			StatusCode:   0,
			ResponseTime: time.Since(startTime),
			Error:        err,
		}
		return
	}
	defer resp.Body.Close()

	// Read the body to ensure the connection is fully utilized and timed.
	// We don't need to process the body content for this utility.
	_, err = io.Copy(io.Discard, resp.Body)
	if err != nil {
		// If reading the body fails, we still report the status code and time.
		// This might be an edge case, but we prioritize reporting what we have.
		results <- FetchResult{
			URL:          url,
			StatusCode:   resp.StatusCode,
			ResponseTime: time.Since(startTime),
			Error:        fmt.Errorf("failed to read response body: %w", err),
		}
		return
	}

	results <- FetchResult{
		URL:          url,
		StatusCode:   resp.StatusCode,
		ResponseTime: time.Since(startTime),
		Error:        nil,
	}
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	for result := range results {
		if result.Error != nil {
			fmt.Printf("URL: %s\n  Error: %v\n\n", result.URL, result.Error)
		} else {
			fmt.Printf("URL: %s\n  Status: %d %s\n  Response Time: %s\n\n", result.URL, result.StatusCode, http.StatusText(result.StatusCode), result.ResponseTime.Round(time.Millisecond))
		}
	}
}
