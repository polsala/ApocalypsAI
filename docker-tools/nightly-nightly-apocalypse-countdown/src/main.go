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

type Response struct {
    Days    int    `json:"days"`
    Message string `json:"message"`
}

func getSeed() int64 {
    if s := os.Getenv("FIXED_SEED"); s != "" {
        if v, err := strconv.ParseInt(s, 10, 64); err == nil {
            return v
        }
    }
    return time.Now().UnixNano()
}

func handler(w http.ResponseWriter, r *http.Request) {
    rand.Seed(getSeed())
    days := rand.Intn(1001) // 0-1000 inclusive
    resp := Response{
        Days:    days,
        Message: "The world ends in " + strconv.Itoa(days) + " days!",
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    http.HandleFunc("/countdown", handler)
    log.Println("Starting server on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
