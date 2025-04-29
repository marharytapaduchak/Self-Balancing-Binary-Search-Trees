"""
Implementing B-tree.
"""

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class BTreeNode(AbstractTreeNode):
    """
    Represents B-tree node.
    """

    def __init__(self, data_entry: DataEntry = None, leaf = False):
        if data_entry is not None:
            super().__init__(data_entry)
            self.keys: list[DataEntry] = [data_entry]
        else:
            self.data: list[DataEntry] = []
            self.keys: list[DataEntry] = []
        self.leaf: bool = leaf
        self.child: list[BTreeNode] = [] # child pointers


class BTree(AbstractTree):
    """
    Represents B-tree.
    """

    def __init__(self, key_col: int, t: int):
        super().__init__(key_col)
        # Minimum degree (defines max and min keys per node)
        self.t: int = t
        # Initialize tree with an empty leaf root
        self._root: BTreeNode = BTreeNode(leaf=True)

    @property
    def root(self) -> BTreeNode | None:
        """Accessor for the tree's root node."""
        return self._root

    def split_child(self, x, i):
        """
        Splits the full child x.child[i] into two and adjusts x accordingly.
        """
        t = self.t
        y = x.child[i]
        # Create new node z to hold y's right half
        z = BTreeNode(leaf=y.leaf)
        # Median entry to move up
        median = y.keys[t - 1]
        # Split y's keys
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        # If not leaf, split children too
        if not y.leaf:
            z.child = y.child[t:]
            y.child = y.child[:t]
        # Insert z as new child of x, and median into x.keys
        x.child.insert(i + 1, z)
        x.keys.insert(i, median)


    def insert(self, data_entry):
        root = self._root

        # if root is full, create a new node - tree's height grows by 1
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode(leaf=False)
            self.root = new_root
            new_root.child.append(root)
            self.split_child(new_root, 0)
            self.insert_non_full(new_root, data_entry)
        else:
            self.insert_non_full(root, data_entry)

    def insert_non_full(self, x, data_entry):
        k = data_entry.columns[self._key_col]
        i = len(x.keys) - 1

        # find the correct spot in the leaf to insert the key
        if x.leaf:
            x.keys.append(data_entry)
            while i >= 0 and k < x.keys[i].columns[self._key_col]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = data_entry
        # if not a leaf, find the correct subtree to insert the key
        else:
            while i >= 0 and k < x.keys[i].columns[self._key_col]:
                i -= 1
            i += 1
            # if child node is full, split it
            if len(x.child[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i].columns[self._key_col]:
                    i += 1
            self.insert_non_full(x.child[i], data_entry)

    def find(self, key, node=None):
        """
        Searches for a DataEntry with the specified key.
        Returns a tuple (node, index) if found, else None.
        """
        node = self.root if node is None else node

        i = 0
        while i < len(node.keys) and key > node.keys[i].columns[self._key_col]:
            i += 1

        if i < len(node.keys) and key == node.keys[i].columns[self._key_col]:
            return (node, i)
        elif node.leaf:
            return None
        else:
            return self.find(key, node.child[i])


    def erase(self, key) -> None:
        """
        Erases data entries from tree by key
        """
