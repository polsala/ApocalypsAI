package main

import (
    "bufio"
    "flag"
    "fmt"
    "math/rand"
    "os"
    "sync"
)

type Job struct {
    idx  int
    line string
}

type Result struct {
    idx  int
    line string
}

var staticChars = []rune{'~', '*', '#', '%'}

// addStatic inserts a number of static characters into the input string.
// The number of insertions is floor(len(s)/5). Positions and characters are
// chosen using the provided rand.Rand instance.
func addStatic(s string, rnd *rand.Rand) string {
    if len(s) == 0 {
        return s
    }
    count := len(s) / 5
    for i := 0; i < count; i++ {
        pos := rnd.Intn(len(s) + 1) // allow insertion at the end
        ch := staticChars[rnd.Intn(len(staticChars))]
        s = s[:pos] + string(ch) + s[pos:]
    }
    return s
}

// worker consumes jobs, processes them, and sends results.
func worker(id int, jobs <-chan Job, results chan<- Result, seed int64, wg *sync.WaitGroup) {
    defer wg.Done()
    rnd := rand.New(rand.NewSource(seed + int64(id)))
    for job := range jobs {
        processed := addStatic(job.line, rnd)
        results <- Result{idx: job.idx, line: processed}
    }
}

// processLines runs the worker pool and returns the processed lines in the
// original order.
func processLines(lines []string, workers int, seed int64) []string {
    jobs := make(chan Job, len(lines))
    results := make(chan Result, len(lines))
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go worker(i, jobs, results, seed, &wg)
    }
    for idx, line := range lines {
        jobs <- Job{idx: idx, line: line}
    }
    close(jobs)
    wg.Wait()
    close(results)

    out := make([]string, len(lines))
    for res := range results {
        out[res.idx] = res.line
    }
    return out
}

func main() {
    workers := flag.Int("workers", 4, "Number of concurrent workers")
    seed := flag.Int64("seed", 0, "Random seed (0 = nondeterministic)")
    flag.Parse()

    scanner := bufio.NewScanner(os.Stdin)
    var lines []string
    for scanner.Scan() {
        lines = append(lines, scanner.Text())
    }
    if err := scanner.Err(); err != nil {
        fmt.Fprintln(os.Stderr, "error reading stdin:", err)
        os.Exit(1)
    }

    out := processLines(lines, *workers, *seed)
    for _, line := range out {
        fmt.Println(line)
    }
}
