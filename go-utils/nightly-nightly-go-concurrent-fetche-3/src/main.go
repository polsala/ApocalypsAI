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
	URL    string
	Status string
	Error  error
}

func fetchURL(url string, client *http.Client, results chan<- FetchResult, wg *sync.WaitGroup) {
	defer wg.Done()

	resp, err := client.Get(url)
	if err != nil {
		results <- FetchResult{URL: url, Error: err}
		return
	}
	defer resp.Body.Close()

	results <- FetchResult{URL: url, Status: fmt.Sprintf("%d %s", resp.StatusCode, http.StatusText(resp.StatusCode))}
}

func main() {
	var timeoutSeconds int
	flag.IntVar(&timeoutSeconds, "timeout", 10, "Request timeout in seconds")
	flag.Parse()

	urls := flag.Args()

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher [-timeout <seconds>] <url1> <url2> ...")
		os.Exit(1)
	}

	client := &http.Client{
		Timeout: time.Duration(timeoutSeconds) * time.Second,
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, client, results, &wg)
	}

	wg.Wait()
	close(results)

	fmt.Println("--- Fetch Results ---")
	for result := range results {
		if result.Error != nil {
			fmt.Printf("URL: %s\n  Error: %v\n", result.URL, result.Error)
		} else {
			fmt.Printf("URL: %s\n  Status: %s\n", result.URL, result.Status)
		}
	}
}
