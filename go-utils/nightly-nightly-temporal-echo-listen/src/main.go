package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"sync"
	"time"
)

// Echo represents a received HTTP request
type Echo struct {
	Timestamp   time.Time         `json:"timestamp"`
	RemoteAddr  string            `json:"remote_addr"`
	Method      string            `json:"method"`
	Path        string            `json:"path"`
	Headers     map[string]string `json:"headers"`
	BodySnippet string            `json:"body_snippet"`
}

// EchoLogger is a concurrency-safe logger for echoes
type EchoLogger struct {
	mu     sync.Mutex
	writer io.Writer
}

func NewEchoLogger(w io.Writer) *EchoLogger {
	return &EchoLogger{writer: w}
}

func (l *EchoLogger) Log(echo Echo) {
	l.mu.Lock()
	defer l.mu.Unlock()

	echoJSON, err := json.Marshal(echo)
	if err != nil {
		log.Printf("Error marshalling echo: %v", err)
		return
	}
	fmt.Fprintf(l.writer, "%s\n", echoJSON)
}

// EchoHandler handles incoming HTTP requests
func EchoHandler(logger *EchoLogger, forwardURL string) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		bodyBytes, err := io.ReadAll(r.Body)
		if err != nil {
			http.Error(w, "Failed to read request body", http.StatusInternalServerError)
			return
		}
		r.Body.Close() // Close the original body

		headers := make(map[string]string)
		for name, values := range r.Header {
			if len(values) > 0 {
				headers[name] = values[0] // Take the first value for simplicity
			}
		}

		bodySnippet := string(bodyBytes)
		if len(bodySnippet) > 200 { // Limit body snippet length
			bodySnippet = bodySnippet[:200] + "..."
		}

		echo := Echo{
			Timestamp:   time.Now().UTC(),
			RemoteAddr:  r.RemoteAddr,
			Method:      r.Method,
			Path:        r.URL.Path,
			Headers:     headers,
			BodySnippet: bodySnippet,
		}

		// Log the echo concurrently
		go logger.Log(echo)

		// Forward the echo if a forward URL is provided
		if forwardURL != "" {
			go func() {
				client := &http.Client{Timeout: 5 * time.Second}
				req, err := http.NewRequest(r.Method, forwardURL+r.URL.Path, bytes.NewReader(bodyBytes))
				if err != nil {
					log.Printf("Error creating forward request: %v", err)
					return
				}
				req.Header = r.Header // Copy all headers
				resp, err := client.Do(req)
				if err != nil {
					log.Printf("Error forwarding echo to %s: %v", forwardURL, err)
					return
				}
				defer resp.Body.Close()
				// Optionally log forward response status
				// log.Printf("Forwarded echo to %s, status: %s", forwardURL, resp.Status)
			}()
		}

		w.Header().Set("Content-Type", "text/plain")
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "Temporal echo received and processed at %s!\n", echo.Timestamp.Format(time.RFC3339))
	}
}

func main() {
	port := flag.Int("port", 8080, "Port to listen on for temporal echoes")
	logFile := flag.String("log-file", "", "Path to a file to log echoes (defaults to stdout if empty)")
	forwardURL := flag.String("forward-url", "", "Optional URL to forward received echoes to")
	flag.Parse()

	var writer io.Writer = os.Stdout
	if *logFile != "" {
		f, err := os.OpenFile(*logFile, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatalf("Failed to open log file %s: %v", *logFile, err)
		}
		defer f.Close()
		writer = f
	}

	logger := NewEchoLogger(writer)

	http.HandleFunc("/", EchoHandler(logger, *forwardURL))

	log.Printf("Nightly Temporal Echo Listener starting on port %d...", *port)
	log.Printf("Echoes will be logged to %s", *logFile)
	if *forwardURL != "" {
		log.Printf("Echoes will also be forwarded to %s", *forwardURL)
	}

	addr := fmt.Sprintf(":%d", *port)
	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
