package main

import (
    "encoding/json"
    "log"
    "net/http"
)

var moodMap = map[string]string{
    "happy":   "😊",
    "sad":     "😢",
    "angry":   "😠",
    "neutral": "😐",
}

func emojiHandler(w http.ResponseWriter, r *http.Request) {
    mood := r.URL.Query().Get("mood")
    emoji, ok := moodMap[mood]
    if !ok {
        emoji = "🤔"
    }
    resp := map[string]string{"emoji": emoji}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/emoji", emojiHandler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
