"""
Test file to verify Red-Black Tree balancing properties
"""
import random
import time
import matplotlib.pyplot as plt
from collections import deque

# Import your implementation
from red_black_tree import RedBlackTree, RedBlackNode
from data_entry import DataEntry

class SimpleDataEntry(DataEntry):
    """Simple implementation of DataEntry for testing"""
    def __init__(self, key):
        self.columns = [key]

    def __str__(self):
        return str(self.columns[0])


def verify_rb_properties(tree):
    """
    Verify Red-Black Tree properties:
    1. Every node is either red or black
    2. The root is black
    3. Every leaf (NIL) is black
    4. If a node is red, then both its children are black
    5. For each node, all simple paths from the node to descendant leaves contain the same number of black nodes

    Returns: (is_valid, error_message, black_height)
    """
    root = tree._RedBlackTree__root

    # Empty tree is valid
    if root is None:
        return True, "Tree is empty", 0

    # Property 2: Root must be black
    if root.color != RedBlackNode.COLORS["BLACK"].value:
        return False, "Root is not black", 0

    errors = []

    # Check properties 1, 3, 4, and compute black heights
    def check_node(node, is_red_parent, path_black_count):
        if node is None:
            return True, path_black_count

        # Property 1: Check node color is valid
        if node.color not in (RedBlackNode.COLORS["RED"].value, RedBlackNode.COLORS["BLACK"].value):
            errors.append(f"Node {node.data[0]} has invalid color {node.color}")
            return False, 0

        # Property 4: Red nodes cannot have red children
        if is_red_parent and node.color == RedBlackNode.COLORS["RED"].value:
            errors.append(f"Red node {node.data[0]} has red parent")
            return False, 0

        # Update black count if this node is black
        current_black_count = path_black_count
        if node.color == RedBlackNode.COLORS["BLACK"].value:
            current_black_count += 1

        # Check if node's parent reference is correct
        if node.left is not None and node.left.parent != node:
            errors.append(f"Node {node.data[0]}'s left child has incorrect parent")
            return False, 0

        if node.right is not None and node.right.parent != node:
            errors.append(f"Node {node.data[0]}'s right child has incorrect parent")
            return False, 0

        # Check left subtree
        left_valid, left_black_count = check_node(
            node.left,
            node.color == RedBlackNode.COLORS["RED"].value,
            current_black_count
        )

        # Check right subtree
        right_valid, right_black_count = check_node(
            node.right,
            node.color == RedBlackNode.COLORS["RED"].value,
            current_black_count
        )

        # Property 5: All paths must have same black height
        if left_valid and right_valid and left_black_count != right_black_count:
            errors.append(f"Node {node.data[0]} has different black heights in subtrees ({left_black_count} vs {right_black_count})")
            return False, 0

        return left_valid and right_valid, left_black_count

    # Start checking from root
    is_valid, black_height = check_node(root, False, 0)

    if not is_valid:
        return False, "\n".join(errors), 0

    return True, "All Red-Black properties are satisfied", black_height


def calculate_tree_height(tree):
    """Calculate the actual height of the tree"""
    root = tree._RedBlackTree__root
    if root is None:
        return 0

    # Use BFS to find the height
    queue = deque([(root, 1)])  # (node, height)
    max_height = 0

    while queue:
        node, height = queue.popleft()
        max_height = max(max_height, height)

        if node.left:
            queue.append((node.left, height + 1))
        if node.right:
            queue.append((node.right, height + 1))

    return max_height


