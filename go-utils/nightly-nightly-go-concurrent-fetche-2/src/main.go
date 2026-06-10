package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

// URLStatus represents the status of a fetched URL.
type URLStatus struct {
	URL        string
	StatusCode int
	Error      error
	Duration   time.Duration
}

func main() {
	urls := os.Args[1:]

	if len(urls) == 0 {
		log.Fatal("No URLs provided. Please provide a list of URLs as command-line arguments.")
	}

	log.Printf("Starting concurrent fetch for %d URLs...\n", len(urls))

	var wg sync.WaitGroup
	results := make(chan URLStatus, len(urls))

	for _, url := range urls {
		wg.Add(1)
		go fetchURL(url, &wg, results)
	}

	wg.Wait()
	close(results)

	log.Println("All fetches completed. Reporting results:")
	for result := range results {
		if result.Error != nil {
			log.Printf("[ERROR] %s - Error: %v\n", result.URL, result.Error)
		} else {
			log.Printf("[SUCCESS] %s - Status: %d %s - Time: %v\n", result.URL, result.StatusCode, http.StatusText(result.StatusCode), result.Duration)
		}
	}
}

func fetchURL(url string, wg *sync.WaitGroup, results chan<- URLStatus) {
	defer wg.Done()

	log.Printf("[INFO] Fetching: %s\n", url)

	startTime := time.Now()

	client := http.Client{
		Timeout: 10 * time.Second, // Set a reasonable timeout
	}

	res, err := client.Get(url)
	statusCode := 0
	if res != nil {
		statusCode = res.StatusCode
		defer res.Body.Close()
	}

	duration := time.Since(startTime)

	results <- URLStatus{
		URL:        url,
		StatusCode: statusCode,
		Error:      err,
		Duration:   duration,
	}
}
