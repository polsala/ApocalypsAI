package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "os"
    "strconv"
    "time"
)

var phrases = []string{
    "The sky cracks like shattered glass",
    "Radiation whispers through the ruins",
    "Dust devours the horizon",
    "Silence screams in the wasteland",
    "Ashes rain from the dying sun",
    "The last beacon flickers out",
}

type response struct {
    Original string `json:"original"`
    Doom     string `json:"doom"`
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
    msg := r.URL.Query().Get("msg")
    if msg == "" {
        http.Error(w, "missing 'msg' query parameter", http.StatusBadRequest)
        return
    }
    idx := rand.Intn(len(phrases))
    resp := response{Original: msg, Doom: phrases[idx]}
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    rand.Seed(time.Now().UnixNano())

    port := 8080
    if p := os.Getenv("PORT"); p != "" {
        if v, err := strconv.Atoi(p); err == nil {
            port = v
        }
    }

    http.HandleFunc("/echo", echoHandler)
    addr := ":" + strconv.Itoa(port)
    log.Printf("Starting apocalypse echo server on %s", addr)
    if err := http.ListenAndServe(addr, nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
