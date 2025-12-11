#!/bin/bash

# Nightly Quantum Entanglement Checker - Basic Usage Examples

# Build the utility
echo "🔨 Building the Quantum Entanglement Checker..."
cargo build --release

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo

# Create test files
echo "📝 Creating test files..."
echo "Hello Quantum World" > file1.txt
echo "Hello Quantum World" > file2.txt
echo "Different Content" > file3.txt
echo

# Example 1: Entangle files
echo "🔗 Example 1: Entangling file1.txt and file2.txt"
./target/release/nightly-quantum-entanglement-checker entangle --files file1.txt file2.txt
echo

# Example 2: Check entanglement
echo "🔬 Example 2: Checking entanglement between file1.txt and file2.txt"
./target/release/nightly-quantum-entanglement-checker check --files file1.txt file2.txt
echo

# Example 3: Check entanglement with different files
echo "🔬 Example 3: Checking entanglement between file1.txt and file3.txt (should be decoherent)"
./target/release/nightly-quantum-entanglement-checker check --files file1.txt file3.txt
echo

# Example 4: List all entangled pairs
echo "📋 Example 4: Listing all entangled pairs"
./target/release/nightly-quantum-entanglement-checker list
echo

# Example 5: JSON output
echo "📊 Example 5: JSON output format"
./target/release/nightly-quantum-entanglement-checker check --files file1.txt file2.txt --format json
echo

# Example 6: Batch processing
echo "🔄 Example 6: Batch processing"
echo "file1.txt file2.txt" > pairs.txt
echo "file1.txt file3.txt" >> pairs.txt
./target/release/nightly-quantum-entanglement-checker batch --file pairs.txt
echo

# Example 7: Custom threshold
echo "🎯 Example 7: Custom threshold (0.9)"
./target/release/nightly-quantum-entanglement-checker check --files file1.txt file2.txt --threshold 0.9
echo

# Example 8: Modify one file and check decoherence
echo "⚠️  Example 8: Modifying file1.txt and checking for decoherence"
echo "Modified Content" >> file1.txt
./target/release/nightly-quantum-entanglement-checker check --files file1.txt file2.txt
echo

# Example 9: Clean up records
echo "🧹 Example 9: Cleaning up entanglement records"
./target/release/nightly-quantum-entanglement-checker clean
echo

# Example 10: List pairs after cleanup
echo "📋 Example 10: Listing pairs after cleanup (should be empty)"
./target/release/nightly-quantum-entanglement-checker list
echo

# Cleanup
echo "🧹 Cleaning up test files..."
rm -f file1.txt file2.txt file3.txt pairs.txt .quantum-entanglement-records.toml

echo "✅ All examples completed successfully!"
echo "✨ The Quantum Entanglement Checker is ready to use!"
echo
echo "💡 Tips:":
echo "  - Use 'cargo run --release -- --help' for all available options"
echo "  - Create .quantum-entanglement.toml for configuration"
echo "  - Use batch mode for checking multiple file pairs"
echo "  - JSON output is great for automation and scripting"
echo
