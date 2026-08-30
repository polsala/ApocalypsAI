package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "time"
)

var inspirational = []string{
    "The sun rises",
    "Hope blooms",
    "Dreams awaken",
    "Stars guide us",
    "New horizons appear",
}

var apocalypse = []string{
    "but the shadows whisper",
    "while the winds howl",
    "as the earth cracks",
    "when the night devours",
    "as the silence screams",
}

type Quote struct {
    Quote string `json:"quote"`
}

func mixedQuote() string {
    rand.Seed(time.Now().UnixNano())
    i := inspirational[rand.Intn(len(inspirational))]
    a := apocalypse[rand.Intn(len(apocalypse))]
    return i + ", " + a + "."
}

func handler(w http.ResponseWriter, r *http.Request) {
    q := Quote{Quote: mixedQuote()}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(q)
}

func main() {
    http.HandleFunc("/quote", handler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatal(err)
    }
}
