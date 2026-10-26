package main

import (
    "bufio"
    "flag"
    "fmt"
    "os"
    "strings"
    "sync"
)

// generateQR creates a deterministic ASCII‑art pattern based on the input text length.
// The pattern is a square of size ((len(text) % 4) + 3) with a star border.
func generateQR(text string) string {
    size := (len(text) % 4) + 3 // minimum size 3, max 6
    var sb strings.Builder
    // top border
    sb.WriteString("+")
    sb.WriteString(strings.Repeat("-", size))
    sb.WriteString("+\n")
    // middle rows
    for i := 0; i < size; i++ {
        sb.WriteString("|")
        for j := 0; j < size; j++ {
            if i == 0 || i == size-1 || j == 0 || j == size-1 {
                sb.WriteString("*")
            } else {
                sb.WriteString(" ")
            }
        }
        sb.WriteString("|\n")
    }
    // bottom border
    sb.WriteString("+")
    sb.WriteString(strings.Repeat("-", size))
    sb.WriteString("+")
    return sb.String()
}

func main() {
    // Optional file flag; if omitted, read from stdin.
    filePath := flag.String("file", "", "Path to a file containing one string per line")
    flag.Parse()

    var scanner *bufio.Scanner
    if *filePath != "" {
        f, err := os.Open(*filePath)
        if err != nil {
            fmt.Fprintf(os.Stderr, "error opening file: %v\n", err)
            os.Exit(1)
        }
        defer f.Close()
        scanner = bufio.NewScanner(f)
    } else {
        scanner = bufio.NewScanner(os.Stdin)
    }

    type result struct {
        output string
    }

    resultsCh := make(chan result)
    var wg sync.WaitGroup

    for scanner.Scan() {
        line := scanner.Text()
        wg.Add(1)
        go func(txt string) {
            defer wg.Done()
            qr := generateQR(txt)
            resultsCh <- result{output: qr}
        }(line)
    }

    // Close channel when all goroutines finish
    go func() {
        wg.Wait()
        close(resultsCh)
    }()

    // Print results as they arrive
    for res := range resultsCh {
        fmt.Println(res.output)
        fmt.Println() // separate entries
    }

    if err := scanner.Err(); err != nil {
        fmt.Fprintf(os.Stderr, "error reading input: %v\n", err)
        os.Exit(1)
    }
}
