package main

import (
    "fmt"
    "strings"
)

func generateSwatch() string {
    var sb strings.Builder
    for i := 0; i < 256; i++ {
        // Print color block with code
        sb.WriteString(fmt.Sprintf("\x1b[48;5;%dm %3d \x1b[0m", i, i))
        // Newline every 8 colors for readability
        if (i+1)%8 == 0 {
            sb.WriteString("\n")
        } else {
            sb.WriteString(" ")
        }
    }
    return sb.String()
}

func main() {
    fmt.Print(generateSwatch())
}
