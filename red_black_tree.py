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
        return self.data == other.data

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node: "RedBlackNode"):
        self._left = node
        node.parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node: "RedBlackNode"):
        self._right = node
        node.parent = self


class RedBlackTree(AbstractTree):
    """
    Red-Black tree
    """
    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root: RedBlackNode = None


    def __rotate_left(self, node: RedBlackNode):
        right = node.right
        par = node.parent
        node.right = right.left
        right.left = node

        if par is None:
            right.color = RedBlackNode.COLORS["BLACK"].value
            self.__root = right
        else:
            if par.left == node:
                par.left = right
            else:
                par.right = right

    def __rotate_right(self, node: RedBlackNode):
        left = node.left
        par = node.parent
        node.left = left.right
        left.right = node

        if par is None:
            left.color = RedBlackNode.COLORS["BLACK"].value
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

        def rebalance(node: RedBlackNode):
            parent = node.parent
            if parent is None:
                node.color = RedBlackNode.COLORS["BLACK"].value
            while parent.color != RedBlackNode.COLORS["BLACK"]:
                grandpar = parent.parent
                if grandpar.left.color == grandpar.right.color:
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
                cur = cur.left
                if cur.left is None:
                    cur.left = RedBlackNode(data_entry, parent=cur)
                    rebalance(cur.left)


            elif key > cur.data[0].columns[self._key_col]:
                cur = cur.right
                if cur.right is None:
                    cur.right = RedBlackNode(data_entry, parent=cur)
                    rebalance(cur.right)


            else:
                cur.data.append(data_entry)



        return None

    def erase(self, key):
        return super().erase(key)

    def inorder(self):
        return super().inorder()

    def preorder(self):
        return super().preorder()

    def postorder(self):
        return super().postorder()




