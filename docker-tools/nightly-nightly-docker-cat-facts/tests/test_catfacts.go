package catfacts_test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/polsala/nightly-docker-cat-facts/src/catfacts"
)

func TestFetchCatFact(t *testing.T) {
	// Mock server
	headler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(`\\{"fact":"Cats have 32 muscles in each ear."\\}`))
	})
	server := httptest.NewServer(handler)
	defer server.Close()

	fact, err := catfacts.FetchCatFact(server.URL)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	expected := "Cats have 32 muscles in each ear."
	if fact != expected {
		t.Fatalf("expected %q, got %q", expected, fact)
	}
}
