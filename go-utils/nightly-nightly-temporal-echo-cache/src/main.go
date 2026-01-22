package main

import (
	"fmt"
	"sync"
	"time"
)

// CacheEntry represents an item in the cache with its expiration time.
type CacheEntry struct {
	Value      string
	Expiration int64 // Unix timestamp in seconds
}

// EchoCache is a concurrent, in-memory key-value store with TTL and expiration echoes.
type EchoCache struct {
	mu        sync.RWMutex
	data      map[string]CacheEntry
	stopChan  chan struct{}
	echoLog   chan string // Channel to send expiration echoes
	cleanInterval time.Duration
}

// NewEchoCache creates and initializes a new EchoCache.
// cleanInterval specifies how often the cache cleaner goroutine runs.
func NewEchoCache(cleanInterval time.Duration) *EchoCache {
	cache := &EchoCache{
		data:      make(map[string]CacheEntry),
		stopChan:  make(chan struct{}),
		echoLog:   make(chan string, 100), // Buffered channel for echoes
		cleanInterval: cleanInterval,
	}
	go cache.cleaner() // Start the background cleaner goroutine
	return cache
}

// Set adds or updates a key-value pair with a given TTL (in seconds).
func (c *EchoCache) Set(key string, value string, ttlSeconds int) {
	c.mu.Lock()
	defer c.mu.Unlock()

	expiration := time.Now().Add(time.Duration(ttlSeconds) * time.Second).Unix()
	c.data[key] = CacheEntry{Value: value, Expiration: expiration}
	fmt.Printf("Cache: Set key '%s' with value '%s', expires in %d seconds.\n", key, value, ttlSeconds)
}

// Get retrieves the value associated with a key. Returns the value and true if found and not expired,
// otherwise returns an empty string and false.
func (c *EchoCache) Get(key string) (string, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	entry, found := c.data[key]
	if !found {
		return "", false
	}

	if entry.Expiration > 0 && time.Now().Unix() > entry.Expiration {
		// Already expired, but cleaner hasn't run yet. Treat as not found.
		// The cleaner will eventually remove it.
		return "", false
	}

	return entry.Value, true
}

// Delete removes a key-value pair from the cache.
func (c *EchoCache) Delete(key string) {
	c.mu.Lock()
	defer c.mu.Unlock()

	if _, found := c.data[key]; found {
		delete(c.data, key)
		fmt.Printf("Cache: Deleted key '%s'.\n", key)
	}
}

// cleaner is a background goroutine that periodically removes expired entries.
func (c *EchoCache) cleaner() {
	ticker := time.NewTicker(c.cleanInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			c.mu.Lock()
			now := time.Now().Unix()
			for key, entry := range c.data {
				if entry.Expiration > 0 && now > entry.Expiration {
					c.echoLog <- fmt.Sprintf("Temporal Echo: Key '%s' with value '%s' expired.", key, entry.Value)
					delete(c.data, key)
				}
			}
			c.mu.Unlock()
		case <-c.stopChan:
			fmt.Println("Cache cleaner stopped.")
			return
		}
	}
}

// StopCleaner stops the background cleaner goroutine.
func (c *EchoCache) StopCleaner() {
	close(c.stopChan)
	// Drain the echoLog channel to prevent goroutine leak if not read
	for len(c.echoLog) > 0 {
		<-c.echoLog
	}
	close(c.echoLog)
}

// GetEchoes retrieves all accumulated expiration echoes.
// This is primarily for testing or a simple logging mechanism.
func (c *EchoCache) GetEchoes() []string {
	var echoes []string
	// Non-blocking read from echoLog channel
	for {
		select {
		case echo := <-c.echoLog:
			echoes = append(echoes, echo)
		default:
			return echoes
		}
	}
}

func main() {
	// Example usage (not part of the utility itself, but for demonstration)
	cache := NewEchoCache(1 * time.Second)
	defer cache.StopCleaner()

	cache.Set("message", "Hello from the past!", 3) // Expires in 3 seconds
	cache.Set("secret", "42", 5) // Expires in 5 seconds

	val, ok := cache.Get("message")
	if ok {
		fmt.Printf("Retrieved 'message': %s\n", val)
	} else {
		fmt.Println("'message' not found or expired.")
	}

	time.Sleep(4 * time.Second) // Wait for 'message' to expire

	val, ok = cache.Get("message")
	if ok {
		fmt.Printf("Retrieved 'message': %s\n", val)
	} else {
		fmt.Println("'message' not found or expired.")
	}

	echoes := cache.GetEchoes()
	for _, echo := range echoes {
		fmt.Println(echo)
	}

	time.Sleep(2 * time.Second) // Wait for 'secret' to expire

	echoes = cache.GetEchoes()
	for _, echo := range echoes {
		fmt.Println(echo)
	}
}