def test_sequential_insertion():
    """Test inserting sequential keys and check balance"""
    print("=== Testing Sequential Insertion ===")
    sizes = [10, 100, 1000, 10000]
    for size in sizes:
        tree = RedBlackTree(0)

        # Insert sequential keys
        for i in range(size):
            entry = SimpleDataEntry(i)
            tree.insert(entry)

        # Verify properties
        is_valid, message, black_height = verify_rb_properties(tree)
        actual_height = calculate_tree_height(tree)
        theoretical_min = 2 * black_height - 1  # Minimum possible height for valid RB tree
        theoretical_max = 2 * black_height  # Maximum possible height for valid RB tree

        print(f"Size: {size}")
        print(f"Valid: {is_valid}")
        print(f"Black Height: {black_height}")
        print(f"Actual Height: {actual_height}")
        print(f"Theoretical Min-Max Height: {theoretical_min}-{theoretical_max}")
        print(f"Actual/Log₂(n) ratio: {actual_height / (size.bit_length()):.2f}")

        if not is_valid:
            print(f"Error: {message}")
        print()


def test_random_insertion():
    """Test inserting random keys and check balance"""
    print("=== Testing Random Insertion ===")
    sizes = [10, 100, 1000, 10000]
    for size in sizes:
        tree = RedBlackTree(0)

        # Generate random keys
        keys = random.sample(range(size * 10), size)

        # Insert random keys
        for key in keys:
            entry = SimpleDataEntry(key)
            tree.insert(entry)

        # Verify properties
        is_valid, message, black_height = verify_rb_properties(tree)
        actual_height = calculate_tree_height(tree)
        theoretical_min = 2 * black_height - 1  # Minimum possible height for valid RB tree
        theoretical_max = 2 * black_height  # Maximum possible height for valid RB tree

        print(f"Size: {size}")
        print(f"Valid: {is_valid}")
        print(f"Black Height: {black_height}")
        print(f"Actual Height: {actual_height}")
        print(f"Theoretical Min-Max Height: {theoretical_min}-{theoretical_max}")
        print(f"Actual/Log₂(n) ratio: {actual_height / (size.bit_length()):.2f}")

        if not is_valid:
            print(f"Error: {message}")
        print()


def test_insertion_performance():
    """Test insertion performance and how it correlates with tree balance"""
    print("=== Testing Insertion Performance vs Tree Height ===")
    sizes = [100, 1000, 5000, 10000, 20000, 30000, 40000, 50000]
    sequential_times = []
    sequential_heights = []
    random_times = []
    random_heights = []

    for size in sizes:
        # Sequential insertion
        tree = RedBlackTree(0)
        start_time = time.time()
        for i in range(size):
            entry = SimpleDataEntry(i)
            tree.insert(entry)
        seq_time = time.time() - start_time
        sequential_times.append(seq_time)
        sequential_heights.append(calculate_tree_height(tree))

        # Random insertion
        tree = RedBlackTree(0)
        keys = random.sample(range(size * 10), size)
        start_time = time.time()
        for key in keys:
            entry = SimpleDataEntry(key)
            tree.insert(entry)
        rand_time = time.time() - start_time
        random_times.append(rand_time)
        random_heights.append(calculate_tree_height(tree))

        print(f"Size: {size}")
        print(f"Sequential: Time={seq_time:.4f}s, Height={sequential_heights[-1]}")
        print(f"Random: Time={rand_time:.4f}s, Height={random_heights[-1]}")
        print()

    # Plot results
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.title("Insertion Time vs Tree Size")
    plt.plot(sizes, sequential_times, 'b-o', label="Sequential")
    plt.plot(sizes, random_times, 'r-o', label="Random")
    plt.xlabel("Number of Elements")
    plt.ylabel("Time (seconds)")
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.title("Tree Height vs Tree Size")
    plt.plot(sizes, sequential_heights, 'b-o', label="Sequential")
    plt.plot(sizes, random_heights, 'r-o', label="Random")
    plt.plot(sizes, [2 * (n.bit_length()) for n in sizes], 'g--', label="2 × log₂(n)")
    plt.xlabel("Number of Elements")
    plt.ylabel("Tree Height")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("rb_tree_insertion_analysis.png")
    plt.close()

    print("Analysis plot saved as rb_tree_insertion_analysis.png")


