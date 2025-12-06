def optimize_inventory(items, capacity):
    """
    Optimizes a scavenger's inventory to maximize total value within a given capacity.
    Uses a 0/1 knapsack algorithm.

    Args:
        items (list): A list of dictionaries, where each dictionary represents an item
                      and has keys 'name' (str), 'value' (int), and 'weight' (int).
        capacity (int): The maximum total weight the scavenger can carry.

    Returns:
        tuple: A tuple containing:
               - list: Names of the selected items.
               - int: Total value of the selected items.
               - int: Total weight of the selected items.
    """
    n = len(items)
    # dp[i][w] will store the maximum value that can be obtained with a capacity 'w'
    # using items from the first 'i' items.
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = items[i - 1]
        for w in range(capacity + 1):
            if item['weight'] <= w:
                # Option 1: Include the current item
                #   value of current item + max value of remaining capacity with previous items
                # Option 2: Exclude the current item
                #   max value with previous items and same capacity
                dp[i][w] = max(item['value'] + dp[i - 1][w - item['weight']], dp[i - 1][w])
            else:
                # Cannot include the current item due to weight limit
                dp[i][w] = dp[i - 1][w]

    # Reconstruct the selected items
    selected_items = []
    total_weight = 0
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            # This item was included
            item = items[i - 1]
            selected_items.append(item['name'])
            total_weight += item['weight']
            w -= item['weight']

    selected_items.reverse() # To get them in original order or some logical order
    return selected_items, dp[n][capacity], total_weight
