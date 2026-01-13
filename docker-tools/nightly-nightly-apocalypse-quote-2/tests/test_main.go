package main

import (
	\"encoding/json\"
	\"net/http\"
	\"net/http/httptest\"
	\"testing\"
)

func TestQuoteHandler(t *testing.T) {
	// Create a test server using the handler
	ts := httptest.NewServer(http.HandlerFunc(quoteHandler))
	defer ts.Close()

	resp, err := http.Get(ts.URL + \"/quote\")
	if err != nil {
		t.Fatalf(\"Failed to GET /quote: %v\", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		t.Fatalf(\"Expected status 200, got %d\", resp.StatusCode)
	}

	var body map[string]string
	if err := json.NewDecoder(resp.Body).Decode(&body); err != nil {
		t.Fatalf(\"Failed to decode JSON: %v\", err)
	}

	quote, ok := body[\"quote\"]
	if !ok {
		t.Fatalf(\"Response JSON missing 'quote' field\")
	}

	// Verify that the quote is one of the predefined quotes
	found := false
	for _, q := range quotes {
		if q == quote {
			found = true
			break
		}
	}
	if !found {
		t.Fatalf(\"Quote not in predefined list: %s\", quote)
	}
}
