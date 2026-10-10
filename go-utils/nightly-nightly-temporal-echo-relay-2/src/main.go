package main

import (
	"encoding/json"
	"log"
	"math/rand"
	"net/http"
	"os"
	"strings"
	"time"
)

// RequestPayload defines the structure of the incoming JSON request
type RequestPayload struct {
	Message        string  `json:"message"`
	DelayMs        int     `json:"delay_ms"`
	CorruptionLevel float64 `json:"corruption_level"` // 0.0 to 1.0
}

// ResponsePayload defines the structure of the outgoing JSON response
type ResponsePayload struct {
	OriginalMessage   string `json:"original_message"`
	CorruptedMessage string `json:"corrupted_message"`
	DelayAppliedMs    int    `json:"delay_applied_ms"`
}

// sleeper is an interface to allow mocking time.Sleep in tests
type sleeper interface {
	Sleep(d time.Duration)
}

// realSleeper implements the sleeper interface using time.Sleep
type realSleeper struct{}

func (rs realSleeper) Sleep(d time.Duration) {
	time.Sleep(d)
}

// echoHandler handles incoming echo requests
func echoHandler(s sleeper, r *rand.Rand) http.HandlerFunc {
	return func(w http.ResponseWriter, req *http.Request) {
		if req.Method != http.MethodPost {
			http.Error(w, "Only POST requests are accepted", http.StatusMethodNotAllowed)
			return
		}

		var payload RequestPayload
		err := json.NewDecoder(req.Body).Decode(&payload)
		if err != nil {
			http.Error(w, "Invalid request payload", http.StatusBadRequest)
			return
		}

		log.Printf("Received message: \"%s\" with delay %dms, corruption %.2f",
			payload.Message, payload.DelayMs, payload.CorruptionLevel)

		// Apply delay
		if payload.DelayMs > 0 {
			s.Sleep(time.Duration(payload.DelayMs) * time.Millisecond)
		}

		// Apply corruption
		corruptedMsg := corruptMessage(payload.Message, payload.CorruptionLevel, r)

		response := ResponsePayload{
			OriginalMessage:   payload.Message,
			CorruptedMessage: corruptedMsg,
			DelayAppliedMs:    payload.DelayMs,
		}

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
	}
}

// corruptMessage applies a simulated corruption to the message
func corruptMessage(msg string, level float64, r *rand.Rand) string {
	if level <= 0.0 {
		return msg
	}
	if level > 1.0 {
		level = 1.0 // Cap corruption level
	}

	runes := []rune(msg)
	for i := 0; i < len(runes); i++ {
		if r.Float64() < level {
			// Apply a random corruption effect
			effect := r.Intn(3) // 0: case change, 1: char swap, 2: char replacement
			switch effect {
			case 0: // Case change
				charStr := string(runes[i])
				if strings.ToLower(charStr) == charStr {
					runes[i] = []rune(strings.ToUpper(charStr))[0]
				} else {
					runes[i] = []rune(strings.ToLower(charStr))[0]
				}
			case 1: // Character swap with adjacent (if possible)
				if i+1 < len(runes) {
					runes[i], runes[i+1] = runes[i+1], runes[i]
					i++ // Skip next char as it was just swapped
				}
			case 2: // Character replacement
				// Replace with a random printable ASCII character (33-126)
				runes[i] = rune(r.Intn(94) + 33)
			}
		}
	}
	return string(runes)
}

func main() {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Initialize a random source for corruption
	// Use a non-deterministic source for the actual service
	source := rand.NewSource(time.Now().UnixNano())
	globalRand := rand.New(source)

	log.Printf("Starting Temporal Echo Relay service on :%s", port)
	http.HandleFunc("/echo", echoHandler(realSleeper{}, globalRand))
	log.Fatal(http.ListenAndServe(":"+port, nil))
}
