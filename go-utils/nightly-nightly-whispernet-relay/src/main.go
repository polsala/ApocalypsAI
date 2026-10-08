package main

import (
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"sync"
	"time"
)

// Whisper represents a single ephemeral message
type Whisper struct {
	Content   []byte
	ExpiresAt time.Time
}

// WhisperStore manages the storage and retrieval of whispers
type WhisperStore struct {
	mu        sync.RWMutex
	whispers  map[string]Whisper
	defaultTTL time.Duration
}

// NewWhisperStore creates a new WhisperStore with a given default TTL
func NewWhisperStore(ttl time.Duration) *WhisperStore {
	return &WhisperStore{
		whispers:  make(map[string]Whisper),
		defaultTTL: ttl,
	}
}

// PostWhisper adds a new whisper to the store. Returns true if successful, false if channel already exists.
func (ws *WhisperStore) PostWhisper(channelID string, content []byte) bool {
	ws.mu.Lock()
	defer ws.mu.Unlock()

	if _, exists := ws.whispers[channelID]; exists {
		return false // Channel already has a whisper
	}

	ws.whispers[channelID] = Whisper{
		Content:   content,
		ExpiresAt: time.Now().Add(ws.defaultTTL),
	}
	log.Printf("Whisper posted to channel '%s', expires in %v", channelID, ws.defaultTTL)
	return true
}

// GetWhisper retrieves and removes a whisper from the store. Returns content and true if found, nil and false otherwise.
func (ws *WhisperStore) GetWhisper(channelID string) ([]byte, bool) {
	ws.mu.Lock()
	defer ws.mu.Unlock()

	whisper, found := ws.whispers[channelID]
	if !found {
		return nil, false
	}

	delete(ws.whispers, channelID)
	log.Printf("Whisper retrieved and deleted from channel '%s'", channelID)
	return whisper.Content, true
}

// CleanExpiredWhispers removes any whispers that have passed their expiration time.
func (ws *WhisperStore) CleanExpiredWhispers() {
	ws.mu.Lock()
	defer ws.mu.Unlock()

	now := time.Now()
	for channelID, whisper := range ws.whispers {
		if now.After(whisper.ExpiresAt) {
			delete(ws.whispers, channelID)
			log.Printf("Whisper in channel '%s' expired and was cleaned up.", channelID)
		}
	}
}

// GetWhisperCount returns the current number of whispers in the store.
func (ws *WhisperStore) GetWhisperCount() int {
	ws.mu.RLock()
	defer ws.mu.RUnlock()
	return len(ws.whispers)
}

// Server handles HTTP requests for the WhisperNet Relay
type Server struct {
	store *WhisperStore
}

// NewServer creates a new Server instance
func NewServer(store *WhisperStore) *Server {
	return &Server{store: store}
}

// postWhisperHandler handles POST requests to /whisper/{channel_id}
func (s *Server) postWhisperHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	channelID := r.URL.Path[len("/whisper/"):]
	if channelID == "" {
		http.Error(w, "Channel ID is required", http.StatusBadRequest)
		return
	}

	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Failed to read request body", http.StatusInternalServerError)
		return
	}
	if len(body) == 0 {
		http.Error(w, "Message body cannot be empty", http.StatusBadRequest)
		return
	}

	if s.store.PostWhisper(channelID, body) {
		w.WriteHeader(http.StatusCreated)
		fmt.Fprintf(w, "Whisper posted to channel '%s'\n", channelID)
	} else {
		http.Error(w, "Whisper already exists for this channel", http.StatusConflict)
	}
}

// getWhisperHandler handles GET requests to /whisper/{channel_id}
func (s *Server) getWhisperHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return
	}

	channelID := r.URL.Path[len("/whisper/"):]
	if channelID == "" {
		http.Error(w, "Channel ID is required", http.StatusBadRequest)
		return
	}

	content, found := s.store.GetWhisper(channelID)
	if found {
		w.Header().Set("Content-Type", "application/octet-stream") // Or whatever was sent
		w.WriteHeader(http.StatusOK)
		_, _ = w.Write(content)
	} else {
		http.Error(w, "Whisper not found or expired", http.StatusNotFound)
	}
}

func main() {
	port := flag.Int("port", 8080, "Port to listen on")
	ttlStr := flag.String("ttl", "5m", "Default Time-To-Live for whispers (e.g., 1m, 10s, 1h)")
	flag.Parse()

	ttl, err := time.ParseDuration(*ttlStr)
	if err != nil {
		log.Fatalf("Invalid TTL duration: %v", err)
	}

	store := NewWhisperStore(ttl)
	server := NewServer(store)

	// Start background goroutine for cleaning expired whispers
	go func() {
		ticker := time.NewTicker(1 * time.Minute) // Check every minute
		defer ticker.Stop()
		for range ticker.C {
			store.CleanExpiredWhispers()
		}
	}()

	http.HandleFunc("/whisper/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			server.postWhisperHandler(w, r)
		} else if r.Method == http.MethodGet {
			server.getWhisperHandler(w, r)
		} else {
			http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		}
	})

	log.Printf("WhisperNet Relay starting on port %d with default TTL %v", *port, ttl)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", *port), nil))
}
