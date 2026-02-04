package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"sync"
	"time"
)

// RecordedRequest stores the details of an incoming HTTP request.
type RecordedRequest struct {
	Timestamp string            `json:"timestamp"`
	Method    string            `json:"method"`
	URL       string            `json:"url"`
	Headers   map[string][]string `json:"headers"`
	Body      string            `json:"body"`
}

var (
	recordedRequests []RecordedRequest
	mu               sync.Mutex // Mutex to protect access to recordedRequests
)

// echoHandler records the incoming request and responds.
func echoHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	bodyBytes, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusInternalServerError)
		log.Printf("Error reading body: %v", err)
		return
	}
	defer r.Body.Close()

	// Clone headers to avoid modifying the original map if it's reused
	headers := make(map[string][]string)
	for k, v := range r.Header {
		headers[k] = v
	}

	recordedRequests = append(recordedRequests, RecordedRequest{
		Timestamp: time.Now().Format(time.RFC3339),
		Method:    r.Method,
		URL:       r.URL.String(),
		Headers:   headers,
		Body:      string(bodyBytes),
	})

	log.Printf("Recorded request: %s %s", r.Method, r.URL.String())
	fmt.Fprintf(w, "Request recorded successfully!\n")
}

// historyHandler returns all recorded requests as JSON.
func historyHandler(w http.ResponseWriter, r *http.Request) {
	mu.Lock()
	defer mu.Unlock()

	w.Header().Set("Content-Type", "application/json")
	encoder := json.NewEncoder(w)
	encoder.SetIndent("", "  ") // Pretty print JSON
	if err := encoder.Encode(recordedRequests);
		err != nil {
			http.Error(w, "Failed to encode history", http.StatusInternalServerError)
			log.Printf("Error encoding history: %v", err)
			return
	}
}

func main() {
	http.HandleFunc("/echo/", echoHandler) // Catch all paths under /echo/
	http.HandleFunc("/history", historyHandler)

	port := ":8080"
	log.Printf("Temporal Replay Box listening on port %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
