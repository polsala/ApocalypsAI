package main

import (
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"
)

type FetchResult struct {
	URL      string
	Status   string
	Duration time.Duration
	Error    error
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	startTime := time.Now()
	resp, err := http.Get(url)

	duration := time.Since(startTime)

	result := FetchResult{
		URL:      url,
		Duration: duration,
	}

	if err != nil {
		result.Status = fmt.Sprintf("Failed (%v)", err)
		result.Error = err
	} else {
		defer resp.Body.Close()
		body, readErr := io.ReadAll(resp.Body)
		if readErr != nil {
			result.Status = fmt.Sprintf("Failed reading body (%v)", readErr)
			result.Error = readErr
		} else {
			result.Status = fmt.Sprintf("%d %s", resp.StatusCode, http.StatusText(resp.StatusCode))
			_ = body // Consume body to ensure connection is closed properly
		}
	}

	results <- result
}

func main() {
	urls := []string{
		"https://www.google.com",
		"https://httpbin.org/delay/2",
		"https://www.github.com",
		"https://nonexistent.domain.xyz", // Example of a failing URL
		"https://httpbin.org/status/404",
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	fmt.Println("Fetching URLs concurrently...")

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	svar successfulCount int
	var failedCount int

	for result := range results {
		fmt.Printf("\nURL: %s\n", result.URL)
		fmt.Printf("  Status: %s\n", result.Status)
		fmt.Printf("  Duration: %v\n", result.Duration)

		if result.Error == nil {
			successfulCount++
		} else {
			failedCount++
		}
	}

	fmt.Println("\nSummary:")
	fmt.Printf("  Total URLs: %d\n", len(urls))
	fmt.Printf("  Successful: %d\n", successfulCount)
	fmt.Printf("  Failed: %d\n", failedCount)
}
