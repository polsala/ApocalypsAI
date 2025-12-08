import random
import time
import argparse
import sys
import os
from typing import List, Tuple, Dict, Optional


class QuantumGarden:
    """A whimsical quantum garden simulation."""
    
    def __init__(self, size: int = 15, seed: Optional[int] = None):
        self.size = max(5, min(50, size))  # Clamp between 5 and 50
        self.seed = seed
        self.garden: List[List[str]] = [['·' for _ in range(self.size)] for _ in range(self.size)]
        self.flowers: List[Tuple[int, int, str, bool]] = []  # x, y, type, superposition
        self.butterflies: List[Tuple[int, int, str]] = []  # x, y, color
        self.entangled_pairs: List[Tuple[int, int]] = []  # indices of entangled butterflies
        self.generation = 0
        
        # Set seed for reproducibility
        if seed is not None:
            random.seed(seed)
        else:
            random.seed(int(time.time()))
            
    def _quantum_random(self, min_val: float, max_val: float) -> float:
        """Generate a quantum-inspired random number."""
        # Add some quantum-like randomness
        base = random.random()
        quantum_factor = random.choice([0.95, 1.0, 1.05])
        result = base * (max_val - min_val) * quantum_factor + min_val
        return max(min_val, min(max_val, result))
    
    def _place_flower(self, x: int, y: int) -> None:
        """Place a quantum flower at coordinates."""
        flower_types = ['✿', '❀', '❁', '✽', '✾', '✿']
        flower_type = random.choice(flower_types)
        superposition = random.random() < 0.3  # 30% chance of superposition
        
        self.flowers.append((x, y, flower_type, superposition))
        self.garden[y][x] = flower_type
    
    def _place_butterfly(self, x: int, y: int) -> None:
        """Place a butterfly at coordinates."""
        butterfly_colors = ['🦋', '🦋', '🦋', '🦋']
        butterfly_type = random.choice(butterfly_colors)
        
        self.butterflies.append((x, y, butterfly_type))
        self.garden[y][x] = butterfly_type
    
    def _entangle_butterflies(self) -> None:
        """Create entangled pairs of butterflies."""
        if len(self.butterflies) >= 2:
            # Create 1-3 entangled pairs
            pairs_to_create = random.randint(1, min(3, len(self.butterflies) // 2))
            butterfly_indices = list(range(len(self.butterflies)))
            random.shuffle(butterfly_indices)
            
            for i in range(pairs_to_create):
                if i * 2 + 1 < len(butterfly_indices):
                    pair = (butterfly_indices[i * 2], butterfly_indices[i * 2 + 1])
                    self.entangled_pairs.append(pair)
    
    def _quantum_tunnel(self, x: int, y: int) -> Tuple[int, int]:
        """Simulate quantum tunneling to move through barriers."""
        # Try to tunnel to a nearby location
        for _ in range(3):
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            new_x = max(0, min(self.size - 1, x + dx))
            new_y = max(0, min(self.size - 1, y + dy))
            
            if self.garden[new_y][new_x] == '·':  # Empty space
                return new_x, new_y
        
        return x, y  # Can't tunnel, stay put
    
    def _observe_garden(self) -> None:
        """Observe the garden, collapsing quantum states."""
        for i, (x, y, flower_type, superposition) in enumerate(self.flowers):
            if superposition:
                # Collapse superposition to a definite state
                if random.random() < 0.5:
                    # Change to a different flower type
                    new_type = random.choice(['✿', '❀', '❁', '✽', '✾'])
                    self.flowers[i] = (x, y, new_type, False)
                    self.garden[y][x] = new_type
    
    def generate_garden(self) -> None:
        """Generate the initial quantum garden."""
        # Clear garden
        self.garden = [['·' for _ in range(self.size)] for _ in range(self.size)]
        self.flowers = []
        self.butterflies = []
        self.entangled_pairs = []
        
        # Place flowers
        num_flowers = int(self.size * self._quantum_random(0.3, 0.6))
        for _ in range(num_flowers):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.garden[y][x] == '·':
                self._place_flower(x, y)
        
        # Place butterflies
        num_butterflies = int(self.size * self._quantum_random(0.1, 0.3))
        for _ in range(num_butterflies):
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.garden[y][x] == '·':
                self._place_butterfly(x, y)
        
        # Entangle some butterflies
        self._entangle_butterflies()
        
        # Observe to collapse initial states
        self._observe_garden()
    
    def grow_step(self) -> None:
        """Perform one growth step."""
        self.generation += 1
        
        # Move butterflies (with entanglement)
        for i, (x, y, butterfly_type) in enumerate(self.butterflies):
            # Check if this butterfly is entangled
            is_entangled = any(i in pair for pair in self.entangled_pairs)
            
            if is_entangled and random.random() < 0.3:
                # Entangled butterflies mirror movements
                for pair in self.entangled_pairs:
                    if i in pair:
                        other_i = pair[0] if pair[1] == i else pair[1]
                        other_x, other_y, _ = self.butterflies[other_i]
                        new_x, new_y = other_x, other_y
                        break
            else:
                # Normal random movement
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                new_x = max(0, min(self.size - 1, x + dx))
                new_y = max(0, min(self.size - 1, y + dy))
                
                # Try quantum tunneling if blocked
                if self.garden[new_y][new_x] != '·':
                    new_x, new_y = self._quantum_tunnel(new_x, new_y)
            
            # Move butterfly if destination is empty
            if self.garden[new_y][new_x] == '·':
                self.garden[y][x] = '·'
                self.garden[new_y][new_x] = butterfly_type
                self.butterflies[i] = (new_x, new_y, butterfly_type)
        
        # Flowers grow and spread
        new_flowers = []
        for x, y, flower_type, superposition in self.flowers:
            # Chance to spread to adjacent cells
            if random.random() < 0.2:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    new_x = max(0, min(self.size - 1, x + dx))
                    new_y = max(0, min(self.size - 1, y + dy))
                    
                    if self.garden[new_y][new_x] == '·':
                        new_flowers.append((new_x, new_y, flower_type, False))
                        self.garden[new_y][new_x] = flower_type
                        break
        
        self.flowers.extend(new_flowers)
        
        # Occasional quantum event
        if random.random() < 0.1:
            self._observe_garden()
    
    def render(self) -> str:
        """Render the garden as a string."""
        result = []
        result.append("=" * (self.size + 4))
        result.append(f"| Quantum Garden (Gen: {self.generation:3d}) |")
        result.append("=" * (self.size + 4))
        
        for row in self.garden:
            result.append("| " + "".join(row) + " |")
        
        result.append("=" * (self.size + 4))
        
        # Add quantum info
        result.append(f"\nQuantum Effects:")
        result.append(f"  • Flowers in superposition: {sum(1 for _, _, _, s in self.flowers if s)}")
        result.append(f"  • Entangled butterfly pairs: {len(self.entangled_pairs)}")
        result.append(f"  • Garden size: {self.size}×{self.size}")
        if self.seed is not None:
            result.append(f"  • Seed: {self.seed} (reproducible)")
        else:
            result.append(f"  • Seed: timestamp (unique each run)")
        
        return "\n".join(result)


def print_quantum_concept(concept_num: int) -> None:
    """Print an educational quantum concept."""
    concepts = {
        1: """
Quantum Superposition:
In quantum mechanics, particles can exist in multiple states simultaneously
until measured. Our flowers exist in superposition until the garden
is observed, at which point they 'collapse' into a definite state.
""",
        2: """
Quantum Entanglement:
When particles become entangled, they share a mysterious connection.
Measuring one instantly affects the other, no matter the distance.
Our butterflies demonstrate this by mirroring each other's movements.
""",
        3: """
Quantum Tunneling:
In the quantum world, particles can sometimes 'tunnel' through barriers
that would be impossible to cross classically. Our garden simulates this
by allowing entities to occasionally pass through obstacles.
""",
        4: """
Wave Function Collapse:
Quantum systems are described by wave functions containing all possible
states. Upon observation, this wave function 'collapses' to a single
outcome. Observing our garden causes quantum states to become definite.
""",
        5: """
Quantum Uncertainty:
There's a fundamental limit to how precisely we can know certain
properties of quantum systems simultaneously. Our garden embraces this
uncertainty, creating unpredictable but beautiful patterns.
"""
    }
    
    if concept_num in concepts:
        print(concepts[concept_num])


def main():
    parser = argparse.ArgumentParser(description='Generate a whimsical quantum garden')
    parser.add_argument('--size', type=int, default=15, help='Garden size (5-50, default: 15)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')
    parser.add_argument('--speed', choices=['slow', 'medium', 'fast'], default='medium', help='Animation speed')
    parser.add_argument('--duration', type=int, default=10, help='Number of growth cycles')
    parser.add_argument('--concept', action='store_true', help='Show quantum concept explanation')
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.size < 5 or args.size > 50:
        print("Error: Garden size must be between 5 and 50", file=sys.stderr)
        sys.exit(1)
    
    if args.duration < 1 or args.duration > 100:
        print("Error: Duration must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    
    # Speed settings
    speed_delays = {'slow': 0.8, 'medium': 0.4, 'fast': 0.2}
    delay = speed_delays[args.speed]
    
    # Create and run garden
    garden = QuantumGarden(size=args.size, seed=args.seed)
    garden.generate_garden()
    
    # Clear screen (works on most terminals)
    print("\033[2J\033[H", end="")
    
    print("Welcome to the Nightly Quantum Garden!\n")
    print("Watch as quantum effects create a unique garden...\n")
    
    # Animation loop
    for step in range(args.duration):
        # Clear screen
        print("\033[2J\033[H", end="")
        
        # Show header
        print(f"🌌 Nightly Quantum Garden - Step {step + 1}/{args.duration} 🌌\n")
        
        # Grow and render
        if step > 0:
            garden.grow_step()
        
        print(garden.render())
        
        # Show quantum concept every 3 steps
        if args.concept and step % 3 == 0:
            concept_num = (step // 3) % 5 + 1
            print_quantum_concept(concept_num)
        
        # Wait before next step
        if step < args.duration - 1:  # Don't sleep after the last step
            time.sleep(delay)
    
    # Final message
    print("\n" + "=" * 50)
    print("🌸 Quantum Garden simulation complete! 🌸")
    print("=" * 50)
    print("\nTip: Try different seeds for reproducible gardens!")
    print("Example: --seed 42")


if __name__ == "__main__":
    main()
