package main

import (
    "bufio"
    "fmt"
    "os"
    "strconv"
    "strings"
    "sync"
)

// decodeCaesar shifts each letter by shift positions backward.
// Non‑alphabetic characters are left unchanged.
func decodeCaesar(cipher string, shift int) string {
    shift = shift % 26
    var sb strings.Builder
    for _, r := range cipher {
        switch {
        case r >= 'A' && r <= 'Z':
            sb.WriteRune('A' + (r-'A'+26-int32(shift))%26)
        case r >= 'a' && r <= 'z':
            sb.WriteRune('a' + (r-'a'+26-int32(shift))%26)
        default:
            sb.WriteRune(r)
        }
    }
    return sb.String()
}

// parseLine expects format "SHIFT:<n>:<ciphertext>".
// Returns shift, ciphertext, or an error.
func parseLine(line string) (int, string, error) {
    parts := strings.SplitN(line, ":", 3)
    if len(parts) != 3 || strings.TrimSpace(parts[0]) != "SHIFT" {
        return 0, "", fmt.Errorf("invalid format")
    }
    shift, err := strconv.Atoi(strings.TrimSpace(parts[1]))
    if err != nil {
        return 0, "", fmt.Errorf("invalid shift")
    }
    return shift, parts[2], nil
}

func main() {
    scanner := bufio.NewScanner(os.Stdin)
    var wg sync.WaitGroup
    out := make(chan string)

    // Collector goroutine to print results as they become available.
    go func() {
        for decoded := range out {
            fmt.Println(decoded)
        }
    }()

    for scanner.Scan() {
        line := scanner.Text()
        wg.Add(1)
        go func(l string) {
            defer wg.Done()
            shift, cipher, err := parseLine(l)
            if err != nil {
                out <- fmt.Sprintf("error: %v", err)
                return
            }
            decoded := decodeCaesar(cipher, shift)
            out <- decoded
        }(line)
    }

    wg.Wait()
    close(out)
}
