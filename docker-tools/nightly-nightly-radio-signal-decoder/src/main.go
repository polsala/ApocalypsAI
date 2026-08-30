package main

import (
    "encoding/base64"
    "fmt"
    "os"
)

func main() {
    signal := os.Getenv("SIGNAL")
    if signal == "" {
        fmt.Println("⚠️ No SIGNAL env var provided")
        os.Exit(1)
    }
    decoded, err := base64.StdEncoding.DecodeString(signal)
    if err != nil {
        fmt.Printf("❌ Invalid base64: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("🔊 Decoded signal: %s\n", string(decoded))
}
