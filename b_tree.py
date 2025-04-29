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
        self.t = t
        self._root = BTreeNode(leaf=True)

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
        # Create new node to hold y's right half
        z = BTreeNode(leaf=y.leaf)
        # Median entry to move up
        median = y.keys[t - 1]

        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]

        if not y.leaf:
            z.child = y.child[t:]
            y.child = y.child[:t]

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

        if x.leaf:
            x.keys.append(data_entry)
            while i >= 0 and k < x.keys[i].columns[self._key_col]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = data_entry
        else:
            while i >= 0 and k < x.keys[i].columns[self._key_col]:
                i -= 1
            i += 1
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
        if node.leaf:
            return None
        return self.find(key, node.child[i])


    def erase(self, key) -> None:
        """
        Erases data entries from tree by key
        """

    def inorder(self):
        return self._inorder(self._root)

    def _inorder(self, node):
        if node is None:
            return []
        res = []
        for i, key in enumerate(node.keys):
            if i < len(node.child):
                res.extend(self._inorder(node.child[i]))
            res.append(key)
        if len(node.child) > len(node.keys):
            res.extend(self._inorder(node.child[-1]))
        return res

    def preorder(self):
        return self._preorder(self._root)

    def _preorder(self, node):
        if node is None:
            return []
        res = []
        res.extend(node.keys)
        for c in node.child:
            res.extend(self._preorder(c))
        return res

    def postorder(self):
        return self._postorder(self._root)

    def _postorder(self, node):
        if node is None:
            return []
        res = []
        for c in node.child:
            res.extend(self._postorder(c))
        res.extend(node.keys)
        return res
