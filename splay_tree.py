"""
Contains splay tree representation
"""

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class SplayTreeNode(AbstractTreeNode):
    """
    Represents splay tree node
    """

    def __init__(self, data_entry: DataEntry):
        super().__init__(data_entry)
        self.__left = None
        self.__right = None
        self.parent = None

    @property
    def left(self):
        """
        Obtains left child node
        """
        return self.__left

    @left.setter
    def left(self, new_left):
        """
        Sets left child node
        """
        self.__left = new_left
        if new_left is not None:
            self.__left.parent = self

    @property
    def right(self):
        """
        Obtains right child node
        """
        return self.__right

    @right.setter
    def right(self, new_right):
        """
        Sets right child node
        """
        self.__right = new_right
        if new_right is not None:
            self.__right.parent = self

class SplayTree(AbstractTree):
    """
    Represents splay tree
    """

    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root = None

    def __rotate_left(self, node: SplayTreeNode) -> None:
        new_root = node.right
        new_root.parent = node.parent
        node.right = new_root.left
        new_root.left = node

        if new_root.parent is None:
            self.__root = new_root
        else:
            if node is new_root.parent.left:
                new_root.parent.left = new_root
            else:
                new_root.parent.right = new_root

    def __rotate_right(self, node: SplayTreeNode) -> None:
        new_root = node.left
        new_root.parent = node.parent
        node.left = new_root.right
        new_root.right = node

        if new_root.parent is None:
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
                # zig
                self.__rotate_right(self.__root)
            else:
                # zag
                self.__rotate_left(self.__root)
            return

        if node.parent is node.parent.parent.left:
            if node is node.parent.left:
                # zig-zig
                self.__rotate_right(node.parent.parent)
            else:
                # zag-zig
                self.__rotate_left(node.parent)
            self.__rotate_right(node.parent)
        else:
            if node is node.parent.right:
                # zag-zag
                self.__rotate_left(node.parent.parent)
            else:
                # zig-zag
                self.__rotate_right(node.parent)
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

        if self.__root.left is not None:
            right_subtree = self.__root.right
            self.__root = self.__root.left
            self.__root.parent = None

            greatest_node = self.__root
            while greatest_node.right is not None:
                greatest_node = greatest_node.right

            self.__splay(greatest_node)
            if right_subtree is not None:
                self.__root.right = right_subtree
                right_subtree.parent = self.__root
        elif self.__root.right is not None:
            self.__root = self.__root.right
            self.__root.parent = None
        else:
            self.__root = None

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
