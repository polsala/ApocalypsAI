package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"sync"
	"time"
)

// MessagePayload represents the data sent to a listening post
type MessagePayload struct {
	Message   string `json:"message"`
	Timestamp string `json:"timestamp"`
}

// ListeningPost represents a target for the whisper
type ListeningPost struct {
	Name string
	URL  string
}

// HTTPClient interface for mocking HTTP requests
type HTTPClient interface {
	Post(url, contentType string, body *bytes.Buffer) (*http.Response, error)
}

// RealHTTPClient implements HTTPClient using net/http
type RealHTTPClient struct {
	Client *http.Client
}

// Post makes a real HTTP POST request
func (r *RealHTTPClient) Post(url, contentType string, body *bytes.Buffer) (*http.Response, error) {
	return r.Client.Post(url, contentType, body)
}

// obfuscateMessage applies a whimsical distortion to the message using a ROT13-like shift.
func obfuscateMessage(msg string) string {
	runes := []rune(msg)
	for i, r := range runes {
		if r >= 'a' && r <= 'z' {
			runes[i] = 'a' + (r-'a'+13)%26
		} else if r >= 'A' && r <= 'Z' {
			runes[i] = 'A' + (r-'A'+13)%26
		}
	}
	return string(runes) + " [echoed]"
}

// sendWhisperToPost simulates sending a message to a single listening post.
// It uses the provided HTTPClient for network operations and reports results via a channel.
func sendWhisperToPost(client HTTPClient, post ListeningPost, obfuscatedMessage string, wg *sync.WaitGroup, results chan<- string) {
	defer wg.Done()

	// Simulate temporal distortion (random delay)
	delay := time.Duration(rand.Intn(500)+100) * time.Millisecond // 100ms to 600ms
	time.Sleep(delay)

	payload := MessagePayload{
		Message:   obfuscatedMessage,
		Timestamp: time.Now().Format(time.RFC3339),
	}
	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		results <- fmt.Sprintf("Failed to marshal payload for %s: %v", post.Name, err)
		return
	}

	body := bytes.NewBuffer(jsonPayload)

	resp, err := client.Post(post.URL, "application/json", body)
	if err != nil {
		results <- fmt.Sprintf("Error sending to %s (%s): %v", post.Name, post.URL, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		responseBody, _ := ioutil.ReadAll(resp.Body)
		results <- fmt.Sprintf("Failed to send to %s (%s). Status: %d, Response: %s", post.Name, post.URL, resp.StatusCode, string(responseBody))
		return
	}

	results <- fmt.Sprintf("Successfully echoed to %s (%s) after %v", post.Name, post.URL, delay)
}

// broadcastWhisper concurrently sends an obfuscated message to multiple listening posts.
// It returns a slice of strings detailing the outcome for each post.
func broadcastWhisper(message string, posts []ListeningPost, client HTTPClient) []string {
	obfuscatedMsg := obfuscateMessage(message)
	log.Printf("Original message: \"%s\"", message)
	log.Printf("Obfuscated whisper: \"%s\"", obfuscatedMsg)
	log.Printf("Broadcasting to %d listening posts...", len(posts))

	var wg sync.WaitGroup
	results := make(chan string, len(posts)) // Buffered channel for results

	for _, post := range posts {
		wg.Add(1)
		go sendWhisperToPost(client, post, obfuscatedMsg, &wg, results)
	}

	wg.Wait()      // Wait for all goroutines to finish
	close(results) // Close the channel when all sends are done

	var finalResults []string
	for res := range results {
		finalResults = append(finalResults, res)
	}
	return finalResults
}

func main() {
	rand.Seed(time.Now().UnixNano()) // Seed for random delays

	if len(os.Args) < 2 {
		fmt.Println("Usage: nightly-echo-chamber-relay <message>")
		os.Exit(1)
	}

	message := os.Args[1]

	// Define some whimsical listening posts (mock URLs for demonstration)
	listeningPosts := []ListeningPost{
		{Name: "Whisperwind Spire", URL: "http://localhost:8081/receive"},
		{Name: "Temporal Beacon 7", URL: "http://localhost:8082/receive"},
		{Name: "Echoing Cavern Node", URL: "http://localhost:8083/receive"},
		{Name: "Silent Sentinel Hub", URL: "http://localhost:8084/receive"},
	}

	// Use a real HTTP client for the main execution
	realClient := &RealHTTPClient{Client: &http.Client{Timeout: 2 * time.Second}}

	finalResults := broadcastWhisper(message, listeningPosts, realClient)

	fmt.Println("\n--- Broadcast Summary ---")
	for _, res := range finalResults {
		fmt.Println(res)
	}
}
