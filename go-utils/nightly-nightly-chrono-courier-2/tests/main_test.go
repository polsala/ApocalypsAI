package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

// Mock rationale: We need to control time for deterministic tests of message delivery.
// Instead of mocking time.Now() directly (which is complex in Go), we will
// manually set the DeliveryTime for test messages and then directly call
// processPendingMessages, simulating the passage of time.
// For HTTP tests, httptest.NewServer is used to avoid actual network calls.

func TestCourier_ScheduleAndGetMessages(t *testing.T) {
	courier := NewCourier()

	// Test scheduling a message
	recipient := "testuser"
	content := "Hello from the past!"
	delay := 5 // seconds
	msg, err := courier.ScheduleMessage(recipient, content, delay)

	if err != nil {
		t.Fatalf("ScheduleMessage failed: %v", err)
	}
	if msg.Recipient != recipient {
		t.Errorf("Expected recipient %s, got %s", recipient, msg.Recipient)
	}
	if msg.Content != content {
		t.Errorf("Expected content %s, got %s", content, msg.Content)
	}
	if msg.DeliveryTime.IsZero() {
		t.Error("DeliveryTime should not be zero")
	}

	// Message should be pending, not delivered yet
	delivered := courier.GetDeliveredMessages(recipient)
	if len(delivered) != 0 {
		t.Errorf("Expected 0 delivered messages, got %d", len(delivered))
	}

	// Manually process pending messages (simulating time passing)
	// Set the current time to be after the message's delivery time
	// Mock rationale: Simulating time passage by directly manipulating the internal state
	// and calling the processing function, rather than waiting for real time.
	now := time.Now().UTC().Add(time.Duration(delay+1) * time.Second)
	for r, msgs := range courier.pendingMessages {
		for i := range msgs {
			msgs[i].DeliveryTime = now.Add(-1 * time.Second) // Ensure it's in the past
		}
		courier.pendingMessages[r] = msgs
	}

	courier.processPendingMessages()

	// Message should now be delivered
	delivered = courier.GetDeliveredMessages(recipient)
	if len(delivered) != 1 {
		t.Fatalf("Expected 1 delivered message, got %d", len(delivered))
	}
	if delivered[0].ID != msg.ID {
		t.Errorf("Delivered message ID mismatch. Expected %s, got %s", msg.ID, delivered[0].ID)
	}
}

func TestCourier_ProcessPendingMessages(t *testing.T) {
	courier := NewCourier()
	recipient := "testuser2"

	// Schedule a message for 10 seconds in the future
	msg1, _ := courier.ScheduleMessage(recipient, "Future message 1", 10)
	// Schedule a message for 1 second in the future
	msg2, _ := courier.ScheduleMessage(recipient, "Future message 2", 1)

	// Initially, no messages should be delivered
	if len(courier.GetDeliveredMessages(recipient)) != 0 {
		t.Error("Expected no delivered messages initially")
	}
	if len(courier.pendingMessages[recipient]) != 2 {
		t.Errorf("Expected 2 pending messages, got %d", len(courier.pendingMessages[recipient]))
	}

	// Mock rationale: Manually setting delivery times to simulate time passing
	// without actually waiting. This makes the test deterministic and fast.
	// Simulate 2 seconds passing, so msg2 should be delivered.
	now := time.Now().UTC()
	for i := range courier.pendingMessages[recipient] {
		if courier.pendingMessages[recipient][i].ID == msg2.ID {
			courier.pendingMessages[recipient][i].DeliveryTime = now.Add(-1 * time.Second) // Make msg2 deliverable
		}
	}

	courier.processPendingMessages()

	// msg2 should be delivered, msg1 still pending
	delivered := courier.GetDeliveredMessages(recipient)
	if len(delivered) != 1 {
		t.Fatalf("Expected 1 delivered message after first process, got %d", len(delivered))
	}
	if delivered[0].ID != msg2.ID {
		t.Errorf("Expected msg2 to be delivered, got %s", delivered[0].ID)
	}
	if len(courier.pendingMessages[recipient]) != 1 {
		t.Errorf("Expected 1 pending message, got %d", len(courier.pendingMessages[recipient]))
	}
	if courier.pendingMessages[recipient][0].ID != msg1.ID {
		t.Errorf("Expected msg1 to still be pending, got %s", courier.pendingMessages[recipient][0].ID)
	}

	// Mock rationale: Simulate more time passing, so msg1 should now be delivered.
	for i := range courier.pendingMessages[recipient] {
		if courier.pendingMessages[recipient][i].ID == msg1.ID {
			courier.pendingMessages[recipient][i].DeliveryTime = now.Add(5 * time.Second) // Make msg1 deliverable
		}
	}
	courier.processPendingMessages()

	// Both messages should be delivered
	delivered = courier.GetDeliveredMessages(recipient)
	if len(delivered) != 2 {
		t.Fatalf("Expected 2 delivered messages after second process, got %d", len(delivered))
	}
	if len(courier.pendingMessages[recipient]) != 0 {
		t.Errorf("Expected 0 pending messages, got %d", len(courier.pendingMessages[recipient]))
	}
}

