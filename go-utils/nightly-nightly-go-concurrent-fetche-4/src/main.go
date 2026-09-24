package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

// FetchResult holds the outcome of fetching a single URL.
type FetchResult struct {
	URL    string
	Status string
	Error  error
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		return
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	// Set a reasonable timeout for each request.
	client := http.Client{
		Timeout: 10 * time.Second,
	}

	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			fmt.Printf("Fetching %s...\n", u)

			resp, err := client.Get(u)
			if err != nil {
				results <- FetchResult{URL: u, Error: err}
				return
			}
			defer resp.Body.Close()

			results <- FetchResult{URL: u, Status: resp.Status}
		}(url)
	}

	wg.Wait()
	close(results)

	// Process and print results
	for res := range results {
		if res.Error != nil {
			fmt.Printf("  -> Error: %v\n", res.Error)
		} else {
			fmt.Printf("  -> Success: %s\n", res.Status)
		}
	}
}
