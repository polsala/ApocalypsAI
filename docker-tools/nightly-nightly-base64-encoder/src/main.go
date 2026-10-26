package main

import (
    "encoding/base64"
    "fmt"
    "io"
    "os"
)

// Encode returns the Base64 representation of the input bytes.
func Encode(input []byte) string {
    return base64.StdEncoding.EncodeToString(input)
}

func main() {
    data, err := io.ReadAll(os.Stdin)
    if err != nil {
        fmt.Fprintln(os.Stderr, "error reading stdin:", err)
        os.Exit(1)
    }
    fmt.Print(Encode(data))
}
