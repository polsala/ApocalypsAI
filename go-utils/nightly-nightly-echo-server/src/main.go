package main

import (
    "encoding/json"
    "io/ioutil"
    "log"
    "net/http"
    "os"
)

type EchoResponse struct {
    Method  string            `json:"method"`
    URL     string            `json:"url"`
    Headers map[string]string `json:"headers"`
    Body    string            `json:"body"`
}

func echoHandler(w http.ResponseWriter, r *http.Request) {
    bodyBytes, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "failed to read body", http.StatusInternalServerError)
        return
    }
    defer r.Body.Close()

    headers := make(map[string]string)
    for k, v := range r.Header {
        headers[k] = v[0]
    }

    resp := EchoResponse{
        Method:  r.Method,
        URL:     r.URL.Path,
        Headers: headers,
        Body:    string(bodyBytes),
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(resp)
}

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }
    http.HandleFunc("/", echoHandler)
    log.Printf("Starting echo server on :%s\n", port)
    if err := http.ListenAndServe(":"+port, nil); err != nil {
        log.Fatalf("Server failed: %v", err)
    }
}
