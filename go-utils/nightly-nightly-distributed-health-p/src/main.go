package main

import (
	"bufio"
	"flag"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

type ProbeResult struct {
	URL        string
	Status     string
	Duration   time.Duration
	StatusCode int
	Error      error
}

// probeURL performs an HTTP GET request to the given URL and measures the response time.
func probeURL(url string, timeout time.Duration) ProbeResult {
	client := http.Client{
		Timeout: timeout,
	}

	start := time.Now()
	resp, err := client.Get(url)
	latency := time.Since(start)

	if err != nil {
		return ProbeResult{URL: url, Status: "VOID ANOMALY", Error: err}
	}
	defer resp.Body.Close()

	status := "OK"
	if resp.StatusCode >= 400 {
		status = "VOID ANOMALY"
	}

	return ProbeResult{URL: url, Status: status, Duration: latency, StatusCode: resp.StatusCode}
}

// loadURLsFromFile reads URLs from a file, one per line.
func loadURLsFromFile(filePath string) ([]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open URL file: %w", err)
	}
	defer file.Close()

	var urls []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" && !strings.HasPrefix(line, "#") {
			urls = append(urls, line)
		}
	}

	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("error reading URL file: %w", err)
	}

	return urls, nil
}

func main() {
	var urlsFlag string
	var fileFlag string
	var concurrencyFlag int
	var timeoutFlag time.Duration

	flag.StringVar(&urlsFlag, "urls", "", "Comma-separated list of URLs to probe.")
	flag.StringVar(&fileFlag, "file", "", "Path to a file containing URLs, one per line.")
	flag.IntVar(&concurrencyFlag, "concurrency", 5, "Maximum number of concurrent probes.")
	flag.DurationVar(&timeoutFlag, "timeout", 5*time.Second, "Timeout for each HTTP request.")
	flag.Parse()

	var targetURLs []string
	if urlsFlag != "" {
		targetURLs = append(targetURLs, strings.Split(urlsFlag, ",")...)
	}

	if fileFlag != "" {
		fileURLs, err := loadURLsFromFile(fileFlag)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error loading URLs from file: %v\n", err)
			os.Exit(1)
		}
		targetURLs = append(targetURLs, fileURLs...)
	}

	if len(targetURLs) == 0 {
		fmt.Println("No URLs provided. Use -urls or -file flag.")
		flag.Usage()
		os.Exit(1)
	}

	// Use a buffered channel to send URLs to workers
	urlChan := make(chan string, len(targetURLs))
	// Use a buffered channel to receive results from workers
	resultChan := make(chan ProbeResult, len(targetURLs))

	var wg sync.WaitGroup

	// Start worker goroutines
	for i := 0; i < concurrencyFlag; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for url := range urlChan {
				resultChan <- probeURL(url, timeoutFlag)
			}
		}()
	}

	// Send URLs to the urlChan
	for _, url := range targetURLs {
		urlChan <- url
	}
	close(urlChan) // Close the channel to signal workers no more URLs are coming

	// Wait for all workers to finish
	wg.Wait()
	close(resultChan) // Close the result channel after all results are sent

	// Collect and print results
	for result := range resultChan {
		fmt.Printf("Probing %s...\n", result.URL)
		if result.Error != nil {
			fmt.Printf("  Status: %s\n", result.Status)
			fmt.Printf("  Temporal Echo: N/A\n")
			fmt.Printf("  Aura Code: N/A (Error: %v)\n\n", result.Error)
		} else {
			fmt.Printf("  Status: %s\n", result.Status)
			fmt.Printf("  Temporal Echo: %s\n", result.Duration)
			fmt.Printf("  Aura Code: %d\n\n", result.StatusCode)
		}
	}
}
