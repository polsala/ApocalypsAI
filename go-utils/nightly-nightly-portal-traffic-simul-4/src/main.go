package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "sync/atomic"
    "time"
)

var requestCount uint64

var messages = []string{
    "Welcome, wanderer of the wasteland!",
    "Your destiny awaits beyond the portal.",
    "Beware the temporal rift, traveler.",
    "May the void whisper sweet nothings.",
    "You have entered the realm of endless possibilities.",
}

func greetHandler(w http.ResponseWriter, r *http.Request) {
    atomic.AddUint64(&requestCount, 1)
    // Seed with current time for runtime randomness
    rand.Seed(time.Now().UnixNano())
    msg := messages[rand.Intn(len(messages))]
    resp := map[string]string{"message": msg}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func statsHandler(w http.ResponseWriter, r *http.Request) {
    count := atomic.LoadUint64(&requestCount)
    resp := map[string]uint64{"total_requests": count}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/greet", greetHandler)
    http.HandleFunc("/stats", statsHandler)
    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
