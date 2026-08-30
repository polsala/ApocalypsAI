from flask import Flask, render_template_string, request, redirect, url_for
from datetime import datetime, timedelta
import database

app = Flask(__name__)

# Initialize the database when the app starts
database.init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nightly Forager's Fridge Monitor</title>
    <style>
        body { font-family: 'Courier New', monospace; background-color: #1a1a1a; color: #00ff00; margin: 20px; }
        .container { max-width: 800px; margin: auto; background-color: #333; padding: 20px; border: 1px solid #00ff00; box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); }
        h1, h2 { color: #00ff00; text-shadow: 0 0 5px rgba(0, 255, 0, 0.7); }
        form { margin-bottom: 20px; padding: 15px; border: 1px dashed #00ff00; }
        input[type="text"], input[type="number"], button {
            background-color: #000;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 8px;
            margin: 5px 0;
            font-family: 'Courier New', monospace;
        }
        button { cursor: pointer; background-color: #005500; }
        button:hover { background-color: #008800; }
        .item-list { list-style: none; padding: 0; }
        .item-list li {
            background-color: #222;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #00ff00;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .warning { color: #ff0000; font-weight: bold; text-shadow: 0 0 3px rgba(255, 0, 0, 0.7); }
        .status-buttons button { margin-left: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Nightly Forager's Fridge Monitor</h1>

        <h2>Add New Scavenged Item</h2>
        <form method="POST" action="/add">
            <label for="name">Item Name:</label>
            <input type="text" id="name" name="name" required><br>
            <label for="spoil_days">Days until spoilage:</label>
            <input type="number" id="spoil_days" name="spoil_days" min="1" required><br>
            <button type="submit">Add Item</button>
        </form>

        <h2>Current Inventory</h2>
        <ul class="item-list">
            {% for item in items %}
            <li>
                <div>
                    <strong>{{ item.name }}</strong> (Added: {{ item.added_date }})<br>
                    {% if item.spoil_warning %}
                        <span class="warning">{{ item.spoil_warning }}</span>
                    {% else %}
                        <span>Freshness remaining: {{ item.days_left }} days</span>
                    {% endif %}
                </div>
                <div class="status-buttons">
                    <form method="POST" action="/update_status/{{ item.id }}/consumed" style="display:inline;">
                        <button type="submit">Consumed</button>
                    </form>
                    <form method="POST" action="/update_status/{{ item.id }}/spoiled" style="display:inline;">
                        <button type="submit">Spoiled</button>
                    </form>
                </div>
            </li>
            {% else %}
            <li>No items in your fridge. Time to scavenge!</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

def get_spoil_warning(added_date_str, spoil_days):
    added_date = datetime.strptime(added_date_str, '%Y-%m-%d')
    spoil_date = added_date + timedelta(days=spoil_days)
    today = datetime.now()
    days_left = (spoil_date - today).days

    if days_left < 0:
        return f"This '{spoil_days}-day-old' item is {abs(days_left)} days past its prime. It's now a biohazard, or perhaps a new life form.", None
    elif days_left == 0:
        return "WARNING: This item spoils TODAY! Consume at your own risk, or prepare for mutation.", None
    elif days_left == 1:
        return "CRITICAL: Only 1 day left! The whispers of spoilage are growing louder.", None
    elif days_left <= 3:
        return f"ALERT: Only {days_left} days left! The decay process is accelerating.", None
    return None, days_left # Return None for warning if not critical, and days_left

@app.route('/')
def index():
    items = database.get_all_items()
    processed_items = []
    for item in items:
        warning, days_left = get_spoil_warning(item['added_date'], item['spoil_days'])
        item['spoil_warning'] = warning
        item['days_left'] = days_left if warning is None else None # Only show days_left if no warning
        processed_items.append(item)
    return render_template_string(HTML_TEMPLATE, items=processed_items)

@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    spoil_days = int(request.form['spoil_days'])
    database.add_item(name, spoil_days)
    return redirect(url_for('index'))

@app.route('/update_status/<int:item_id>/<status>', methods=['POST'])
def update_status(item_id, status):
    if status in ['consumed', 'spoiled']:
        database.update_item_status(item_id, status)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
