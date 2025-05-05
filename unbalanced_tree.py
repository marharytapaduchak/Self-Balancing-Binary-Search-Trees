"""
Contains unbalanced binary tree representation
"""

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class UnbalancedTreeNode(AbstractTreeNode):
    """
    Represents unbalanced binary tree node
    """

    def __init__(self, data_entry: DataEntry):
        super().__init__(data_entry)
        self.left = None
        self.right = None


class UnbalancedTree(AbstractTree):
    """
    Represents unbalanced binary tree
    """

    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root = None

    def __erase_node(self, node: UnbalancedTreeNode):
        if node.left is None:
            return node.right

        if node.right is None:
            return node.left

        tmp_node = node.right
        node.right = tmp_node.left
        tmp_node.left = self.__erase_node(node)

        return tmp_node

    def insert(self, data_entry: DataEntry) -> None:
        if self.__root is None:
            self.__root = UnbalancedTreeNode(data_entry)
            return

        curr_node = self.__root

        while True:
            if data_entry.columns[self.key_col] < curr_node.data[0].columns[self.key_col]:
                if curr_node.left is None:
                    curr_node.left = UnbalancedTreeNode(data_entry)
                    return
                curr_node = curr_node.left
            elif data_entry.columns[self.key_col] > curr_node.data[0].columns[self.key_col]:
                if curr_node.right is None:
                    curr_node.right = UnbalancedTreeNode(data_entry)
                    return
                curr_node = curr_node.right
            else:
                curr_node.data.append(data_entry)
                return

    def find(self, key) -> list[DataEntry]:
        curr_node = self.__root

        while True:
            if curr_node is None:
                return []

            if key < curr_node.data[0].columns[self.key_col]:
                curr_node = curr_node.left
            elif key > curr_node.data[0].columns[self.key_col]:
                curr_node = curr_node.right
            else:
                return curr_node.data

    def erase(self, key):
        curr_node = self.__root

        if self.__root is not None and self.__root.data[0].columns[self.key_col] == key:
            self.__root = self.__erase_node(self.__root)
            return

        while True:
            if curr_node is None:
                return

            if key < curr_node.data[0].columns[self.key_col]:
                if curr_node.left is not None and curr_node.left.data[0].columns[self.key_col] == key:
                    curr_node.left = self.__erase_node(curr_node.left)
                    return

                curr_node = curr_node.left
                continue

            if curr_node.right is not None and curr_node.right.data[0].columns[self.key_col] == key:
                curr_node.right = self.__erase_node(curr_node.right)
                return

            curr_node = curr_node.right

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
