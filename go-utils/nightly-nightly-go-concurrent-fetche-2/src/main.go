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
	URL    string
	Status string
	Error  error
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	client := http.Client{
		Timeout: 10 * time.Second,
	}

	resp, err := client.Get(url)
	if err != nil {
		results <- FetchResult{URL: url, Error: err}
		return
	}
	defer resp.Body.Close()

	// Read the body to ensure the request is fully processed
	_, readErr := io.ReadAll(resp.Body)
	if readErr != nil {
		results <- FetchResult{URL: url, Error: fmt.Errorf("failed to read body: %w", readErr)}
		return
	}

	results <- FetchResult{URL: url, Status: resp.Status}
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent_fetcher <url1> <url2> ...")
		return
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	fmt.Println("Starting concurrent fetches...")
	for _, url := range urls {
		fmt.Printf("Processing URL: %s\n", url)
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	svar successes []string
	var failures []string

	for res := range results {
		if res.Error != nil {
			failures = append(failures, fmt.Sprintf("- %s (Error: %v)", res.URL, res.Error))
		} else {
			successes = append(successes, fmt.Sprintf("- %s (Status: %s)", res.URL, res.Status))
		}
	}

	fmt.Println("\nResults:")

	if len(successes) > 0 {
		fmt.Println("\nSuccesses:")
		for _, s := range successes {
			fmt.Println(s)
		}
	}

	if len(failures) > 0 {
		fmt.Println("\nFailures:")
		for _, f := range failures {
			fmt.Println(f)
		}
	}

	if len(successes) == 0 && len(failures) == 0 {
		fmt.Println("No URLs were processed.")
	}
}
