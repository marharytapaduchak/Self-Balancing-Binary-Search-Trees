"""
Red-Black Tree Animation
This script creates an animated visualization of a Red-Black Tree as data is inserted.
"""
import random
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button
from red_black_tree import RedBlackTree, RedBlackNode
from data_entry import DataEntry

# Function to extract tree structure for visualization
def extract_tree_structure(tree):
    """
    Extract node information from the Red-Black tree for visualization
    Returns a dictionary of nodes with their positions, colors, and connections
    """
    nodes = {}
    edges = []

    def _traverse(node, x, y, level=0, horizontal_pos=0):
        if node is None:
            return

        # Create a unique ID for each node
        node_id = f"{node.data[0].columns[tree.key_col]}"

        # Store node properties
        nodes[node_id] = {
            'x': x,
            'y': y,
            'color': 'red' if node.color == RedBlackNode.COLORS["RED"].value else 'black',
            'key': node.data[0].columns[tree.key_col],
            'level': level
        }

        # Calculate positions for children
        h_spacing = 2.0 / (2 ** (level + 1))

        # Process left child
        if node.left is not None:
            left_id = f"{node.left.data[0].columns[tree.key_col]}"
            edges.append((node_id, left_id))
            _traverse(node.left, x - h_spacing, y - 1, level + 1, horizontal_pos - 1)

        # Process right child
        if node.right is not None:
            right_id = f"{node.right.data[0].columns[tree.key_col]}"
            edges.append((node_id, right_id))
            _traverse(node.right, x + h_spacing, y - 1, level + 1, horizontal_pos + 1)

    # Start traversal from the root
    root = tree._RedBlackTree__root
    if root:
        _traverse(root, 0, 0.5)

    return nodes, edges

def animate_red_black_tree():
    """
    Create an animation showing the step-by-step construction of a Red-Black tree
    """
    # Create a Red-Black tree
    rb_tree = RedBlackTree(0)  # Using the first column as the key

    # Generate random integers for insertion
    num_elements = 20
    random_numbers = random.sample(range(1, 100), num_elements)

    print(f"Random numbers to insert: {random_numbers}")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-4, 1)
    ax.axis('off')

    # Create a graph for animation
    G = nx.DiGraph()

    current_frame = [0]  # Use a mutable object to track the current frame

    def draw_tree(frame):
        if frame < len(random_numbers):
            # Insert the next number
            num = random_numbers[frame]
            entry = DataEntry([num])
            rb_tree.insert(entry)

            # Clear previous frame
            ax.clear()
            ax.set_xlim(-2, 2)
            ax.set_ylim(-4, 1)
            ax.axis('off')

            # Extract tree structure
            nodes, edges = extract_tree_structure(rb_tree)

            # Create a new graph
            G.clear()

            # Add nodes with positions
            for node_id, props in nodes.items():
                G.add_node(node_id, pos=(props['x'], props['y']), color=props['color'], key=props['key'])

            # Add edges
            for source, target in edges:
                G.add_edge(source, target)

            # Get positions for all nodes
            pos = nx.get_node_attributes(G, 'pos')

            # Draw nodes
            node_colors = [data['color'] for _, data in G.nodes(data=True)]

            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, ax=ax)
            nx.draw_networkx_edges(G, pos, arrows=False, ax=ax)

            # Draw labels (keys inside nodes)
            labels = {node: G.nodes[node]['key'] for node in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=labels, font_color='white', ax=ax)

            ax.set_title(f"Red-Black Tree - Inserted {frame+1}/{len(random_numbers)}: {num}")

    def on_next(event):
        if current_frame[0] < len(random_numbers):
            draw_tree(current_frame[0])
            current_frame[0] += 1
            plt.draw()

    # Add a button for manual control
    ax_button = plt.axes([0.4, 0.01, 0.2, 0.05])  # Position of the button
    button = Button(ax_button, 'Next Insertion')
    button.on_clicked(on_next)

    # Initial draw
    draw_tree(current_frame[0])

    plt.tight_layout()
    plt.show()

    # Print the final tree traversal orders
    print("\nFinal tree:")
    print("Inorder traversal:")
    inorder = rb_tree.inorder()
    print([entry.columns[0] for entry in inorder])

    print("\nPreorder traversal:")
    preorder = rb_tree.preorder()
    print([entry.columns[0] for entry in preorder])

if __name__ == "__main__":
    animate_red_black_tree()