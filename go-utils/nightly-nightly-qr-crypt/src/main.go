package main

import (
    "crypto/sha256"
    "fmt"
    "os"
)

// generateQR returns an 8×8 ASCII representation of the first 64 bits of the
// SHA‑256 hash of the supplied input. A bit value of 1 is rendered as "#",
// while 0 is rendered as a space.
func generateQR(input string) string {
    hash := sha256.Sum256([]byte(input))
    var grid string
    for i := 0; i < 8; i++ {
        b := hash[i]
        for bit := 7; bit >= 0; bit-- {
            if (b>>bit)&1 == 1 {
                grid += "#"
            } else {
                grid += " "
            }
        }
        if i < 7 {
            grid += "\n"
        }
    }
    return grid
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: qrcrypt <text>")
        os.Exit(1)
    }
    input := os.Args[1]
    fmt.Println(generateQR(input))
}
