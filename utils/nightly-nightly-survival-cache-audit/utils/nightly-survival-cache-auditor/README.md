# Nightly Survival Cache Auditor

## Overview
The `nightly-survival-cache-auditor` is a crucial utility for any post-apocalyptic survivor, helping to keep track of vital resources across various caches. It scans designated JSON cache files, identifies expired items, flags low-stock supplies, and provides actionable restock suggestions.

Stay prepared, even when the world isn't.

## Features
- Load cache data from JSON files.
- Audit items for expiry dates and minimum quantity thresholds.
- Generate a comprehensive report of cache status.
- Suggest items that need immediate restocking.

## Usage
```bash
python src/auditor.py --cache-file <path_to_cache.json> [--current-date YYYY-MM-DD]
```

### Example Cache File (`my_cache.json`)
```json
{
  "cache_name": "Emergency Stash",
  "location": "Sector 7G",
  "items": [
    {
      "name": "Water Bottle",
      "quantity": 5,
      "unit": "bottles",
      "expiry_date": "2025-01-01",
      "min_quantity": 3
    },
    {
      "name": "MRE",
      "quantity": 2,
      "unit": "packs",
      "expiry_date": "2024-06-15",
      "min_quantity": 5
    },
    {
      "name": "First Aid Kit",
      "quantity": 1,
      "unit": "kit",
      "expiry_date": null,
      "min_quantity": 1
    },
    {
      "name": "Canned Beans",
      "quantity": 10,
      "unit": "cans",
      "expiry_date": "2023-03-01",
      "min_quantity": 5
    }
  ]
}
```

### Example Output
```
Auditing cache: Emergency Stash (Sector 7G)

--- Cache Report ---
Item: Water Bottle
  Quantity: 5 bottles (OK)
  Expiry: 2025-01-01 (OK)

Item: MRE
  Quantity: 2 packs (LOW STOCK - Min: 5)
  Expiry: 2024-06-15 (OK)

Item: First Aid Kit
  Quantity: 1 kit (OK)
  Expiry: No expiry date

Item: Canned Beans
  Quantity: 10 cans (OK)
  Expiry: 2023-03-01 (EXPIRED!)

--- Restock Suggestions ---
- MRE (Current: 2, Needed: 3)
- Canned Beans (Expired, consider replacement)
```
