package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)

// Message represents a time-delayed communication.
type Message struct {
	ID           string    `json:"id"`
	Recipient    string    `json:"recipient"`
	Content      string    `json:"content"`
	DeliveryTime time.Time `json:"delivery_time"`
	SentTime     time.Time `json:"sent_time"`
}

// Courier manages the scheduling and delivery of messages.
type Courier struct {
	mu              sync.Mutex
	pendingMessages map[string][]Message // recipient -> []Message
	deliveredMessages map[string][]Message // recipient -> []Message
	messageCounter  int
}

// NewCourier creates and initializes a new Courier instance.
func NewCourier() *Courier {
	return &Courier{
		pendingMessages: make(map[string][]Message),
		deliveredMessages: make(map[string][]Message),
		messageCounter:  0,
	}
}

// ScheduleMessage adds a message to the pending queue with a specified delay.
func (c *Courier) ScheduleMessage(recipient, content string, delaySeconds int) (Message, error) {
	c.mu.Lock()
	defer c.mu.Unlock()

	c.messageCounter++
	id := fmt.Sprintf("msg-%d", c.messageCounter)
	sentTime := time.Now().UTC()
	deliveryTime := sentTime.Add(time.Duration(delaySeconds) * time.Second)

	msg := Message{
		ID:           id,
		Recipient:    recipient,
		Content:      content,
		DeliveryTime: deliveryTime,
		SentTime:     sentTime,
	}

	c.pendingMessages[recipient] = append(c.pendingMessages[recipient], msg)
	return msg, nil
}

// GetDeliveredMessages retrieves all messages that have been delivered for a given recipient.
func (c *Courier) GetDeliveredMessages(recipient string) []Message {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.deliveredMessages[recipient]
}

// processPendingMessages checks for messages whose delivery time has passed and moves them.
func (c *Courier) processPendingMessages() {
	c.mu.Lock()
	defer c.mu.Unlock()

	now := time.Now().UTC()
	for recipient, messages := range c.pendingMessages {
		var stillPending []Message
		for _, msg := range messages {
			if msg.DeliveryTime.Before(now) || msg.DeliveryTime.Equal(now) {
				c.deliveredMessages[recipient] = append(c.deliveredMessages[recipient], msg)
			} else {
				stillPending = append(stillPending, msg)
			}
		}
		c.pendingMessages[recipient] = stillPending
	}
}

// StartDeliveryLoop starts a goroutine that periodically processes pending messages.
func (c *Courier) StartDeliveryLoop(interval time.Duration) {
	ticker := time.NewTicker(interval)
	go func() {
		for range ticker.C {
			c.processPendingMessages()
		}
	}()
}

// sendHandler handles POST requests to schedule a message.
// Expects JSON: {"recipient": "user1", "content": "hello future", "delay_seconds": 60}
func sendHandler(courier *Courier) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
			return
		}

		var req struct {
			Recipient    string `json:"recipient"`
			Content      string `json:"content"`
			DelaySeconds int    `json:"delay_seconds"`
		}

		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid request body", http.StatusBadRequest)
			return
		}
		if req.Recipient == "" || req.Content == "" || req.DelaySeconds < 0 {
			http.Error(w, "Recipient, content, and non-negative delay_seconds are required", http.StatusBadRequest)
			return
		}

		msg, err := courier.ScheduleMessage(req.Recipient, req.Content, req.DelaySeconds)
		if err != nil {
			http.Error(w, "Failed to schedule message", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusAccepted)
		json.NewEncoder(w).Encode(msg)
	}
}

// receiveHandler handles GET requests to retrieve delivered messages for a recipient.
// Expects query param: ?recipient=user1
func receiveHandler(courier *Courier) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "Only GET method is allowed", http.StatusMethodNotAllowed)
			return
		}

		recipient := r.URL.Query().Get("recipient")
		if recipient == "" {
			http.Error(w, "Recipient query parameter is required", http.StatusBadRequest)
			return
		}

		messages := courier.GetDeliveredMessages(recipient)
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(messages)
	}
}

func main() {
	courier := NewCourier()
	courier.StartDeliveryLoop(1 * time.Second) // Check for deliveries every second

	http.HandleFunc("/send", sendHandler(courier))
	http.HandleFunc("/receive", receiveHandler(courier))

	port := 8080
	log.Printf("Chrono-Courier service starting on :%d", port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", port), nil))
}
