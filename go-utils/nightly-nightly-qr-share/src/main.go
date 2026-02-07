package main

import (
    "flag"
    "fmt"
    "log"
    "net/http"
    "time"

    "github.com/skip2/go-qrcode"
)

// generateQRCode creates a 256x256 PNG QR code for the given text.
func generateQRCode(text string) ([]byte, error) {
    return qrcode.Encode(text, qrcode.Medium, 256)
}

func main() {
    text := flag.String("text", "", "Text to encode into QR code")
    port := flag.Int("port", 8080, "Port for HTTP server")
    ttl := flag.Int("ttl", 300, "Time‑to‑live in seconds")
    flag.Parse()

    if *text == "" {
        log.Fatal("text flag is required")
    }

    png, err := generateQRCode(*text)
    if err != nil {
        log.Fatalf("failed to generate QR code: %v", err)
    }

    handler := func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", "image/png")
        w.Write(png)
    }

    http.HandleFunc("/qr.png", handler)

    srv := &http.Server{Addr: fmt.Sprintf(":%d", *port)}

    go func() {
        log.Printf("Serving QR code at http://localhost:%d/qr.png for %d seconds", *port, *ttl)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("server error: %v", err)
        }
    }()

    // Shutdown after ttl seconds
    time.AfterFunc(time.Duration(*ttl)*time.Second, func() {
        log.Println("TTL expired, shutting down server")
        srv.Close()
    })

    // Block until server is closed
    select {}
}
