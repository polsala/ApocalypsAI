package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
)

var emojis = []string{"ð", "ð±", "ð", "ð", "ð", "ð"}

func main() {
    var reader io.Reader
    if len(os.Args) > 1 {
        f, err := os.Open(os.Args[1])
        if err != nil {
            fmt.Fprintln(os.Stderr, "Error opening file:", err)
            os.Exit(1)
        }
        defer f.Close()
        reader = f
    } else {
        reader = os.Stdin
    }
    scanner := bufio.NewScanner(reader)
    lineIndex := 0
    for scanner.Scan() {
        line := scanner.Text()
        emoji := emojis[lineIndex%len(emojis)]
        fmt.Println(emoji, line)
        lineIndex++
    }
    if err := scanner.Err(); err != nil {
        fmt.Fprintln(os.Stderr, "Error reading:", err)
        os.Exit(1)
    }
}

