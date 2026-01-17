package main

import "testing"

func TestGetPurificationSteps(t *testing.T) {
    cases := []struct {
        ph        float64
        turbidity float64
        coliform  int
        expected  []string
    }{
        // Safe water – no action needed
        {7.0, 2.0, 0, []string{"Water appears safe – no treatment needed"}},
        // Acidic water needs pH adjustment
        {5.5, 2.0, 0, []string{"Adjust pH (add baking soda or acid)"}},
        // High turbidity needs filtration
        {7.2, 10.0, 0, []string{"Filter (remove particulates)"}},
        // Coliform present, low turbidity – UV
        {7.2, 3.0, 10, []string{"UV treatment (kill microbes)"}},
        // Coliform present, high turbidity – boil after filtration
        {7.2, 30.0, 10, []string{"Filter (remove particulates)", "Boil (kill microbes)"}},
        // Multiple issues combined
        {5.0, 12.0, 5, []string{"Adjust pH (add baking soda or acid)", "Filter (remove particulates)", "UV treatment (kill microbes)"}},
    }

    for i, c := range cases {
        got := getPurificationSteps(c.ph, c.turbidity, c.coliform)
        if len(got) != len(c.expected) {
            t.Fatalf("case %d: expected %d steps, got %d", i, len(c.expected), len(got))
        }
        for j := range got {
            if got[j] != c.expected[j] {
                t.Fatalf("case %d, step %d: expected %q, got %q", i, j, c.expected[j], got[j])
            }
        }
    }
}
