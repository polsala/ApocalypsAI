package main

import (
    "flag"
    "fmt"
    "os"
    "time"
)

func main() {
    dir := flag.String("dir", "", "Directory to watch")
    flag.Parse()

    if *dir == "" {
        fmt.Println("Please provide a directory to watch using -dir flag.")
        os.Exit(1)
    }

    fmt.Printf("Watching directory: %s\\n", *dir)
    WatchDir(*dir, func(name string) {
        fmt.Printf("👻 A new ghost has appeared: %s\\n", name)
    })
}

func WatchDir(dir string, onNewFile func(string)) {
    seen := make(map[string]struct{})
    ticker := time.NewTicker(500 * time.Millisecond)
    defer ticker.Stop()

    for {
        select {
        case <-ticker.C:
            entries, err := os.ReadDir(dir)
            if err != nil {
                fmt.Fprintf(os.Stderr, "Error reading directory: %v\\n", err)
                continue
            }
            for _, entry := range entries {
                if entry.IsDir() {
                    continue
                }
                name := entry.Name()
                if _, ok := seen[name]; !ok {
                    seen[name] = struct{}{}
                    onNewFile(name)
                }
            }
        }
    }
}
