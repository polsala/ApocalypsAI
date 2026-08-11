package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

type FetchResult struct {
	URL         string
	StatusCode  int
	ResponseTime time.Duration
	Error       string
}

func fetchURL(url string, client *http.Client, results chan<- FetchResult, wg *sync.WaitGroup) {
	defer wg.Done()

	startTime := time.Now()
	resp, err := client.Get(url)

	result := FetchResult{URL: url}

	if err != nil {
		result.Error = err.Error()
		// If there's an error, we might not have a status code, or it might be 0
		if resp != nil {
			result.StatusCode = resp.StatusCode
		}
	} else {
		result.StatusCode = resp.StatusCode
		resp.Body.Close() // Ensure the body is closed
	}

	result.ResponseTime = time.Since(startTime)
	results <- result
}

func main() {
	var timeoutSeconds int
	flag.IntVar(&timeoutSeconds, "timeout", 30, "Timeout for each HTTP request in seconds")
	flag.Parse()

	urls := flag.Args()

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher [--timeout <seconds>] <url1> <url2> ...")
		os.Exit(1)
	}

	client := &http.Client{
		Timeout: time.Duration(timeoutSeconds) * time.Second,
	}

	results := make(chan FetchResult, len(urls))
	var wg sync.WaitGroup

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, client, results, &wg)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	fmt.Printf("Fetching %d URLs with a timeout of %d seconds:\n\n", len(urls), timeoutSeconds)

	for result := range results {
		status := fmt.Sprintf("%d", result.StatusCode)
		if result.StatusCode == 0 {
			status = "N/A"
		}
		fmt.Printf("URL: %s\n", result.URL)
		fmt.Printf("  Status Code: %s\n", status)
		fmt.Printf("  Response Time: %s\n", result.ResponseTime.Round(time.Millisecond))
		if result.Error != "" {
			fmt.Printf("  Error: %s\n", result.Error)
		}
		fmt.Println("--------------------")
	}
}
