package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "sync"
    "time"
)

type Quote struct {
    Text   string `json:"text"`
    Author string `json:"author"`
}

var quotes = []Quote{
    {"The only limit to our realization of tomorrow is our doubts of today.", "Franklin D. Roosevelt"},
    {"In the middle of difficulty lies opportunity.", "Albert Einstein"},
    {"Do not go gentle into that good night.", "Dylan Thomas"},
    {"When the world ends, at least we have coffee.", "Anonymous"},
}

type QuoteCache struct {
    mu   sync.RWMutex
    last Quote
    ts   time.Time
    ttl  time.Duration
}

func NewQuoteCache(ttl time.Duration) *QuoteCache {
    return &QuoteCache{ttl: ttl}
}

func (c *QuoteCache) Get() Quote {
    c.mu.RLock()
    if time.Since(c.ts) < c.ttl {
        q := c.last
        c.mu.RUnlock()
        return q
    }
    c.mu.RUnlock()
    // cache miss – acquire write lock
    c.mu.Lock()
    defer c.mu.Unlock()
    // double‑check after acquiring write lock
    if time.Since(c.ts) < c.ttl {
        return c.last
    }
    q := quotes[rand.Intn(len(quotes))]
    c.last = q
    c.ts = time.Now()
    return q
}

func quoteHandler(cache *QuoteCache) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        q := cache.Get()
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(q)
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    cache := NewQuoteCache(5 * time.Second)
    http.HandleFunc("/quote", quoteHandler(cache))
    log.Println("Starting server on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
