package main

import (
	"crypto/sha256"
	"encoding/hex"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

// HTTPClient defines the interface for making HTTP requests.
// This allows for easy mocking in tests.
type HTTPClient interface {
	Get(url string) (*http.Response, error)
}

// RealHTTPClient implements HTTPClient using the standard http.Client.
type RealHTTPClient struct {
	Client *http.Client
}

func (r *RealHTTPClient) Get(url string) (*http.Response, error) {
	return r.Client.Get(url)
}

// URLState stores the last known state of a URL.
type URLState struct {
	ContentHash string
	LatencyMs   int64
	LastChecked time.Time
}

// ChronoWatchdog monitors a list of URLs for changes.
type ChronoWatchdog struct {
	URLs     []string
	Interval time.Duration
	Client   HTTPClient
	states   map[string]URLState
	mu       sync.Mutex // Protects access to the states map
	logger   *log.Logger // For outputting reports
}

// NewChronoWatchdog creates a new ChronoWatchdog instance.
func NewChronoWatchdog(urls []string, interval time.Duration, client HTTPClient, logger *log.Logger) *ChronoWatchdog {
	if client == nil {
		client = &RealHTTPClient{Client: &http.Client{Timeout: 10 * time.Second}}
	}
	if logger == nil {
		logger = log.New(io.Discard, "", 0) // Default to discarding logs if not provided
	}
	return &ChronoWatchdog{
		URLs:     urls,
		Interval: interval,
		Client:   client,
		states:   make(map[string]URLState),
		logger:   logger,
	}
}

// StartMonitoring begins the periodic monitoring of URLs.
func (cw *ChronoWatchdog) StartMonitoring(stopCh chan struct{}) {
	cw.logger.Printf("Starting Chrono-Watchdog for %d URLs, checking every %s\n", len(cw.URLs), cw.Interval)
	ticker := time.NewTicker(cw.Interval)
	defer ticker.Stop()

	// Initial check
	cw.checkAllURLs()

	for {
		select {
		case <-ticker.C:
			cw.checkAllURLs()
		case <-stopCh:
			cw.logger.Println("Chrono-Watchdog stopped.")
			return
		}
	}
}

func (cw *ChronoWatchdog) checkAllURLs() {
	var wg sync.WaitGroup
	for _, url := range cw.URLs {
		wg.Add(1)
		go func(u string) {
			defer wg.Done()
			cw.checkURL(u)
		}(url)
	}
	wg.Wait()
}

func (cw *ChronoWatchdog) checkURL(url string) {
	start := time.Now()
	resp, err := cw.Client.Get(url)
	latency := time.Since(start).Milliseconds()

	if err != nil {
		cw.logger.Printf("[ERROR] Failed to fetch %s: %v (Latency: %dms)\n", url, err, latency)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		cw.logger.Printf("[WARNING] %s returned status %d (Latency: %dms)\n", url, resp.StatusCode, latency)
		return
	}

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		cw.logger.Printf("[ERROR] Failed to read body for %s: %v (Latency: %dms)\n", url, err, latency)
		return
	}

	hasher := sha256.New()
	hasher.Write(bodyBytes)
	currentHash := hex.EncodeToString(hasher.Sum(nil))

	cw.mu.Lock()
	prevState, exists := cw.states[url]
	cw.states[url] = URLState{
		ContentHash: currentHash,
		LatencyMs:   latency,
		LastChecked: time.Now(),
	}
	cw.mu.Unlock()

	if !exists {
		cw.logger.Printf("[INFO] Initial check for %s: Hash=%s, Latency=%dms\n", url, currentHash, latency)
		return
	}

	if prevState.ContentHash != currentHash {
		cw.logger.Printf("[ANOMALY] Content change detected for %s!\n  Old Hash: %s\n  New Hash: %s\n  Latency: %dms\n",
			url, prevState.ContentHash, currentHash, latency)
	} else if latency > prevState.LatencyMs*2 && prevState.LatencyMs > 0 { // Simple latency anomaly: more than double previous, and previous wasn't zero
		cw.logger.Printf("[ANOMALY] Significant latency increase for %s!\n  Old Latency: %dms\n  New Latency: %dms\n  Content Hash: %s\n",
			url, prevState.LatencyMs, latency, currentHash)
	} else {
		cw.logger.Printf("[INFO] %s: No significant changes. Hash=%s, Latency=%dms\n", url, currentHash, latency)
	}
}

func main() {
	urlsStr := flag.String("urls", "", "Comma-separated list of URLs to monitor")
	intervalStr := flag.String("interval", "1m", "Check interval (e.g., 30s, 5m, 1h)")
	flag.Parse()

	if *urlsStr == "" {
		log.Fatal("Error: --urls flag is required.")
	}

	urls := strings.Split(*urlsStr, ",")
	interval, err := time.ParseDuration(*intervalStr)
	if err != nil {
		log.Fatalf("Error parsing interval: %v", err)
	}

	// Use a standard logger for main execution
	mainLogger := log.New(os.Stdout, "", log.LstdFlags)

	watchdog := NewChronoWatchdog(urls, interval, nil, mainLogger) // nil for default HTTP client
	stopCh := make(chan struct{})

	// Handle graceful shutdown
	go func() {
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
		<-sigCh
		close(stopCh)
	}()

	watchdog.StartMonitoring(stopCh)
}
