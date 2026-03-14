package main

import (
    "encoding/json"
    "flag"
    "log"
    "net/http"
    "strconv"
    "sync"
    "time"
)

type Message struct {
    Text      string    `json:"msg"`
    Timestamp time.Time `json:"timestamp"`
}

type Store struct {
    msgs      []Message
    mu        sync.Mutex
    retention time.Duration
}

func NewStore(retention time.Duration) *Store {
    return &Store{
        msgs:      make([]Message, 0),
        retention: retention,
    }
}

func (s *Store) Add(text string) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.msgs = append(s.msgs, Message{
        Text:      text,
        Timestamp: time.Now().UTC(),
    })
}

func (s *Store) Get() []Message {
    s.mu.Lock()
    defer s.mu.Unlock()
    cutoff := time.Now().UTC().Add(-s.retention)
    var out []Message
    for _, m := range s.msgs {
        if m.Timestamp.After(cutoff) {
            out = append(out, m)
        }
    }
    return out
}

// NewHandler returns an http.Handler with the service routes.
// Exported for testing.
func NewHandler(s *Store) http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("/bottle", func(w http.ResponseWriter, r *http.Request) {
        switch r.Method {
        case http.MethodPost:
            var payload struct {
                Msg string `json:"msg"`
            }
            if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
                http.Error(w, "invalid json", http.StatusBadRequest)
                return
            }
            s.Add(payload.Msg)
            w.WriteHeader(http.StatusOK)
        case http.MethodGet:
            msgs := s.Get()
            w.Header().Set("Content-Type", "application/json")
            json.NewEncoder(w).Encode(msgs)
        default:
            http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
        }
    })
    return mux
}

func main() {
    port := flag.Int("port", 8080, "Port to listen on")
    retentionMin := flag.Int("retention", 10, "Retention time in minutes")
    flag.Parse()

    store := NewStore(time.Duration(*retentionMin) * time.Minute)
    handler := NewHandler(store)

    addr := ":" + strconv.Itoa(*port)
    log.Printf("Starting bottle service on %s with retention %d minutes", addr, *retentionMin)
    if err := http.ListenAndServe(addr, handler); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
