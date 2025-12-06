/// Permuted Congruential Generator (PCG) - a fast, high-quality pseudo-random number generator
/// Based on the PCG-XSH-RR variant
pub struct Pcg32 {
    state: u64,
    inc: u64,
}

impl Pcg32 {
    /// Create a new PCG generator with the given seed
    pub fn new(seed: u64) -> Self {
        let mut pcg = Pcg32 {
            state: 0,
            inc: (seed << 1) | 1,
        };
        
        // Initialize the state
        pcg.next_u32();
        pcg.state = pcg.state.wrapping_add(seed);
        pcg.next_u32();
        
        pcg
    }

    /// Generate the next 32-bit random number
    pub fn next_u32(&mut self) -> u32 {
        let oldstate = self.state;
        
        // Advance internal state
        self.state = oldstate.wrapping_mul(6364136223846793005).wrapping_add(self.inc | 1);
        
        // Calculate output function (XSH RR), uses old state for max ILP
        let word = ((oldstate >> 18) ^ oldstate) >> 27;
        let rot = oldstate >> 59;
        
        word.rotate_right(rot) as u32
    }

    /// Generate the next 64-bit random number
    pub fn next_u64(&mut self) -> u64 {
        (self.next_u32() as u64) << 32 | self.next_u32() as u64
    }

    /// Generate a random float in [0, 1)
    pub fn next_float(&mut self) -> f32 {
        self.next_u32() as f32 / (u32::MAX as f32 + 1.0)
    }

    /// Generate a random double in [0, 1)
    pub fn next_double(&mut self) -> f64 {
        self.next_u64() as f64 / (u64::MAX as f64 + 1.0)
    }

    /// Generate a random number in the range [min, max]
    pub fn next_range(&mut self, min: u32, max: u32) -> u32 {
        min + (self.next_u32() % (max - min + 1))
    }

    /// Shuffle a slice in-place using the Fisher-Yates algorithm
    pub fn shuffle<T>(&mut self, slice: &mut [T]) {
        for i in (1..slice.len()).rev() {
            let j = self.next_range(0, i as u32) as usize;
            slice.swap(i, j);
        }
    }

    /// Select a random element from a slice
    pub fn choose<T>(&mut self, slice: &[T]) -> Option<&T> {
        if slice.is_empty() {
            None
        } else {
            Some(&slice[self.next_range(0, slice.len() as u32 - 1) as usize])
        }
    }

    /// Set the stream (sequence) for this generator
    pub fn set_stream(&mut self, stream: u64) {
        self.inc = (stream << 1) | 1;
    }

    /// Get the current state (for debugging or saving state)
    pub fn get_state(&self) -> (u64, u64) {
        (self.state, self.inc)
    }

    /// Set the state (for restoring a saved state)
    pub fn set_state(&mut self, state: u64, inc: u64) {
        self.state = state;
        self.inc = inc | 1; // Ensure inc is always odd
    }
}

impl Default for Pcg32 {
    fn default() -> Self {
        Self::new(42)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_basic_generation() {
        let mut pcg = Pcg32::new(12345);
        
        // Test that we can generate numbers
        let a = pcg.next_u32();
        let b = pcg.next_u32();
        let c = pcg.next_u32();
        
        assert_ne!(a, b);
        assert_ne!(b, c);
        assert_ne!(a, c);
    }

    #[test]
    fn test_deterministic() {
        let mut pcg1 = Pcg32::new(42);
        let mut pcg2 = Pcg32::new(42);
        
        // Same seed should produce same sequence
        for _ in 0..100 {
            assert_eq!(pcg1.next_u32(), pcg2.next_u32());
        }
    }

    #[test]
    fn test_range() {
        let mut pcg = Pcg32::new(42);
        
        for _ in 0..1000 {
            let val = pcg.next_range(10, 20);
            assert!(val >= 10 && val <= 20);
        }
    }

    #[test]
    fn test_float_range() {
        let mut pcg = Pcg32::new(42);
        
        for _ in 0..1000 {
            let val = pcg.next_float();
            assert!(val >= 0.0 && val < 1.0);
        }
    }

    #[test]
    fn test_shuffle() {
        let mut pcg = Pcg32::new(42);
        let mut vec = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        
        // Make a copy to compare
        let original = vec.clone();
        pcg.shuffle(&mut vec);
        
        // Should be different order (very unlikely to be the same)
        assert_ne!(vec, original);
        
        // But should contain the same elements
        vec.sort();
        assert_eq!(vec, original);
    }

    #[test]
    fn test_choose() {
        let mut pcg = Pcg32::new(42);
        let vec = vec![1, 2, 3, 4, 5];
        
        for _ in 0..100 {
            let chosen = pcg.choose(&vec).unwrap();
            assert!(vec.contains(chosen));
        }
        
        // Test empty slice
        let empty: Vec<i32> = vec![];
        assert_eq!(pcg.choose(&empty), None);
    }

    #[test]
    fn test_state_management() {
        let mut pcg = Pcg32::new(42);
        
        // Generate some numbers
        let a = pcg.next_u32();
        let b = pcg.next_u32();
        
        // Save state
        let (state, inc) = pcg.get_state();
        
        // Generate more numbers
        let c = pcg.next_u32();
        let d = pcg.next_u32();
        
        // Restore state
        pcg.set_state(state, inc);
        
        // Should generate the same sequence
        assert_eq!(pcg.next_u32(), c);
        assert_eq!(pcg.next_u32(), d);
    }
}
