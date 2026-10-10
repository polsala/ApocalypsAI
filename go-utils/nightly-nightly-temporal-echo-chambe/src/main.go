package main

import (
	"bytes"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"
)

var (
	listenPort  = flag.Int("port", 8080, "Port to listen for incoming messages")
	outputURL   = flag.String("output-url", "", "URL to re-broadcast messages to (e.g., http://localhost:8081/echo)")
	delayMillis = flag.Int("delay", 5000, "Delay in milliseconds before re-broadcasting the message")
	
	// osExit is a variable to allow mocking os.Exit in tests.
	osExit = os.Exit 
)

func main() {
	flag.Parse()

	if *outputURL == "" {
		log.Println("Error: --output-url is required.")
		osExit(1)
	}

	log.Printf("Starting Temporal Echo Chamber on :%d", *listenPort)
	log.Printf("Messages will be delayed by %dms and sent to %s", *delayMillis, *outputURL)

	http.HandleFunc("/echo", echoHandler)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", *listenPort), nil))
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Only POST method is supported", http.StatusMethodNotAllowed)
		return
	}

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusInternalServerError)
		return
	}
	defer r.Body.Close()

	log.Printf("Received message (size: %d bytes) from %s", len(body), r.RemoteAddr)

	// Start a goroutine to handle the delayed re-broadcast
	go echoMessage(body, r.Header)

	w.WriteHeader(http.StatusAccepted)
	fmt.Fprintln(w, "Message accepted for temporal echoing.")
}

func echoMessage(body []byte, headers http.Header) {
	delay := time.Duration(*delayMillis) * time.Millisecond
	time.Sleep(delay)

	client := &http.Client{}
	req, err := http.NewRequest(http.MethodPost, *outputURL, bytes.NewBuffer(body))
	if err != nil {
		log.Printf("Error creating re-broadcast request: %v", err)
		return
	}

	// Copy relevant headers, e.g., Content-Type
	if contentType := headers.Get("Content-Type"); contentType != "" {
		req.Header.Set("Content-Type", contentType)
	}
	// Add a custom header to indicate the delay applied
	req.Header.Set("X-Temporal-Echo-Delay", fmt.Sprintf("%dms", *delayMillis))

	resp, err := client.Do(req)
	if err != nil {
		log.Printf("Error re-broadcasting message to %s: %v", *outputURL, err)
		return
	}
	defer resp.Body.Close()

	log.Printf("Message re-broadcasted to %s after %dms delay. Status: %s", *outputURL, *delayMillis, resp.Status)
}
