package main

import (
    "encoding/json"
    "reflect"
    "testing"
)

func TestAllocateSimple(t *testing.T) {
    // Mock input: five items, two participants.
    inp := Input{
        Items: []Item{{"A", 5}, {"B", 4}, {"C", 3}, {"D", 2}, {"E", 1}},
        Participants: 2,
    }
    expected := Output{Allocations: []Allocation{{
        Participant: 0,
        Items: []Item{{"A", 5}, {"D", 2}, {"E", 1}},
        TotalValue: 8,
    }, {
        Participant: 1,
        Items: []Item{{"B", 4}, {"C", 3}},
        TotalValue: 7,
    }}}

    got := allocate(inp)
    if !reflect.DeepEqual(got, expected) {
        t.Fatalf("allocation mismatch\nexpected: %v\n   got: %v", expected, got)
    }
}

func TestAllocateJSONRoundTrip(t *testing.T) {
    // # Mock rationale: ensure that JSON marshaling/unmarshaling works without external services.
    raw := `{"items":[{"name":"Gold","value":100},{"name":"Silver","value":50}],"participants":2}`
    var inp Input
    if err := json.Unmarshal([]byte(raw), &inp); err != nil {
        t.Fatalf("failed to unmarshal input JSON: %v", err)
    }
    out := allocate(inp)
    // Verify that total value is preserved.
    total := 0
    for _, a := range out.Allocations {
        total += a.TotalValue
    }
    if total != 150 {
        t.Fatalf("total value mismatch: expected 150, got %d", total)
    }
}
