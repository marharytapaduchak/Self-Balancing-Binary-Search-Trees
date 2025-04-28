"""
Implementation of Red-Black tree
"""
from enum import Enum

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode


class RedBlackNode(AbstractTreeNode):
    """
    Node in Red-Black tree
    """
    COLORS = Enum("Colors", [("BLACK", 0), ("RED", 1)])
    def __init__(self,
                 data: DataEntry, color: int=1,
                 left: "RedBlackNode"=None, right: "RedBlackNode"=None, parent: "RedBlackNode"=None
                 ):
        """
        color should match enum
        COLORS = Enum("Colors", [("BLACK", 0), ("RED", 1)])
        """
        super().__init__(data)
        self._left = left
        self._right = right
        self.parent = parent
        if color not in self.COLORS:
            raise ValueError('color should match Enum("Colors", [("BLACK", 0), ("RED", 1)])')
        self.color = color

    def __eq__(self, other: "RedBlackNode") -> bool:
        if not isinstance(other, RedBlackNode):
            return False
        return self.data == other.data

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node: "RedBlackNode"):
        self._left = node
        if node is not None:
            node.parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node: "RedBlackNode"):
        self._right = node
        if node is not None:
            node.parent = self


class RedBlackTree(AbstractTree):
    """
    Red-Black tree
    """
    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root: RedBlackNode = None


    def __rotate_left(self, node: RedBlackNode):
        if node is None:
            return
        right = node.right
        par = node.parent
        node.right = right.left
        right.left = node

        if par is None:
            right.color = RedBlackNode.COLORS["BLACK"].value
            right.parent = None
            self.__root = right
        else:
            if par.left == node:
                par.left = right
            else:
                par.right = right

    def __rotate_right(self, node: RedBlackNode):
        if node is None:
            return
        left = node.left
        par = node.parent
        node.left = left.right
        left.right = node

        if par is None:
            left.color = RedBlackNode.COLORS["BLACK"].value
            left.parent = None
            self.__root = left
        else:
            if par.right == node:
                par.right = left
            else:
                par.left = left





    def find(self, key) -> list[DataEntry]:
        curr_node = self.__root

        while True:
            if curr_node is None:
                return []

            if key < curr_node.data[0].columns[self._key_col]:
                curr_node = curr_node.left
            elif key > curr_node.data[0].columns[self._key_col]:
                curr_node = curr_node.right
            else:
                return curr_node.data

    def insert(self, data_entry: DataEntry) -> None|DataEntry:
        """
        returns DataEntry if key from data_entry is already in the tree
        """
        if self.__root is None:
            self.__root = RedBlackNode(data_entry, RedBlackNode.COLORS["BLACK"])
            return None

        def rebalance(node: RedBlackNode):
            parent = node.parent

            while parent is not None and parent.color != RedBlackNode.COLORS["BLACK"]:
                grandpar = parent.parent
                if grandpar is None:
                    if parent.left is None or parent.right is None:
                        return
                    if node == parent.left:
                        node.color = parent.right.color
                    else:
                        node.color = parent.left.color
                    return

                if grandpar.left is not None and grandpar.right is not None and \
                        grandpar.left.color == grandpar.right.color:

                    grandpar.left.color = grandpar.right.color = RedBlackNode.COLORS["BLACK"]
                    grandpar.color = RedBlackNode.COLORS["RED"]
                    node = grandpar

                elif grandpar.left == parent:
                    if parent.right == node:
                        self.__rotate_left(parent)

                    self.__rotate_right(grandpar)
                #elif grandpar.right == parent:
                else:
                    if parent.left == node:
                        self.__rotate_right(parent)

                    self.__rotate_left(grandpar)

                parent = node.parent

            if parent is None:
                node.color = RedBlackNode.COLORS["BLACK"].value



        cur = self.__root
        key = data_entry.columns[self._key_col]
        while cur is not None:
            if key < cur.data[0].columns[self._key_col]:
                if cur.left is None:
                    cur.left = RedBlackNode(data_entry, parent=cur)
                    rebalance(cur.left)
                    break
                cur = cur.left


            elif key > cur.data[0].columns[self._key_col]:
                if cur.right is None:
                    cur.right = RedBlackNode(data_entry, parent=cur)
                    rebalance(cur.right)
                    break
                cur = cur.right


            else:
                cur.data.append(data_entry)
                break



        return None

    def erase(self, key):
        return super().erase(key)

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
        def inner(node: RedBlackNode) -> list[RedBlackNode]:
            if node is None:
                return []
            return [node.data] + inner(node.left) + inner(node.right)

        return inner(self.__root)

    def postorder(self) -> list[DataEntry]:
        return super().postorder()




