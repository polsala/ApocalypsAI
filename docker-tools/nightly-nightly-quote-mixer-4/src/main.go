package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var postApoc = []string{
    "The sky bleeds ash.",
    "Silence is the new thunder.",
    "We walk the ruins of yesterday.",
    "Dust whispers the names of the lost.",
}

var inspirational = []string{
    "Believe in yourself.",
    "Every day is a new beginning.",
    "Dreams are the seeds of reality.",
    "Courage is the fire within.",
}

// generateMixedQuote creates a mixed quote using the provided random source.
func generateMixedQuote(r *rand.Rand) string {
    pa := postApoc[r.Intn(len(postApoc))]
    insp := inspirational[r.Intn(len(inspirational))]
    return pa + " " + insp
}

// quoteHandler handles HTTP requests and returns a JSON quote.
func quoteHandler(w http.ResponseWriter, r *http.Request) {
    rnd := rand.New(rand.NewSource(time.Now().UnixNano()))
    q := generateMixedQuote(rnd)
    resp := map[string]string{"quote": q}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/quote", quoteHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
