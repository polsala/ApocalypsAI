#!/bin/bash

MANIFEST_FILE="manifest.txt"

# Function to ensure manifest file exists
init_manifest() {
    if [ ! -f "$MANIFEST_FILE" ]; then
        touch "$MANIFEST_FILE"
        echo "Initialized empty manifest: $MANIFEST_FILE"
    fi
}

# Function to add/update an item
add_item() {
    local category="$1"
    local item_name="$2"
    local quantity="$3"

    if [[ -z "$category" || -z "$item_name" || -z "$quantity" ]]; then
        echo "Usage: add <CATEGORY> <ITEM_NAME> <QUANTITY>"
        return 1
    fi

    if ! [[ "$quantity" =~ ^[0-9]+$ ]]; then
        echo "Error: Quantity must be a positive integer."
        return 1
    fi

    init_manifest

    # Use a temporary file for atomic updates
    local temp_manifest=$(mktemp)
    local found=0

    while IFS=':' read -r line_category line_item line_quantity; do
        # Trim whitespace from each part
        local existing_category=$(echo "$line_category" | xargs)
        local existing_item=$(echo "$line_item" | xargs)
        local existing_quantity=$(echo "$line_quantity" | xargs)

        if [[ "$existing_category" == "$category" && "$existing_item" == "$item_name" ]]; then
            local new_quantity=$((existing_quantity + quantity))
            echo "$category: $item_name: $new_quantity" >> "$temp_manifest"
            found=1
        else
            echo "$existing_category: $existing_item: $existing_quantity" >> "$temp_manifest"
        fi
    done < "$MANIFEST_FILE"

    if [ "$found" -eq 0 ]; then
        echo "$category: $item_name: $quantity" >> "$temp_manifest"
    fi

    mv "$temp_manifest" "$MANIFEST_FILE"
    echo "Added/Updated: $category: $item_name: $quantity"
}

# Function to list items
list_items() {
    local category_filter="$1"
    init_manifest

    if [ -z "$category_filter" ]; then
        cat "$MANIFEST_FILE"
    else
        grep -i "^$category_filter:" "$MANIFEST_FILE"
    fi
}

# Function to summarize items
summarize_items() {
    init_manifest
    if [ ! -s "$MANIFEST_FILE" ]; then
        echo "Manifest is empty."
        return 0
    fi
    # Use awk to sum quantities for each unique item name
    awk -F': ' '
        {
            item = $2;
            qty = $3;
            gsub(/^[ \t]+|[ \t]+$/, "", item); # Trim whitespace from item name
            gsub(/^[ \t]+|[ \t]+$/, "", qty);  # Trim whitespace from quantity
            sum[item] += qty;
        }
        END {
            for (item in sum) {
                print item ": " sum[item];
            }
        }
    ' "$MANIFEST_FILE" | sort
}

# Function to check for an item
check_item() {
    local item_name="$1"
    if [ -z "$item_name" ]; then
        echo "Usage: check <ITEM_NAME>"
        return 1
    fi
    init_manifest
    grep -iq ": $item_name:" "$MANIFEST_FILE"
}

# Main script logic
case "$1" in
    init)
        init_manifest
        ;;
    add)
        add_item "$2" "$3" "$4"
        ;;
    list)
        list_items "$2"
        ;;
    summary)
        summarize_items
        ;;
    check)
        check_item "$2"
        ;;
    *)
        echo "Usage: $0 {init|add|list|summary|check}"
        echo "  init                                 - Initialize an empty manifest.txt"
        echo "  add <CATEGORY> <ITEM_NAME> <QUANTITY> - Add or update an item"
        echo "  list [CATEGORY]                      - List all items or by category"
        echo "  summary                              - Show total quantities for each item"
        echo "  check <ITEM_NAME>                    - Check if an item exists"
        exit 1
        ;;
esac
