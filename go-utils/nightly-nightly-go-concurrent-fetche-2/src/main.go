package main

import (
	"fmt"
	"net/http"
	"os"
	"sync"
	"time"
)

type FetchResult struct {
	URL      string
	Status   string
	Duration time.Duration
	Error    error
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- FetchResult) {
	defer wg.Done()

	startTime := time.Now()
	client := http.Client{
		Timeout: 10 * time.Second, // Set a reasonable timeout
	}

	res := FetchResult{URL: url}
	resp, err := client.Get(url)
	if err != nil {
		res.Status = "Error"
		res.Error = err
	} else {
		res.Status = "OK"
		defer resp.Body.Close()
	}

	res.Duration = time.Since(startTime)
	results <- res
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		fmt.Println("Usage: concurrent-fetcher <url1> <url2> ...")
		return
	}

	var wg sync.WaitGroup
	results := make(chan FetchResult, len(urls))

	fmt.Println("Starting concurrent fetches...")

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	fmt.Println("\n--- Fetch Results ---")
	for res := range results {
		if res.Error != nil {
			fmt.Printf("[%s] %s (%.2fs) - Error: %v\n", res.Status, res.URL, res.Duration.Seconds(), res.Error)
		} else {
			fmt.Printf("[%s] %s (%.2fs)\n", res.Status, res.URL, res.Duration.Seconds())
		}
	}
	fmt.Println("---------------------")
}
