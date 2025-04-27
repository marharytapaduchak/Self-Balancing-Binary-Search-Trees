"""
Implementation of Red-Black tree
"""
from enum import Enum

from data_entry import DataEntry
from abstract_tree import AbstractTree


class RedBlackNode:
    """
    Node in Red-Black tree
    """
    COLORS = Enum("Colors", [("BLACK", 0), ("RED", 1)])
    def __init__(self, data, color: int, left: "RedBlackNode"=None, right: "RedBlackNode"=None):
        """
        color should match enum
        COLORS = Enum("Colors", [("BLACK", 0), ("RED", 1)])
        """
        self.left = left
        self.right = right
        self.data = data
        if color not in self.COLORS:
            raise ValueError('color should match Enum("Colors", [("BLACK", 0), ("RED", 1)])')
        self.color = color


class RedBlackTree(AbstractTree):
    """
    Red-Black tree
    """
    def __init__(self, key_col: int):
        super().__init__(key_col)
        self._root = None



