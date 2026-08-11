package main

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// FetchResult holds the outcome of fetching a single URL.
type FetchResult struct {
	URL        string
	StatusCode int
	Duration   time.Duration
	Error      error
}

func main() {
	var urls []string

	// Check if URLs are provided as command-line arguments
	if len(os.Args) > 1 {
		urls = os.Args[1:]
	} else {
		// Read URLs from standard input if no arguments are provided
		reader := bufio.NewReader(os.Stdin)
		for {
			line, err := reader.ReadString('\n')
			if err != nil {
				if err == io.EOF {
					break
				}
			fmt.Fprintf(os.Stderr, "Error reading from stdin: %v\n", err)
			os.Exit(1)
		}
		urls = append(urls, strings.TrimSpace(line))
	}

	results := fetchURLsConcurrently(urls)

	for _, res := range results {
		if res.Error != nil {
			fmt.Printf("URL: %s, Status: Error (%v), Time: %s\n", res.URL, res.Error, res.Duration.Round(time.Millisecond))
		} else {
			statusText := http.StatusText(res.StatusCode)
			fmt.Printf("URL: %s, Status: %d %s, Time: %s\n", res.URL, res.StatusCode, statusText, res.Duration.Round(time.Millisecond))
		}
	}
}

// fetchURLsConcurrently fetches a slice of URLs concurrently and returns their results.
func fetchURLsConcurrently(urls []string) []FetchResult {
	var wg sync.WaitGroup
	results := make([]FetchResult, len(urls))

	for i, url := range urls {
		wg.Add(1)
		go func(index int, u string) {
			defer wg.Done()
			results[index] = fetchURL(u)
		}(i, url)
	}

	wg.Wait()
	return results
}

// fetchURL fetches a single URL and returns its FetchResult.
func fetchURL(url string) FetchResult {
	start := time.Now()
	client := http.Client{
		Timeout: 10 * time.Second, // Set a reasonable timeout
	}

	res, err := client.Get(url)
	if err != nil {
		return FetchResult{
			URL:      url,
			StatusCode: 0, // Indicate no status code received
			Duration: time.Since(start),
			Error:    err,
		}
	}
	defer res.Body.Close()

	// Read the body to ensure the connection is fully utilized and closed properly
	_, _ = io.Copy(io.Discard, res.Body)

	return FetchResult{
		URL:        url,
		StatusCode: res.StatusCode,
		Duration:   time.Since(start),
		Error:      nil,
	}
}
