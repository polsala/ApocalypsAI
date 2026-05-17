package main

import (
	"context"
	"flag"
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
	Err    error
	Duration time.Duration
}

func fetchURL(ctx context.Context, url string, results chan<- FetchResult, timeout time.Duration) {
	start := time.Now()
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		results <- FetchResult{URL: url, Status: "Error", Err: err, Duration: time.Since(start)}
		return
	}

	client := &http.Client{
		Timeout: timeout,
	}

	resp, err := client.Do(req)
	if err != nil {
		results <- FetchResult{URL: url, Status: "Error", Err: err, Duration: time.Since(start)}
		return
	}

	defer resp.Body.Close()

	// Read the body to ensure the request is fully processed, but discard it.
	_, err = io.Copy(io.Discard, resp.Body)
	if err != nil {
		results <- FetchResult{URL: url, Status: "Error reading body", Err: err, Duration: time.Since(start)}
		return
	}

	if resp.StatusCode >= 200 && resp.StatusCode < 300 {
		results <- FetchResult{URL: url, Status: "Success", Duration: time.Since(start)}
	} else {
		results <- FetchResult{URL: url, Status: fmt.Sprintf("HTTP Error: %d", resp.StatusCode), Err: fmt.Errorf("status code %d", resp.StatusCode), Duration: time.Since(start)}
	}
}

func main() {
	var timeoutSeconds int
	flag.IntVar(&timeoutSeconds, "timeout", 10, "Timeout for each HTTP request in seconds")
	flag.Parse()

	urls := flag.Args()

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher [-timeout <seconds>] <url1> <url2> ...")
		os.Exit(1)
	}

	timeout := time.Duration(timeoutSeconds) * time.Second
	fmt.Printf("Fetching URLs with a timeout of %s...

", timeout)

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	ctx, cancel := context.WithTimeout(context.Background(), timeout*time.Duration(len(urls)))
	defer cancel() // Ensure cancel is called to release resources

	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			fetchURL(ctx, u, results, timeout)
		}(url)
	}

	wg.Wait()
	close(results)

	var successCount, errorCount, timeoutCount int

	fmt.Println("Results:")
	for res := range results {
		fmt.Printf("----------------------------------------\n")
		fmt.Printf("URL: %s\n", res.URL)
		if res.Err != nil {
			if res.Err.Error() == "context deadline exceeded" {
				fmt.Printf("Status: Timeout (%s)\n", res.Err)
				timeoutCount++
			} else {
				fmt.Printf("Status: Error (%s)\n", res.Err)
				errorCount++
			}
		} else {
			fmt.Printf("Status: %s\n", res.Status)
			successCount++
		}
		fmt.Printf("Time: %s\n", res.Duration.Round(time.Millisecond))
	}

	fmt.Printf("----------------------------------------\n")
	fmt.Println("\nSummary:")
	fmt.Printf("Successful: %d\n", successCount)
	fmt.Printf("Errors: %d\n", errorCount)
	fmt.Printf("Timeouts: %d\n", timeoutCount)
}
