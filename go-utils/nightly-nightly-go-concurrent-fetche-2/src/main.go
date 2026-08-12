package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

const defaultTimeout = 10 * time.Second

type FetchResult struct {
	URL        string
	StatusCode int
	Duration   time.Duration
	Error      error
}

func fetchURL(url string, client *http.Client, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	startTime := time.Now()
	resp, err := client.Get(url)

	duration := time.Since(startTime)

	result := FetchResult{
		URL:      url,
		Duration: duration,
		Error:    err,
	}

	if err != nil {
		results <- result
		return
	}

	defer resp.Body.Close()
	result.StatusCode = resp.StatusCode
	results <- result
}

func main() {
	var urls []string

	if len(os.Args) > 1 {
		urls = os.Args[1:]
	} else {
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

	client := &http.Client{
		Timeout: defaultTimeout,
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	for _, url := range urls {
		// Ensure URLs have a scheme, default to http if missing
		processedURL := url
		if !strings.HasPrefix(processedURL, "http://") && !strings.HasPrefix(processedURL, "https://") {
			processedURL = "http://" + processedURL
		}
		wg.Add(1)
		go fetchURL(processedURL, client, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("--- Fetch Results ---")
for result := range results {
	if result.Error != nil {
		fmt.Printf("%s: Error - %v\n", result.URL, result.Error)
	} else {
		fmt.Printf("%s: Status %d, Time %s\n", result.URL, result.StatusCode, result.Duration.Round(time.Millisecond))
	}
}
	fmt.Println("---------------------")
}
