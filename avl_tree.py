"""
Implementing AVL-tree.
"""

from data_entry import DataEntry
from abstract_tree import AbstractTree

class AVLTreeNode:
    """
    Represents AVL tree node.
    """

    def __init__(self, data_entry: DataEntry):
        self.data = [data_entry]
        self.left = None
        self.right = None
        self.height = 1


class AVLTree(AbstractTree):
    """
    Represents AVL tree.
    """

    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root = None

    def get_height(self, node: AVLTreeNode):
        """Returns a height of the node."""

        if not node:
            return 0
        return node.height

    def get_balance(self, node: AVLTreeNode):
        """Returns a balance coefficient."""

        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def __rotate_left(self, node: AVLTreeNode):
        """Rotate left."""

        new_root = node.right
        subtree = new_root.left
        new_root.left = node
        node.right = subtree
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        new_root.height = 1 + max(self.get_height(new_root.left), self.get_height(new_root.right))
        return new_root

    def __rotate_right(self, node: AVLTreeNode):
        """Rotate right"""

        new_root = node.left
        subtree = new_root.right
        new_root.right = node
        node.left = subtree
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        new_root.height = 1 + max(self.get_height(new_root.left), self.get_height(new_root.right))
        return new_root

    def __insert(self, node: AVLTreeNode, data_entry: DataEntry) -> AVLTreeNode:
        key = data_entry.columns[self._key_col]

        if node is None:
            return AVLTreeNode(data_entry)

        node_key = node.data[0].columns[self._key_col]

        if key < node_key:
            node.left = self.__insert(node.left, data_entry)
        elif key > node_key:
            node.right = self.__insert(node.right, data_entry)
        else:
            node.data.append(data_entry)
            return node

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Balance the node
        if balance > 1:
            if key < node.left.data[0].columns[self._key_col]:
                return self.__rotate_right(node)
            else:
                node.left = self.__rotate_left(node.left)
                return self.__rotate_right(node)

        if balance < -1:
            if key > node.right.data[0].columns[self._key_col]:
                return self.__rotate_left(node)
            else:
                node.right = self.__rotate_right(node.right)
                return self.__rotate_left(node)

        return node

    def insert(self, data_entry: DataEntry) -> None:
        self.__root = self.__insert(self.__root, data_entry)

    def __min_node(self, node: AVLTreeNode) -> AVLTreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def __delete(self, node: AVLTreeNode, key) -> AVLTreeNode:
        if node is None:
            return None

        node_key = node.data[0].columns[self._key_col]

        if key < node_key:
            node.left = self.__delete(node.left, key)
        elif key > node_key:
            node.right = self.__delete(node.right, key)
        else:
            # Case: multiple entries with same key — remove all
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Replace with in-order successor
            successor = self.__min_node(node.right)
            node.data = successor.data
            node.right = self.__delete(node.right, successor.data[0].columns[self._key_col])

        if node is None:
            return None

        # Update height and rebalance
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Left heavy
        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.__rotate_right(node)
            else:
                node.left = self.__rotate_left(node.left)
                return self.__rotate_right(node)

        # Right heavy
        if balance < -1:
            if self.get_balance(node.right) <= 0:
                return self.__rotate_left(node)
            else:
                node.right = self.__rotate_right(node.right)
                return self.__rotate_left(node)

        return node

    def erase(self, key) -> None:
        self.__root = self.__delete(self.__root, key)

    def find(self, key) -> list[DataEntry]:
        """
        Finds all data entries in the tree matching the given key.
        
        Args:
            key: Value from the key column to search for.

        Returns:
            list[DataEntry]: List of matching entries (empty if not found).
        """

        def __find_recursive(node: AVLTreeNode) -> list[DataEntry]:
            if node is None:
                return []

            node_key = node.data[0].columns[self._key_col]

            if key < node_key:
                return __find_recursive(node.left)
            elif key > node_key:
                return __find_recursive(node.right)
            else:
                return node.data

        return __find_recursive(self.__root)

    def inorder(self) -> list[DataEntry]:
        """
        In-order tree traversal: left → root → right.
        Returns list of DataEntry objects sorted by key column.
        """

        def __inorder_recursive(node: AVLTreeNode, result: list[DataEntry]) -> None:
            if node is None:
                return

            __inorder_recursive(node.left, result)

            for entry in node.data:
                result.append(entry)

            __inorder_recursive(node.right, result)

        result = []
        __inorder_recursive(self.__root, result)

        return result

    def preorder(self) -> list[DataEntry]:
        """
        Pre-order tree traversal: root → left → right.
        Returns list of DataEntry objects.
        """

        def __preorder_recursive(node: AVLTreeNode, result: list[DataEntry]) -> None:
            if node is None:
                return

            for entry in node.data:
                result.append(entry)

            __preorder_recursive(node.left, result)
            __preorder_recursive(node.right, result)

        result = []
        __preorder_recursive(self.__root, result)

        return result

    def postorder(self) -> list[DataEntry]:
        """
        Post-order tree traversal: left → right → root.
        Returns list of DataEntry objects.
        """

        def __postorder_recursive(node: AVLTreeNode, result: list[DataEntry]) -> None:
            if node is None:
                return

            __postorder_recursive(node.left, result)
            __postorder_recursive(node.right, result)

            for entry in node.data:
                result.append(entry)

        result = []
        __postorder_recursive(self.__root, result)
        return result
