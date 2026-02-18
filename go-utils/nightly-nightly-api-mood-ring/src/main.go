package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
)

// Mood represents the emotional state of an API.
type Mood struct {
	URL         string
	StatusCode  int
	Latency     time.Duration
	Description string
	Error       error
}

// determineMood assigns a whimsical mood based on status code, latency, and error.
func determineMood(statusCode int, latency time.Duration, err error) string {
	if err != nil {
		if strings.Contains(err.Error(), "timeout") {
			return "Silent (Timeout)"
		} else if strings.Contains(err.Error(), "connection refused") || strings.Contains(err.Error(), "no such host") {
			return "Silent (Connection Error)"
		}
		return fmt.Sprintf("Silent (Error: %v)", err.Error())
	}

	switch {
	case statusCode >= 200 && statusCode < 300:
		switch {
		case latency < 100*time.Millisecond:
			return "Serene"
		case latency < 500*time.Millisecond:
			return "Content"
		default:
			return "Sluggish"
		}
	case statusCode >= 400 && statusCode < 500:
		return "Confused"
	case statusCode >= 500 && statusCode < 600:
		return "Furious"
	default:
		return "Mysterious"
	}
}

// checkAPI performs an HTTP GET request and determines the API's mood.
func checkAPI(url string, client *http.Client, results chan<- Mood, wg *sync.WaitGroup) {
	defer wg.Done()

	start := time.Now()
	resp, err := client.Get(url)
	latency := time.Since(start)

	var statusCode int
	if resp != nil {
		statusCode = resp.StatusCode
		// Ensure the response body is read and closed to prevent resource leaks
		io.Copy(io.Discard, resp.Body)
		resp.Body.Close()
	}

	description := determineMood(statusCode, latency, err)

	results <- Mood{
		URL:         url,
		StatusCode:  statusCode,
		Latency:     latency,
		Description: description,
		Error:       err,
	}
}

func main() {
	var urlsFilePath string
	var timeoutStr string

	flag.StringVar(&urlsFilePath, "urls", "", "Path to a file containing URLs (one per line). If empty, reads from stdin.")
	flag.StringVar(&timeoutStr, "timeout", "3s", "HTTP request timeout (e.g., 5s, 500ms).")
	flag.Parse()

	timeout, err := time.ParseDuration(timeoutStr)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing timeout duration: %v\n", err)
		os.Exit(1)
	}

	client := &http.Client{
		Timeout: timeout,
	}

	var urls []string

	if urlsFilePath != "" {
		file, err := os.Open(urlsFilePath)
		if err != nil {
			fmt.Fprintf(os.Stderr, "Error opening URL file: %v\n", err)
			os.Exit(1)
		}
		defer file.Close()

		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			url := strings.TrimSpace(scanner.Text())
			if url != "" {
				urls = append(urls, url)
			}
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error reading URL file: %v\n", err)
			os.Exit(1)
		}
	} else {
		// Read from stdin if no file is specified
		scanner := bufio.NewScanner(os.Stdin)
		for scanner.Scan() {
			url := strings.TrimSpace(scanner.Text())
			if url != "" {
				urls = append(urls, url)
			}
		}
		if err := scanner.Err(); err != nil {
			fmt.Fprintf(os.Stderr, "Error reading from stdin: %v\n", err)
			os.Exit(1)
		}
	}

	if len(urls) == 0 {
		fmt.Println("No URLs provided. Use -urls flag or pipe URLs to stdin.")
		os.Exit(0)
	}

	fmt.Println("Checking API Moods...\n")

	results := make(chan Mood, len(urls))
	var wg sync.WaitGroup

	for _, url := range urls {
		wg.Add(1)
		go checkAPI(url, client, results, &wg)
	}

	wg.Wait()
	close(results)

	for mood := range results {
		fmt.Printf("URL: %s\n", mood.URL)
		statusMsg := fmt.Sprintf("  Status: %d", mood.StatusCode)
		if mood.Error != nil {
			statusMsg = fmt.Sprintf("  Status: %d (Error)", mood.StatusCode)
		}
		fmt.Println(statusMsg)
		fmt.Printf("  Latency: %s\n", mood.Latency)
		fmt.Printf("  Mood: %s\n\n", mood.Description)
	}
}
