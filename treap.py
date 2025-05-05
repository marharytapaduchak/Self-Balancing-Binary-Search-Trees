"""
Contains randomized cartesian tree (treap) representation
"""

import random

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class TreapNode(AbstractTreeNode):
    """
    Represents treap node
    """

    def __init__(self, data_entry: DataEntry):
        super().__init__(data_entry)
        self.left = None
        self.right = None
        self.priority = random.random()

class Treap(AbstractTree):
    """
    Represents randomized cartesian tree (treap)
    """

    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root = None

    def __rotate_left(self, node: TreapNode) -> None:
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        return new_root

    def __rotate_right(self, node: TreapNode) -> None:
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        return new_root

    def insert(self, data_entry: DataEntry) -> None:
        def insert_recursive(node):
            if node is None:
                return TreapNode(data_entry)

            if data_entry.columns[self.key_col] < node.data[0].columns[self.key_col]:
                node.left = insert_recursive(node.left)
                if node.left.priority < node.priority:
                    node = self.__rotate_right(node)
                return node

            if data_entry.columns[self.key_col] > node.data[0].columns[self.key_col]:
                node.right = insert_recursive(node.right)
                if node.right.priority < node.priority:
                    node = self.__rotate_left(node)
                return node

            node.data.append(data_entry)
            return node

        self.__root = insert_recursive(self.__root)

    def find(self, key) -> list[DataEntry]:
        if self.__root is None:
            return []

        curr_node = self.__root

        while True:
            if key < curr_node.data[0].columns[self.key_col]:
                if curr_node.left is None:
                    return []
                curr_node = curr_node.left
            elif key > curr_node.data[0].columns[self.key_col]:
                if curr_node.right is None:
                    return []
                curr_node = curr_node.right
            else:
                return curr_node.data

    def erase(self, key) -> None:
        def erase_recursive(node):
            if node is None:
                return None

            if key < node.data[0].columns[self.key_col]:
                node.left = erase_recursive(node.left)
                return node

            if key > node.data[0].columns[self.key_col]:
                node.right = erase_recursive(node.right)
                return node

            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            if node.left.priority < node.right.priority:
                node = self.__rotate_right(node)
                node.right = erase_recursive(node.right)
                return node

            node = self.__rotate_left(node)
            node.left = erase_recursive(node.left)
            return node

        self.__root = erase_recursive(self.__root)

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
