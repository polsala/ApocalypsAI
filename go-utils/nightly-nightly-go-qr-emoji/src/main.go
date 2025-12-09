package main

import (
    "fmt"
    "os"
    "strings"

    qrcode "github.com/skip2/go-qrcode"
)

// renderEmojiMatrix converts a QR code bitmap ([][]bool) into a string where
// true  => black square emoji (⬛️)
// false => white square emoji (⬜️)
func renderEmojiMatrix(bitmap [][]bool) string {
    var sb strings.Builder
    for y, row := range bitmap {
        for _, cell := range row {
            if cell {
                sb.WriteString("⬛️")
            } else {
                sb.WriteString("⬜️")
            }
        }
        if y < len(bitmap)-1 {
            sb.WriteRune('\n')
        }
    }
    return sb.String()
}

func generateQRCode(input string) (string, error) {
    // Use Medium error correction – a good balance for short strings.
    qr, err := qrcode.New(input, qrcode.Medium)
    if err != nil {
        return "", err
    }
    bitmap := qr.Bitmap()
    return renderEmojiMatrix(bitmap), nil
}

func main() {
    if len(os.Args) != 2 {
        fmt.Fprintln(os.Stderr, "Usage: qr-emoji <string>")
        os.Exit(1)
    }
    input := os.Args[1]
    out, err := generateQRCode(input)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error generating QR code: %v\n", err)
        os.Exit(1)
    }
    fmt.Println(out)
}
