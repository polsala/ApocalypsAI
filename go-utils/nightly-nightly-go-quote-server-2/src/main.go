package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "sync"
    "time"
)

// QuoteHandler holds the quotes and a mutex for safe concurrent access.
type QuoteHandler struct {
    quotes []string
    mu     sync.RWMutex
    rng    *rand.Rand
}

// NewQuoteHandler creates a new QuoteHandler with the provided quotes.
func NewQuoteHandler(quotes []string) *QuoteHandler {
    src := rand.NewSource(time.Now().UnixNano())
    return &QuoteHandler{
        quotes: quotes,
        rng:    rand.New(src),
    }
}

// randomQuote returns a random quote from the slice.
func (qh *QuoteHandler) randomQuote() string {
    qh.mu.RLock()
    defer qh.mu.RUnlock()
    if len(qh.quotes) == 0 {
        return ""
    }
    idx := qh.rng.Intn(len(qh.quotes))
    return qh.quotes[idx]
}

// ServeHTTP implements http.Handler for the /quote endpoint.
func (qh *QuoteHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    quote := qh.randomQuote()
    resp := map[string]string{"quote": quote}
    w.Header().Set("Content-Type", "application/json")
    _ = json.NewEncoder(w).Encode(resp)
}

// healthHandler returns a simple OK response.
func healthHandler(w http.ResponseWriter, r *http.Request) {
    w.WriteHeader(http.StatusOK)
    _, _ = w.Write([]byte("OK"))
}

// NewServer creates an http.Handler with all routes registered.
func NewServer(quotes []string) http.Handler {
    mux := http.NewServeMux()
    mux.Handle("/quote", NewQuoteHandler(quotes))
    mux.HandleFunc("/health", healthHandler)
    return mux
}

func main() {
    // Default quotes; can be customized by editing the source.
    defaultQuotes := []string{
        "The early bird catches the worm.",
        "Fortune favors the bold.",
        "Keep calm and code on.",
        "To err is human; to debug, divine.",
    }
    handler := NewServer(defaultQuotes)
    addr := ":8080"
    log.Printf("Starting quote server on %s", addr)
    if err := http.ListenAndServe(addr, handler); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
