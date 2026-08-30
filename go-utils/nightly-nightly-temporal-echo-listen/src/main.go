package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)

// Echo represents a temporal echo message
type Echo struct {
	Source    string    `json:"source"`
	Message   string    `json:"message"`
	Timestamp time.Time `json:"timestamp"`
}

// EchoStore holds all received echoes
type EchoStore struct {
	mu     sync.Mutex
	echoes []Echo
}

// AddEcho adds a new echo to the store
func (es *EchoStore) AddEcho(echo Echo) {
	es.mu.Lock()
	defer es.mu.Unlock()
	es.echoes = append(es.echoes, echo)
}

// GetEchoes returns a copy of all echoes
func (es *EchoStore) GetEchoes() []Echo {
	es.mu.Lock()
	defer es.mu.Unlock()
	// Return a copy to prevent external modification
	echoesCopy := make([]Echo, len(es.echoes))
	copy(echoesCopy, es.echoes)
	return echoesCopy
}

// echoHandler handles incoming POST requests for echoes
func echoHandler(store *EchoStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
			return
		}

		var echo Echo
		err := json.NewDecoder(r.Body).Decode(&echo)
		if err != nil {
			http.Error(w, "Invalid request body", http.StatusBadRequest)
			return
		}

		echo.Timestamp = time.Now().UTC() // Set server-side timestamp
		store.AddEcho(echo)

		w.WriteHeader(http.StatusAccepted)
		fmt.Fprintf(w, "Echo received from %s\n", echo.Source)
	}
}

// summaryHandler provides a summary of all echoes
func summaryHandler(store *EchoStore) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
			return
		}

		echoes := store.GetEchoes()
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(echoes)
	}
}

func main() {
	echoStore := &EchoStore{
		echoes: make([]Echo, 0),
	}

	http.HandleFunc("/echo", echoHandler(echoStore))
	http.HandleFunc("/summary", summaryHandler(echoStore))

	port := ":8080"
	log.Printf("Temporal Echo Listener starting on port %s", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
