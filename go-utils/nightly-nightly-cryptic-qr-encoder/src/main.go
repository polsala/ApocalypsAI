package main

import (
    "fmt"
    "io/ioutil"
    "os"
)

func main() {
    if len(os.Args) != 3 {
        fmt.Fprintf(os.Stderr, "Usage: %s <text> <output.png>\n", os.Args[0])
        os.Exit(1)
    }
    text := os.Args[1]
    outPath := os.Args[2]

    // In a real implementation, generate a QR code from `text`.
    // Here we write a minimal PNG header as a placeholder.
    pngHeader := []byte{0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A}
    // Append the raw text so the file is not empty – still a valid PNG header.
    data := append(pngHeader, []byte(text)...)

    err := ioutil.WriteFile(outPath, data, 0644)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Failed to write file: %v\n", err)
        os.Exit(1)
    }
    fmt.Printf("Placeholder QR PNG written to %s\n", outPath)
}
