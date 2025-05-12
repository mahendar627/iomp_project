import streamlit as st
import numpy as np

# Node class for Branch and Bound
class Node:
    def _init_(self, level, value, weight, bound, items):
        self.level = int(level)
        self.value = float(value)
        self.weight = float(weight)
        self.bound = float(bound)
        self.items = list(items)

# Function to calculate the bound for a node
def calculate_bound(node, n, capacity, values, weights):
    if node.weight >= capacity:
        return 0

    bound = node.value
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + weights[j] <= capacity:
        total_weight += weights[j]
        bound += values[j]
        j += 1

    if j < n:
        bound += (capacity - total_weight) * (values[j] / weights[j])

    return bound

# Branch and Bound Knapsack Solver
def knapsack_branch_and_bound(values, weights, capacity):
    n = len(values)
    items = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    sorted_weights = [weights[i] for i in items]
    sorted_values = [values[i] for i in items]

    queue = []
    root = Node(-1, 0, 0, 0.0, [])
    root.bound = calculate_bound(root, n, capacity, sorted_values, sorted_weights)
    queue.append(root)

    max_value = 0
    best_items = []

    while queue:
        current = queue.pop(0)

        if current.level == n - 1 or current.bound <= max_value:
            continue

        next_level = current.level + 1

        # Include the next item
        left = Node(
            next_level,
            current.value + sorted_values[next_level],
            current.weight + sorted_weights[next_level],
            0.0,
            current.items + [items[next_level]],
        )
        if left.weight <= capacity and left.value > max_value:
            max_value = left.value
            best_items = left.items
        left.bound = calculate_bound(left, n, capacity, sorted_values, sorted_weights)
        if left.bound > max_value:
            queue.append(left)

        # Exclude the next item
        right = Node(
            next_level,
            current.value,
            current.weight,
            0.0,
            current.items,
        )
        right.bound = calculate_bound(right, n, capacity, sorted_values, sorted_weights)
        if right.bound > max_value:
            queue.append(right)

    return max_value, sorted(best_items)

# Streamlit application
st.title("Knapsack Problem Solver - Branch and Bound")
st.write("Solve the Knapsack problem using the Branch and Bound technique.")

# User input for capacity
capacity = st.number_input("Enter the capacity of the knapsack:", min_value=1, step=1)

# User input for items
st.write("Add items with their weights and values:")
item_data = st.experimental_data_editor(
    [{"Weight": 0, "Value": 0}],
    num_rows="dynamic",
    key="item_editor"
)

# Solve the problem when the button is clicked
if st.button("Solve Knapsack Problem"):
    try:
        weights = [int(row["Weight"]) for row in item_data if row["Weight"] > 0]
        values = [int(row["Value"]) for row in item_data if row["Value"] > 0]
    except ValueError:
        st.error("Please enter valid integers for weights and values.")

    if not weights or not values:
        st.error("Weights and values cannot be empty or zero.")
    elif len(weights) != len(values):
        st.error("Ensure all items have both weight and value.")
    else:
        max_value, included_items = knapsack_branch_and_bound(values, weights, capacity)
        st.success(f"Maximum value that can be obtained: {max_value}")
        st.write("Items included in the knapsack (0-based index):", included_items)
