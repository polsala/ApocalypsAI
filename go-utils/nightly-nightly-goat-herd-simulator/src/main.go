package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

// Goat represents an individual goat in the herd

type Goat struct {
	Name string
	Age  int
}

// Herd manages a group of goats and their behaviors

type Herd struct {
	Goats   []*Goat
	Size    int
	Mutex   sync.RWMutex
	Events  chan string
	Done    chan struct{}
	Verbose bool
}

// NewHerd creates a new herd with initial goats
func NewHerd(size int, verbose bool) *Herd {
	return &Herd{
		Goats:   make([]*Goat, 0, size),
		Size:    size,
		Events:  make(chan string, 100),
		Done:    make(chan struct{}),
		Verbose: verbose,
	}
}

// addInitialGoats populates the herd with initial goats
func (h *Herd) addInitialGoats() {
	goatNames := []string{"Billy", "Daisy", "Rocky", "Luna", "Butter", "Misty", "Clover", "Penny", "Bella", "Honey"}
	for i := 0; i < h.Size; i++ {
		name := goatNames[i%len(goatNames)] + strconv.Itoa(i/len(goatNames)+1)
		goat := &Goat{Name: name, Age: rand.Intn(5) + 1}
		h.Goats = append(h.Goats, goat)
	}
}

// simulateGrazing simulates a goat grazing
func (h *Herd) simulateGrazing(goat *Goat) {
	for {
		select {
		case <-h.Done:
			return
		default:
			if h.Verbose {
				sendEvent(h, fmt.Sprintf("%s is grazing...", goat.Name))
			}
			time.Sleep(time.Duration(rand.Intn(3)+1) * time.Second)
		}
	}
}

// simulateReproduction simulates a goat reproducing
func (h *Herd) simulateReproduction(goat *Goat) {
	for {
		select {
		case <-h.Done:
			return
		default:
			if rand.Float64() < 0.15 { // 15% chance per cycle
				newKid := &Goat{Name: goat.Name + "-Kid", Age: 0}
				h.Mutex.Lock()
				h.Goats = append(h.Goats, newKid)
				h.Mutex.Unlock()
				sendEvent(h, fmt.Sprintf("%s reproduced! A new kid joined the herd.", goat.Name))
			}
			time.Sleep(time.Duration(rand.Intn(5)+2) * time.Second)
		}
	}
}

// simulateMischief simulates a goat causing chaos
func (h *Herd) simulateMischief(goat *Goat) {
	for {
		select {
		case <-h.Done:
			return
		default:
			if rand.Float64() < 0.05 { // 5% chance per cycle
				sendEvent(h, fmt.Sprintf("%s caused a minor stampede!", goat.Name))
			}
			time.Sleep(time.Duration(rand.Intn(10)+3) * time.Second)
		}
	}
}

// sendEvent safely sends an event to the events channel
func sendEvent(h *Herd, msg string) {
	select {
	case h.Events <- msg:
	default:
		// Drop event if channel is full
	}
}

// printEvents continuously prints events from the channel
func (h *Herd) printEvents() {
	for {
		select {
	case event := <-h.Events:
			fmt.Printf("[GOAT] %s\n", event)
	case <-h.Done:
		return
	}
	}
}

// runSimulation starts all goat goroutines
func (h *Herd) runSimulation(duration time.Duration) {
	h.addInitialGoats()
	var wg sync.WaitGroup

	for _, goat := range h.Goats {
		wg.Add(3) // grazing, reproduction, mischief

		go func(g *Goat) {
			h.simulateGrazing(g)
			wg.Done()
		}(goat)

		go func(g *Goat) {
			h.simulateReproduction(g)
			wg.Done()
		}(goat)

		go func(g *Goat) {
			h.simulateMischief(g)
			wg.Done()
		}(goat)
	}

	go h.printEvents()

	time.Sleep(duration)
	close(h.Done)
	wg.Wait()
	close(h.Events)
}

// printFinalStatus displays final herd statistics
func (h *Herd) printFinalStatus() {
	h.Mutex.RLock()
	defer h.Mutex.RUnlock()
	fmt.Printf("[INFO] Simulation ended. Final herd size: %d goats.\n", len(h.Goats))
}

// parseFlags parses command line arguments
func parseFlags() (int, time.Duration, bool) {
	simDuration := 15 * time.Second
	herdSize := 10
	verbose := false

	args := os.Args[1:]
	for i := 0; i < len(args); i++ {
		switch args[i] {
		case "--herd-size":
			if i+1 < len(args) {
				s, err := strconv.Atoi(args[i+1])
				if err == nil && s > 0 {
					herdSize = s
				}
			}
		case "--duration":
			if i+1 < len(args) {
				dur, err := time.ParseDuration(args[i+1])
				if err == nil && dur > 0 {
					simDuration = dur
				}
			}
		case "--verbose":
			verbose = true
		}
	}

	return herdSize, simDuration, verbose
}

// main entry point
func main() {
	herdSize, duration, verbose := parseFlags()

	fmt.Printf("[INFO] Starting simulation with %d goats for %v\n", herdSize, duration)

	herd := NewHerd(herdSize, verbose)
	herd.runSimulation(duration)
	herd.printFinalStatus()
}
