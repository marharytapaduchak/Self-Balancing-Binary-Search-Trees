"""
Contains splay tree representation
"""

from data_entry import DataEntry
from abstract_tree import AbstractTree

class SplayTreeNode:
    """
    Represents splay tree node
    """

    def __init__(self, data_entry: DataEntry):
        self.data = [data_entry]
        self.left = None
        self.right = None
        self.parent = None

class SplayTree(AbstractTree):
    """
    Represents splay tree
    """

    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root = None

    def __rotate_left(self, node: SplayTreeNode) -> None:
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        new_root.parent = node.parent
        node.parent = new_root
        if node.right is not None:
            node.right.parent = node

        if node is self.__root:
            self.__root = new_root
        else:
            if node is new_root.parent.left:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root

    def __rotate_right(self, node: SplayTreeNode) -> None:
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        new_root.parent = node.parent
        node.parent = new_root
        if node.left is not None:
            node.left.parent = node

        if node is self.__root:
            self.__root = new_root
        else:
            if node is new_root.parent.left:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root

    def __splay(self, node: SplayTreeNode) -> None:
        if node.parent is None:
            self.__root = node
            return

        if node.parent is self.__root:
            if node is self.__root.left:
                self.__rotate_right(self.__root)
            else:
                self.__rotate_left(self.__root)
            return

        if node.parent is node.parent.parent.left:
            self.__rotate_right(node.parent.parent)
        else:
            self.__rotate_left(node.parent.parent)

        if node is node.parent.left:
            self.__rotate_right(node.parent)
        else:
            self.__rotate_left(node.parent)

        self.__splay(node)

    def insert(self, data_entry: DataEntry) -> None:
        if self.__root is None:
            self.__root = SplayTreeNode(data_entry)
            return

        curr_node = self.__root

        while True:
            if data_entry.columns[self._key_col] < curr_node.data[0].columns[self._key_col]:
                if curr_node.left is None:
                    curr_node.left = SplayTreeNode(data_entry)
                    curr_node.left.parent = curr_node
                    self.__splay(curr_node.left)
                    return
                curr_node = curr_node.left
            elif data_entry.columns[self._key_col] > curr_node.data[0].columns[self._key_col]:
                if curr_node.right is None:
                    curr_node.right = SplayTreeNode(data_entry)
                    curr_node.right.parent = curr_node
                    self.__splay(curr_node.right)
                    return
                curr_node = curr_node.right
            else:
                curr_node.data.append(data_entry)
                return

    def find(self, key) -> list[DataEntry]:
        if self.__root is None:
            return []

        curr_node = self.__root

        while True:
            if key < curr_node.data[0].columns[self._key_col]:
                if curr_node.left is None:
                    self.__splay(curr_node)
                    return []
                curr_node = curr_node.left
            elif key > curr_node.data[0].columns[self._key_col]:
                if curr_node.right is None:
                    self.__splay(curr_node)
                    return []
                curr_node = curr_node.right
            else:
                self.__splay(curr_node)
                return self.__root.data

    def erase(self, key) -> None:
        data_to_erase = self.find(key)
        if not data_to_erase:
            return

        left_subtree = self.__root.left
        if left_subtree is not None:
            left_subtree.parent = None
            right_subtree = self.__root.right

            self.__root = left_subtree

            greatest_node = self.__root
            while greatest_node.right is not None:
                greatest_node = greatest_node.right

            self.__splay(greatest_node)
            self.__root.right = right_subtree
            if right_subtree is not None:
                right_subtree.parent = self.__root
        else:
            self.__root = self.__root.right
            if self.__root is not None:
                self.__root.parent = None

    def inorder(self) -> list[DataEntry]:
        def inorder_recursive(node, result):
            if node is None:
                return

            inorder_recursive(node.left, result)

            for data_entry in node.data:
                result.append(data_entry)

            inorder_recursive(node.right, result)

        result = []

        inorder_recursive(self.__root, result)

        return result

    def preorder(self) -> list[DataEntry]:
        def preorder_recursive(node, result):
            if node is None:
                return

            for data_entry in node.data:
                result.append(data_entry)

            preorder_recursive(node.left, result)
            preorder_recursive(node.right, result)

        result = []

        preorder_recursive(self.__root, result)

        return result

    def postorder(self) -> list[DataEntry]:
        def postorder_recursive(node, result):
            if node is None:
                return

            postorder_recursive(node.left, result)
            postorder_recursive(node.right, result)

            for data_entry in node.data:
                result.append(data_entry)

        result = []

        postorder_recursive(self.__root, result)

        return result
