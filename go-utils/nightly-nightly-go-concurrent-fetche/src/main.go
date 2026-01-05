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
	URL          string
	StatusCode   int
	ResponseTime time.Duration
	Error        error
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	startTime := time.Now()
	resp, err := http.Get(url)

	result := FetchResult{
		URL:          url,
		ResponseTime: time.Since(startTime),
	}

	if err != nil {
		result.Error = err
	} else {
		result.StatusCode = resp.StatusCode
		defer resp.Body.Close()
		// Read the body to ensure the connection is fully processed
		_, readErr := io.Copy(io.Discard, resp.Body)
		if readErr != nil {
			result.Error = fmt.Errorf("error reading response body: %w", readErr)
		}
	}

	results <- result
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		return
	}

	fmt.Println("Fetching URLs concurrently...")

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("\nResults:")
	for result := range results {
		fmt.Println("--------------------------------------------------")
		fmt.Printf("URL: %s\n", result.URL)
		fmt.Printf("Status: %d %s\n", result.StatusCode, http.StatusText(result.StatusCode))
		fmt.Printf("Response Time: %s\n", result.ResponseTime)
		if result.Error != nil {
			fmt.Printf("Error: %v\n", result.Error)
		}
	}
	fmt.Println("--------------------------------------------------")
}
