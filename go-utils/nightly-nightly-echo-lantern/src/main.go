package main

import (
    "encoding/json"
    "io"
    "log"
    "net/http"
)

type EchoResponse struct {
    Echo    string `json:"echo"`
    Lantern string `json:"lantern"`
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
    body, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "failed to read body", http.StatusBadRequest)
        return
    }
    defer r.Body.Close()

    resp := EchoResponse{
        Echo:    string(body),
        Lantern: "🏮",
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func NewHandler() http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("/echo", echoHandler)
    return mux
}

func main() {
    log.Println("Starting Nightly Echo Lantern on :8080")
    if err := http.ListenAndServe(":8080", NewHandler()); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
