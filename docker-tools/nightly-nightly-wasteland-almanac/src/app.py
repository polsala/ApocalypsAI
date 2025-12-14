import os
import random
from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)

DATA_DIR = 'data'

def load_data(filename):
    """Loads data from a text file, one item per line."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: Data file not found: {filepath}")
        return [f"No {filename.split('.')[0]} found. The wastes are silent."]

@app.route('/')
def index():
    """Renders the main almanac page."""
    wisdom_list = load_data('wisdom.txt')
    foraging_tips = load_data('foraging_tips.txt')
    lore_snippets = load_data('lore.txt')

    # Determine daily wisdom deterministically based on the day of the year
    # Mock rationale: This ensures that for testing, we can control the 'today's date'
    # and get a predictable wisdom item, making tests deterministic.
    today = datetime.now()
    day_of_year = today.timetuple().tm_yday
    
    # Use day_of_year as a seed for random selection to make it "daily" and consistent
    # for a given day, but still appear random over time.
    # If wisdom_list is empty, this will prevent an IndexError.
    if wisdom_list:
        random.seed(day_of_year) # # Mock rationale: Seed random for deterministic daily selection
        daily_wisdom = random.choice(wisdom_list)
    else:
        daily_wisdom = "No wisdom today. Just the wind."

    return render_template(
        'index.html',
        daily_wisdom=daily_wisdom,
        foraging_tips=foraging_tips,
        lore_snippets=lore_snippets,
        now=today # Pass the datetime object to the template
    )

if __name__ == '__main__':
    # Ensure data directory exists for local running, though Docker handles copying
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        # Create dummy files if they don't exist for local testing
        with open(os.path.join(DATA_DIR, 'wisdom.txt'), 'w') as f:
            f.write("Always check your six.\n")
            f.write("A full canteen is worth more than gold.\n")
        with open(os.path.join(DATA_DIR, 'foraging_tips.txt'), 'w') as f:
            f.write("If it glows, don't eat it.\n")
            f.write("Mushrooms are tricky; when in doubt, leave it out.\n")
        with open(os.path.join(DATA_DIR, 'lore.txt'), 'w') as f:
            f.write("The Old World fell not with a bang, but a whimper.\n")
            f.write("Beware the Whispering Sands; they claim many a wanderer.\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
