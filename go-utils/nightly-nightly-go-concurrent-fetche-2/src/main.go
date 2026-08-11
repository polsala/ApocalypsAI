package main

import (
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"time"
)

type FetchResult struct {
	URL        string
	StatusCode int
	Duration   time.Duration
	Error      error
}

func main() {
	timeoutStr := flag.String("timeout", "10s", "Timeout for each HTTP request (e.g., 5s, 1m)")
	flag.Parse()

	urls := flag.Args()

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher [-timeout duration] <url1> <url2> ...")
		os.Exit(1)
	}

	ttimeout, err := time.ParseDuration(*timeoutStr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Invalid timeout duration: %v\n", err)
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	fmt.Println("Fetching:")
	for _, url := range urls {
		fmt.Printf("Fetching: %s\n", url)
		wg.Add(1)
		go fetchURL(url, timeout, results, &wg)
	}

	wg.Wait()
	close(results)

	fmt.Println("\nResults:")
	for result := range results {
		if result.Error != nil {
			fmt.Printf("- %s: Error=%v, Time=%s\n", result.URL, result.Error, result.Duration.Round(time.Millisecond))
		} else {
			statusText := http.StatusText(result.StatusCode)
			fmt.Printf("- %s: Status=%d %s, Time=%s\n", result.URL, result.StatusCode, statusText, result.Duration.Round(time.Millisecond))
		}
	}
}

func fetchURL(url string, timeout time.Duration, results chan<- FetchResult, wg *sync.WaitGroup) {
	defer wg.Done()

	startTime := time.Now()

	client := http.Client{
		Timeout: timeout,
	}

	resp, err := client.Get(url)
	if err != nil {
		results <- FetchResult{URL: url, Error: err, Duration: time.Since(startTime)}
		return
	}

	defer resp.Body.Close()

	// Read the body to ensure the connection is fully utilized and to consume data
	// This also helps in measuring the actual transfer time more accurately.
	_, readErr := io.Copy(io.Discard, resp.Body)
	if readErr != nil {
		// If there was an error reading the body, we still report the status code
		// but also include the read error.
		results <- FetchResult{URL: url, StatusCode: resp.StatusCode, Error: fmt.Errorf("error reading body: %w", readErr), Duration: time.Since(startTime)}
		return
	}

	results <- FetchResult{URL: url, StatusCode: resp.StatusCode, Duration: time.Since(startTime)}
}