def validate_find_operations(tree, keys):
    """Validate that find operations return correct results"""
    all_found = True
    for key in keys:
        result = tree.find(key)
        if not result or result[0].columns[0] != key:
            all_found = False
            print(f"Error: Could not find key {key}")
    return all_found


def test_color_balance():
    """Test if the tree has a reasonable color balance"""
    print("=== Testing Color Balance ===")
    sizes = [100, 1000, 10000]

    for size in sizes:
        tree = RedBlackTree(0)
        keys = random.sample(range(size * 10), size)

        # Insert random keys
        for key in keys:
            entry = SimpleDataEntry(key)
            tree.insert(entry)

        # Count red and black nodes
        def count_colors(node):
            if node is None:
                return 0, 0

            red_count = 1 if node.color == RedBlackNode.COLORS["RED"].value else 0
            black_count = 1 if node.color == RedBlackNode.COLORS["BLACK"].value else 0

            left_red, left_black = count_colors(node.left)
            right_red, right_black = count_colors(node.right)

            return red_count + left_red + right_red, black_count + left_black + right_black

        red_count, black_count = count_colors(tree._RedBlackTree__root)
        total = red_count + black_count

        print(f"Size: {size}")
        print(f"Red nodes: {red_count} ({red_count/total*100:.1f}%)")
        print(f"Black nodes: {black_count} ({black_count/total*100:.1f}%)")
        print(f"Red-to-Black ratio: {red_count/black_count if black_count else 'N/A'}")
        print()


def visualize_small_tree():
    """Create a visualization of a small RB tree to check balancing"""
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
    except ImportError:
        print("networkx library not available, skipping tree visualization")
        return

    print("=== Visualizing Small Tree ===")
    tree = RedBlackTree(0)

    # Insert some keys
    for i in [5, 3, 7, 2, 4, 6, 8, 1, 9]:
        entry = SimpleDataEntry(i)
        tree.insert(entry)

    # Create a graph
    G = nx.DiGraph()

    # Add nodes and edges using BFS
    root = tree._RedBlackTree__root
    if root is None:
        print("Tree is empty")
        return

    queue = deque([root])
    while queue:
        node = queue.popleft()
        node_id = id(node)
        key = node.data[0].columns[0]
        color = "red" if node.color == RedBlackNode.COLORS["RED"].value else "black"
        G.add_node(node_id, key=key, color=color)

        # Add left child
        if node.left:
            left_id = id(node.left)
            left_key = node.left.data[0].columns[0]
            left_color = "red" if node.left.color == RedBlackNode.COLORS["RED"].value else "black"
            G.add_node(left_id, key=left_key, color=left_color)
            G.add_edge(node_id, left_id)
            queue.append(node.left)

        # Add right child
        if node.right:
            right_id = id(node.right)
            right_key = node.right.data[0].columns[0]
            right_color = "red" if node.right.color == RedBlackNode.COLORS["RED"].value else "black"
            G.add_node(right_id, key=right_key, color=right_color)
            G.add_edge(node_id, right_id)
            queue.append(node.right)

    # Draw the tree
    plt.figure(figsize=(10, 8))
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    node_colors = [G.nodes[n]["color"] for n in G.nodes()]
    labels = {n: G.nodes[n]["key"] for n in G.nodes()}

    nx.draw(G, pos, labels=labels, with_labels=True, node_color=node_colors,
            node_size=800, font_color='white', font_weight='bold')

    plt.savefig("rb_tree_visualization.png")
    plt.close()
    print("Tree visualization saved as rb_tree_visualization.png")


if __name__ == "__main__":
    print("Running Red-Black Tree Balance Tests")
    print("=" * 50)

    test_sequential_insertion()
    test_random_insertion()
    test_color_balance()
    test_insertion_performance()

    # Optional: requires networkx and graphviz
    try:
        visualize_small_tree()
    except Exception as e:
        print(f"Visualization failed: {e}")