package main

import (
	"bufio"
	"fmt"
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

func fetchURL(url string, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	start := time.Now()
	resp, err := http.Get(url)

	duration := time.Since(start)

	result := FetchResult{
		URL:      url,
		Duration: duration,
		Error:    err,
	}

	if err == nil {
		result.StatusCode = resp.StatusCode
		resp.Body.Close() // Close the body to prevent resource leaks
	}

	results <- result
}

func main() {
	var urls []string

	// Check if URLs are provided as command-line arguments
	if len(os.Args) > 1 {
		urls = os.Args[1:]
	} else {
		// If not, read URLs from standard input
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			urls = append(urls, scanner.Text())
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error reading from stdin: %v\n", err)
			os.Exit(1)
		}
	}

	if len(urls) == 0 {
		fmt.Println("No URLs provided. Please provide URLs as arguments or via stdin.")
		os.Exit(0)
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("--- Fetch Results ---")
	for result := range results {
		if result.Error != nil {
			fmt.Printf("URL: %s, Error: %v\n", result.URL, result.Error)
		} else {
			fmt.Printf("URL: %s, Status: %d, Duration: %s\n", result.URL, result.StatusCode, result.Duration)
		}
	}
}
