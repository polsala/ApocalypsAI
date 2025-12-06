import json
import argparse
from datetime import datetime

def load_cache(filepath):
    """Loads cache data from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Cache file not found at {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None

def audit_cache(cache_data, current_date_str):
    """Audits cache items for expiry and low stock."""
    if not cache_data or 'items' not in cache_data:
        return None

    current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()
    audited_items = []

    for item in cache_data.get('items', []):
        item_status = {
            'name': item.get('name', 'Unknown Item'),
            'quantity': item.get('quantity', 0),
            'unit': item.get('unit', ''),
            'expiry_date': item.get('expiry_date'),
            'min_quantity': item.get('min_quantity', 0),
            'is_expired': False,
            'is_low_stock': False
        }

        if item_status['expiry_date']:
            try:
                expiry_dt = datetime.strptime(item_status['expiry_date'], '%Y-%m-%d').date()
                if expiry_dt < current_date:
                    item_status['is_expired'] = True
            except ValueError:
                # Invalid date format, treat as non-expiring for this audit
                pass

        if item_status['quantity'] < item_status['min_quantity']:
            item_status['is_low_stock'] = True
        
        audited_items.append(item_status)
    
    return {
        'cache_name': cache_data.get('cache_name', 'Unnamed Cache'),
        'location': cache_data.get('location', 'Unknown Location'),
        'items': audited_items
    }

def generate_report(audited_cache):
    """Generates a human-readable report from audited cache data."""
    if not audited_cache:
        return "No cache data to report."

    report_lines = []
    report_lines.append(f"Auditing cache: {audited_cache['cache_name']} ({audited_cache['location']})\n")
    report_lines.append("--- Cache Report ---")

    for item in audited_cache['items']:
        report_lines.append(f"Item: {item['name']}")
        qty_status = "OK" if not item['is_low_stock'] else f"LOW STOCK - Min: {item['min_quantity']}"
        report_lines.append(f"  Quantity: {item['quantity']} {item['unit']} ({qty_status})")
        
        if item['expiry_date']:
            expiry_status = "EXPIRED!" if item['is_expired'] else "OK"
            report_lines.append(f"  Expiry: {item['expiry_date']} ({expiry_status})")
        else:
            report_lines.append("  Expiry: No expiry date")
        report_lines.append("") # Blank line for readability

    return "\n".join(report_lines)

def suggest_restock(audited_cache):
    """Suggests items that need restocking or replacement."""
    if not audited_cache:
        return []

    suggestions = []
    for item in audited_cache['items']:
        if item['is_low_stock']:
            needed = item['min_quantity'] - item['quantity']
            suggestions.append(f"- {item['name']} (Current: {item['quantity']}, Needed: {needed})")
        elif item['is_expired']:
            suggestions.append(f"- {item['name']} (Expired, consider replacement)")
    
    if suggestions:
        return ["--- Restock Suggestions ---"] + suggestions
    else:
        return ["--- Restock Suggestions ---", "- All clear! No immediate restock needed."]

def main():
    parser = argparse.ArgumentParser(description="Audit survival caches for expiry and low stock.")
    parser.add_argument('--cache-file', required=True, help="Path to the JSON cache file.")
    parser.add_argument('--current-date', default=datetime.now().strftime('%Y-%m-%d'),
                        help="Current date in YYYY-MM-DD format (default: today).")
    
    args = parser.parse_args()

    cache_data = load_cache(args.cache_file)
    if cache_data:
        audited_cache = audit_cache(cache_data, args.current_date)
        if audited_cache:
            print(generate_report(audited_cache))
            print("\n".join(suggest_restock(audited_cache)))

if __name__ == '__main__':
    main()
