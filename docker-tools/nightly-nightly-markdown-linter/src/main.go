package main

import (
    "bufio"
    "errors"
    "flag"
    "fmt"
    "io"
    "net/http"
    "os"
    "regexp"
    "strings"
    "time"
)

// LintError represents a single linting issue.
type LintError struct {
    Line    int
    Message string
}

// LintResult aggregates all lint errors.
type LintResult struct {
    Errors []LintError
}

func main() {
    flag.Usage = func() {
        fmt.Fprintf(flag.CommandLine.Output(), "Usage: %s <markdown-file>\n", os.Args[0])
    }
    flag.Parse()
    if flag.NArg() != 1 {
        flag.Usage()
        os.Exit(1)
    }
    filePath := flag.Arg(0)
    content, err := os.ReadFile(filePath)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
        os.Exit(1)
    }
    result := lintMarkdown(string(content))
    if len(result.Errors) == 0 {
        fmt.Println("No issues found.")
        os.Exit(0)
    }
    fmt.Println("Linting issues:")
    for _, e := range result.Errors {
        fmt.Printf("Line %d: %s\n", e.Line, e.Message)
    }
    os.Exit(1)
}

func lintMarkdown(content string) LintResult {
    var result LintResult
    scanner := bufio.NewScanner(strings.NewReader(content))
    lineNum := 0
    var prevHeadingLevel int
    for scanner.Scan() {
        lineNum++
        line := scanner.Text()
        // Heading check
        if strings.HasPrefix(line, "#") {
            level := strings.Count(line, "#")
            if level > 1 && level-prevHeadingLevel > 1 {
                result.Errors = append(result.Errors, LintError{Line: lineNum, Message: fmt.Sprintf("Heading level jumps from %d to %d", prevHeadingLevel, level)})
            }
            prevHeadingLevel = level
        }
        // Image alt text check
        imageRe := regexp.MustCompile(`!\[([^\]]*)\]\(([^\)]+)\)`)
        for _, match := range imageRe.FindAllStringSubmatch(line, -1) {
            alt := strings.TrimSpace(match[1])
            if alt == "" {
                result.Errors = append(result.Errors, LintError{Line: lineNum, Message: "Image missing alt text"})
            }
        }
        // Link check
        linkRe := regexp.MustCompile(`\[([^\]]+)\]\(([^\)]+)\)`)
        for _, match := range linkRe.FindAllStringSubmatch(line, -1) {
            url := strings.TrimSpace(match[2])
            if err := checkLink(url); err != nil {
                result.Errors = append(result.Errors, LintError{Line: lineNum, Message: fmt.Sprintf("Broken link: %s (%v)", url, err)})
            }
        }
    }
    return result
}

func checkLink(url string) error {
    client := &http.Client{Timeout: 5 * time.Second}
    req, err := http.NewRequest("HEAD", url, nil)
    if err != nil {
        return err
    }
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    if resp.StatusCode < 200 || resp.StatusCode >= 400 {
        return errors.New("status " + resp.Status)
    }
    return nil
}
