package main

import (
    "encoding/json"
    "log"
    "net/http"
    "github.com/skip2/go-qrcode"
)

type request struct {
    Message string `json:"message"`
}

func qrHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "only POST allowed", http.StatusMethodNotAllowed)
        return
    }
    var req request
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid json", http.StatusBadRequest)
        return
    }
    if req.Message == "" {
        http.Error(w, "message required", http.StatusBadRequest)
        return
    }
    png, err := qrcode.Encode(req.Message, qrcode.Medium, 256)
    if err != nil {
        http.Error(w, "failed to generate QR", http.StatusInternalServerError)
        return
    }
    w.Header().Set("Content-Type", "image/png")
    w.Write(png)
}

func main() {
    http.HandleFunc("/qr", qrHandler)
    log.Println("Starting QR Broadcast service on :8080")
    if err := http.ListenAndServe(":8080", nil); err != nil {
        log.Fatalf("server error: %v", err)
    }
}
