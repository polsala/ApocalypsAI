package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
    "strings"
)

func indexOf(slice []string, val string) int {
    for i, v := range slice {
        if v == val {
            return i
        }
    }
    return -1
}

func lintDockerfile(r io.Reader) []string {
    scanner := bufio.NewScanner(r)
    var lines []string
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }
    var issues []string
    hasFrom := false
    hasCmdOrEntrypoint := false
    hasAdd := false
    for _, line := range lines {
        trimmed := strings.TrimSpace(line)
        if trimmed == "" || strings.HasPrefix(trimmed, "#") {
            continue
        }
        upper := strings.ToUpper(trimmed)
        if strings.HasPrefix(upper, "FROM") {
            hasFrom = true
        }
        if strings.HasPrefix(upper, "CMD") || strings.HasPrefix(upper, "ENTRYPOINT") {
            hasCmdOrEntrypoint = true
        }
        if strings.HasPrefix(upper, "ADD") {
            hasAdd = true
        }
        if strings.HasPrefix(upper, "RUN") && strings.Contains(strings.ToLower(trimmed), "apt-get update") {
            if !strings.Contains(strings.ToLower(trimmed), "apt-get install -y") {
                idx := indexOf(lines, line)
                if idx+1 < len(lines) {
                    next := strings.ToLower(strings.TrimSpace(lines[idx+1]))
                    if !strings.Contains(next, "apt-get install -y") {
                        issues = append(issues, "RUN apt-get update without apt-get install -y")
                    }
                } else {
                    issues = append(issues, "RUN apt-get update without apt-get install -y")
                }
            }
        }
    }
    if !hasFrom {
        issues = append(issues, "Missing FROM instruction")
    }
    if !hasCmdOrEntrypoint {
        issues = append(issues, "Missing CMD or ENTRYPOINT instruction")
    }
    if hasAdd {
        issues = append(issues, "ADD instruction found; use COPY instead")
    }
    return issues
}

func main() {
    var reader io.Reader
    if len(os.Args) > 1 {
        file, err := os.Open(os.Args[1])
        if err != nil {
            fmt.Fprintf(os.Stderr, "Error opening file: %v\\n", err)
            os.Exit(1)
        }
        defer file.Close()
        reader = file
    } else {
        reader = os.Stdin
    }
    issues := lintDockerfile(reader)
    if len(issues) == 0 {
        fmt.Println("OK")
    } else {
        for _, issue := range issues {
            fmt.Println(issue)
        }
        os.Exit(1)
    }
}
