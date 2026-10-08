package main

import (
    "encoding/json"
    "log"
    "math/rand"
    "net/http"
    "sync"
    "time"
)

var tips = []string{
    "Always keep a spare can of beans in your backpack.",
    "Never trust a stranger with a shiny object.",
    "Water is more valuable than gold in the wasteland.",
    "A good map is worth a thousand miles of wandering.",
    "Keep your eyes on the horizon and your ears to the ground.",
}

type tipResponse struct {
    Tip string `json:"tip"`
}

func main() {
    rand.Seed(time.Now().UnixNano())
    var mu sync.Mutex // protect log output

    http.HandleFunc("/tip", func(w http.ResponseWriter, r *http.Request) {
        // select random tip
        t := tips[rand.Intn(len(tips))]
        resp := tipResponse{Tip: t}
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(resp)

        // log concurrently
        go func() {
            mu.Lock()
            defer mu.Unlock()
            log.Printf("Served tip to %s: %s", r.RemoteAddr, t)
        }()
    })

    http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("OK"))
    })

    srv := &http.Server{
        Addr:               ":8080",
        ReadHeaderTimeout: 5 * time.Second,
        WriteTimeout:      10 * time.Second,
        IdleTimeout:       120 * time.Second,
    }

    log.Println("Wasteland Tips Server listening on :8080")
    if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
        log.Fatalf("Server error: %v", err)
    }
}
