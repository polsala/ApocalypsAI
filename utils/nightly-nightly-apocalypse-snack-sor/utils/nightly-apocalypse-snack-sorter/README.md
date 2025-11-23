# Nightly Apocalypse Snack Sorter

## 🍎🍫🥫 Prioritize Your Post-Apocalyptic Pantry! 🥫🍫🍎

In the grim future, every bite counts. The `nightly-apocalypse-snack-sorter` is a crucial utility for any discerning survivor, helping you manage your precious food hoard. This tool takes your scavenged snacks and sorts them by immediate consumption priority, ensuring nothing goes to waste and morale stays high.

### Features:

*   **Shelf Life Prioritization**: Eat the perishables first!
*   **Nutritional Value**: Get your calories when you need them most.
*   **Comfort Factor**: Sometimes, a little treat is all it takes to keep going.

### How to Use:

1.  **Prepare your snack list**: Create a text file (e.g., `snacks.txt`) where each line represents a snack with the following comma-separated format:
    `Snack Name,Shelf Life (days),Calories,Comfort Score (1-5)`

    *   `Snack Name`: A descriptive name for your snack.
    *   `Shelf Life (days)`: Estimated days until spoilage/expiration. Lower is higher priority.
    *   `Calories`: Approximate caloric content. Higher is generally better.
    *   `Comfort Score (1-5)`: A subjective rating of how much this snack boosts morale (1 = meh, 5 = pure bliss).

    **Example `snacks.txt`:**
    ```
    Fresh Apple,7,95,4
    Canned Beans,730,200,2
    MRE,1825,1200,3
    Chocolate Bar,365,250,5
    Dried Fruit,365,150,3
    Water Bottle,3650,0,1
    ```

2.  **Run the sorter**: Execute the Python script with your snack file as an argument:
    ```bash
    python3 src/sorter.py snacks.txt
    ```

### Output:

The script will print a prioritized list of your snacks to the console, indicating the recommended order of consumption. Snacks with shorter shelf lives will appear first. For snacks with similar shelf lives, those with higher calories and then higher comfort scores will be prioritized.

**Example Output:**
```
--- Apocalypse Snack Prioritization --- 

1. Fresh Apple (Shelf Life: 7 days, Calories: 95, Comfort: 4) - **CRITICAL: CONSUME IMMEDIATELY!**
2. Chocolate Bar (Shelf Life: 365 days, Calories: 250, Comfort: 5) - Consume Soon!
3. Dried Fruit (Shelf Life: 365 days, Calories: 150, Comfort: 3) - Consume Soon!
4. Canned Beans (Shelf Life: 730 days, Calories: 200, Comfort: 2) - Store for Later.
5. MRE (Shelf Life: 1825 days, Calories: 1200, Comfort: 3) - Store for Later.
6. Water Bottle (Shelf Life: 3650 days, Calories: 0, Comfort: 1) - Store for Later.

--- Stay Fed, Stay Alive! ---
```
