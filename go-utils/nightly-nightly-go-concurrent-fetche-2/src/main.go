package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

func main() {
	urls := os.Args[1:]
	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		os.Exit(1)
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			fetchURL(u, results)
		}(url)
	}

	wg.Wait()
	close(results)

	for res := range results {
		printResult(res)
	}
}

type FetchResult struct {
	URL    string
	Status string
	Time   time.Duration
	Error  error
}

func fetchURL(url string, results chan<- FetchResult) {
	fmt.Printf("Fetching: %s\n", url)
	startTime := time.Now()

	resp, err := http.Get(url)
	if err != nil {
		results <- FetchResult{
			URL:   url,
			Status: "Error",
			Error:  err,
		}
		return
	}
	defer resp.Body.Close()

	duration := time.Since(startTime)

	results <- FetchResult{
		URL:    url,
		Status: "OK",
		Time:   duration,
	}
}

func printResult(res FetchResult) {
	if res.Status == "OK" {
		fmt.Printf("  Status: %s\n", res.Status)
		fmt.Printf("  Time: %s\n", res.Time.Round(time.Millisecond))
	} else {
		fmt.Printf("  Status: %s\n", res.Status)
		fmt.Printf("  Error: %v\n", res.Error)
	}
}
