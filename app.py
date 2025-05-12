import streamlit as st
import heapq

# Branch and Bound Node class
class Node:
    def _init_(self, level, profit, weight, bound, items_included):
        self.level = level  # Current item level in the decision tree
        self.profit = profit  # Current profit
        self.weight = weight  # Current weight
        self.bound = bound  # Upper bound on the best possible profit
        self.items_included = items_included  # Items included in the knapsack

    def _lt_(self, other):
        return self.bound > other.bound  # Max-Heap based on bound

# Function to calculate upper bound
def calculate_bound(node, capacity, weights, values, n):
    if node.weight >= capacity:
        return 0
    profit_bound = node.profit
    j = node.level + 1
    total_weight = node.weight

    while j < n and total_weight + weights[j] <= capacity:
        total_weight += weights[j]
        profit_bound += values[j]
        j += 1

    if j < n:
        profit_bound += (capacity - total_weight) * values[j] / weights[j]

    return profit_bound

# Branch and Bound Knapsack Solver
def knapsack_branch_and_bound(values, weights, capacity):
    n = len(values)
    value_per_weight = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    values = [values[i] for i in value_per_weight]
    weights = [weights[i] for i in value_per_weight]

    priority_queue = []
    u = Node(-1, 0, 0, 0, [])
    u.bound = calculate_bound(u, capacity, weights, values, n)
    heapq.heappush(priority_queue, u)

    max_profit = 0
    items_included = []

    while priority_queue:
        u = heapq.heappop(priority_queue)

        if u.bound > max_profit and u.level < n - 1:
            v = Node(u.level + 1, u.profit + values[u.level + 1], u.weight + weights[u.level + 1], 0, u.items_included + [u.level + 1])
            if v.weight <= capacity and v.profit > max_profit:
                max_profit = v.profit
                items_included = v.items_included

            v.bound = calculate_bound(v, capacity, weights, values, n)
            if v.bound > max_profit:
                heapq.heappush(priority_queue, v)

            v = Node(u.level + 1, u.profit, u.weight, 0, u.items_included)
            v.bound = calculate_bound(v, capacity, weights, values, n)
            if v.bound > max_profit:
                heapq.heappush(priority_queue, v)

    return max_profit, [value_per_weight[i] for i in items_included]

# Streamlit app
st.title("Knapsack Problem Solver (Branch and Bound)")
st.write("This application solves the Knapsack problem using the Branch and Bound technique.")

# User input for capacity
capacity = st.number_input("Enter the capacity of the knapsack:", min_value=1, step=1)

# User input for items
st.write("Add items with their weights and values:")
item_data = st.experimental_data_editor(
    [{"Weight": 0, "Value": 0}], 
    num_rows="dynamic", 
    key="item_editor"
)

# Solve the problem when items are added
if st.button("Solve Knapsack Problem"):
    weights = [int(row["Weight"]) for row in item_data if row["Weight"] > 0]
    values = [int(row["Value"]) for row in item_data if row["Value"] > 0]

    if not weights or not values:
        st.error("Please add valid items with weights and values greater than 0.")
    elif len(weights) != len(values):
        st.error("Ensure that all items have both weight and value.")
    else:
        max_value, included_items = knapsack_branch_and_bound(values, weights, capacity)
        st.success(f"Maximum value that can be obtained: {max_value}")
        st.write("Items included in the knapsack (0-based index):", included_items)