func TestSendHandler(t *testing.T) {
	courier := NewCourier()
	handler := sendHandler(courier)

	// Test valid request
	reqBody := []byte(`{"recipient": "userA", "content": "Test message A", "delay_seconds": 1}`)
	req := httptest.NewRequest(http.MethodPost, "/send", bytes.NewBuffer(reqBody))
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusAccepted {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusAccepted)
	}

	var responseMsg Message
	err := json.NewDecoder(rr.Body).Decode(&responseMsg)
	if err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}
	if responseMsg.Recipient != "userA" {
		t.Errorf("Expected recipient userA, got %s", responseMsg.Recipient)
	}
	if len(courier.pendingMessages["userA"]) != 1 {
		t.Errorf("Expected 1 pending message for userA, got %d", len(courier.pendingMessages["userA"]))
	}

	// Test invalid method
	req = httptest.NewRequest(http.MethodGet, "/send", nil)
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for invalid method: got %v want %v", status, http.StatusMethodNotAllowed)
	}

	// Test invalid JSON
	reqBody = []byte(`{"recipient": "userB", "content": "Test message B", "delay_seconds": "invalid"}`)
	req = httptest.NewRequest(http.MethodPost, "/send", bytes.NewBuffer(reqBody))
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for invalid JSON: got %v want %v", status, http.StatusBadRequest)
	}

	// Test missing fields
	reqBody = []byte(`{"recipient": "userC", "delay_seconds": 1}`) // Missing content
	req = httptest.NewRequest(http.MethodPost, "/send", bytes.NewBuffer(reqBody))
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing content: got %v want %v", status, http.StatusBadRequest)
	}
}

func TestReceiveHandler(t *testing.T) {
	courier := NewCourier()
	handler := receiveHandler(courier)

	recipient := "userX"
	content1 := "Delivered message 1"
	content2 := "Delivered message 2"

	// Mock rationale: Manually adding messages to deliveredMessages to simulate
	// prior delivery for testing the receive handler.
	courier.mu.Lock()
	courier.deliveredMessages[recipient] = []Message{
		{ID: "dmsg1", Recipient: recipient, Content: content1, DeliveryTime: time.Now().UTC().Add(-5 * time.Minute)},
		{ID: "dmsg2", Recipient: recipient, Content: content2, DeliveryTime: time.Now().UTC().Add(-1 * time.Minute)},
	}
	courier.mu.Unlock()

	// Test valid request
	req := httptest.NewRequest(http.MethodGet, fmt.Sprintf("/receive?recipient=%s", recipient), nil)
	rr := httptest.NewRecorder()
	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
	}

	var messages []Message
	err := json.NewDecoder(rr.Body).Decode(&messages)
	if err != nil {
		t.Fatalf("Failed to decode response: %v", err)
	}
	if len(messages) != 2 {
		t.Fatalf("Expected 2 delivered messages, got %d", len(messages))
	}
	if messages[0].Content != content1 && messages[1].Content != content1 { // Order might not be guaranteed
		t.Errorf("Expected content %s not found", content1)
	}

	// Test recipient with no messages
	req = httptest.NewRequest(http.MethodGet, "/receive?recipient=nonexistent", nil)
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusOK { // Should return 200 with empty array
		t.Errorf("handler returned wrong status code for nonexistent recipient: got %v want %v", status, http.StatusOK)
	}
	var emptyMessages []Message
	json.NewDecoder(rr.Body).Decode(&emptyMessages)
	if len(emptyMessages) != 0 {
		t.Errorf("Expected 0 messages for nonexistent recipient, got %d", len(emptyMessages))
	}

	// Test missing recipient query parameter
	req = httptest.NewRequest(http.MethodGet, "/receive", nil)
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusBadRequest {
		t.Errorf("handler returned wrong status code for missing recipient param: got %v want %v", status, http.StatusBadRequest)
	}

	// Test invalid method
	req = httptest.NewRequest(http.MethodPost, "/receive?recipient=userX", nil)
	rr = httptest.NewRecorder()
	handler.ServeHTTP(rr, req)
	if status := rr.Code; status != http.StatusMethodNotAllowed {
		t.Errorf("handler returned wrong status code for invalid method: got %v want %v", status, http.StatusMethodNotAllowed)
	}
}
