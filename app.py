import streamlit as st
import heapq

# Knapsack solver using Branch and Bound
class Node:
    def _init_(self, level, value, weight, bound, items):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound
        self.items = items

    def _lt_(self, other):
        return self.bound > other.bound

def calculate_bound(node, capacity, values, weights, n):
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

def knapsack_branch_and_bound(values, weights, capacity):
    n = len(values)
    items = list(range(n))
    value_weight_ratio = [(values[i] / weights[i], i) for i in range(n)]
    value_weight_ratio.sort(reverse=True, key=lambda x: x[0])

    values = [values[i] for _, i in value_weight_ratio]
    weights = [weights[i] for _, i in value_weight_ratio]
    items = [i for _, i in value_weight_ratio]

    queue = []
    root = Node(-1, 0, 0, 0.0, [])
    root.bound = calculate_bound(root, capacity, values, weights, n)
    heapq.heappush(queue, root)

    max_value = 0
    best_items = []

    while queue:
        node = heapq.heappop(queue)

        if node.bound > max_value:
            next_level = node.level + 1

            if next_level < n:
                included = Node(next_level, node.value + values[next_level],
                                node.weight + weights[next_level], 0.0, node.items + [items[next_level]])
                if included.weight <= capacity:
                    if included.value > max_value:
                        max_value = included.value
                        best_items = included.items
                    included.bound = calculate_bound(included, capacity, values, weights, n)
                    if included.bound > max_value:
                        heapq.heappush(queue, included)

                excluded = Node(next_level, node.value, node.weight, 0.0, node.items)
                excluded.bound = calculate_bound(excluded, capacity, values, weights, n)
                if excluded.bound > max_value:
                    heapq.heappush(queue, excluded)

    return max_value, sorted(best_items)

# Streamlit app
st.title("Knapsack Problem Solver (Branch and Bound)")
st.write("This application solves the Knapsack problem using the Branch and Bound technique.")

# User input for capacity
capacity = st.number_input("Enter the capacity of the knapsack:", min_value=1, step=1, value=10)

# User input for items
st.write("Enter items with their weights and values:")
num_items = st.number_input("Number of items:", min_value=1, step=1, value=1)

weights = []
values = []

for i in range(num_items):
    st.write(f"Item {i + 1}")
    weight = st.number_input(f"Weight of item {i + 1}:", min_value=1, step=1, key=f"weight_{i}")
    value = st.number_input(f"Value of item {i + 1}:", min_value=1, step=1, key=f"value_{i}")
    weights.append(weight)
    values.append(value)

# Solve the problem when the button is clicked
if st.button("Solve Knapsack Problem"):
    if len(weights) != num_items or len(values) != num_items:
        st.error("Please provide weights and values for all items.")
    elif capacity <= 0:
        st.error("Capacity must be greater than zero.")
    else:
        max_value, included_items = knapsack_branch_and_bound(values, weights, capacity)
        st.success(f"Maximum value that can be obtained: {max_value}")
        st.write("Items included in the knapsack (0-based index):", included_items)
