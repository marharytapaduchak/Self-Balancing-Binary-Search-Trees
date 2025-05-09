from enum import Enum

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode


class RedBlackNode(AbstractTreeNode):
    COLORS = Enum("Colors", [("BLACK", 0), ("RED", 1)])

    def __init__(self, data: DataEntry, key, color: int = 1,
                 left: "RedBlackNode" = None, right: "RedBlackNode" = None, parent: "RedBlackNode" = None):
        super().__init__(data)
        self._left = left
        self._right = right
        self.parent = parent
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
    def __init__(self, key_col: int):
        super().__init__(key_col)
        self.__root: RedBlackNode = None

    def __node_color(self, node: RedBlackNode):
        if node is None:
            return RedBlackNode.COLORS.BLACK.value
        return node.color

    def __rotate_left(self, node: RedBlackNode):
        if node is None:
            return
        right = node.right
        par = node.parent
        node.right = right.left
        right.left = node

        if par is None:
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
            left.parent = None
            self.__root = left
        else:
            if par.right == node:
                par.right = left
            else:
                par.left = left

    def find(self, key) -> list[DataEntry]:
        curr_node = self.__root
        while curr_node is not None:
            if key < curr_node.data[0].columns[self.key_col]:
                curr_node = curr_node.left
            elif key > curr_node.data[0].columns[self.key_col]:
                curr_node = curr_node.right
            else:
                return curr_node.data
        return []

    def insert(self, data_entry: DataEntry) -> None | DataEntry:
        key = data_entry.columns[self.key_col]
        if self.__root is None:
            self.__root = RedBlackNode(data_entry, key, RedBlackNode.COLORS.BLACK.value)
            return None

        node = self.__root
        parent = None
        while node is not None:
            parent = node
            if key < node.data[0].columns[self.key_col]:
                node = node.left
            elif key > node.data[0].columns[self.key_col]:
                node = node.right
            else:
                node.data.append(data_entry)
                return None

        new_node = RedBlackNode(data_entry, key, RedBlackNode.COLORS.RED.value, parent=parent)
        if key < parent.data[0].columns[self.key_col]:
            parent.left = new_node
        else:
            parent.right = new_node

        self.__insert_fixup(new_node)
        return None

    def __insert_fixup(self, node: RedBlackNode):
        while node != self.__root and node.parent.color == RedBlackNode.COLORS.RED.value:
            parent = node.parent
            gp = parent.parent
            if parent == gp.left:
                uncle = gp.right
                if uncle is not None and uncle.color == RedBlackNode.COLORS.RED.value:
                    parent.color = RedBlackNode.COLORS.BLACK.value
                    uncle.color = RedBlackNode.COLORS.BLACK.value
                    gp.color = RedBlackNode.COLORS.RED.value
                    node = gp
                else:
                    if node == parent.right:
                        node = parent
                        self.__rotate_left(node)
                        parent = node.parent
                        gp = parent.parent
                    parent.color = RedBlackNode.COLORS.BLACK.value
                    gp.color = RedBlackNode.COLORS.RED.value
                    self.__rotate_right(gp)
            else:
                uncle = gp.left
                if uncle is not None and uncle.color == RedBlackNode.COLORS.RED.value:
                    parent.color = RedBlackNode.COLORS.BLACK.value
                    uncle.color = RedBlackNode.COLORS.BLACK.value
                    gp.color = RedBlackNode.COLORS.RED.value
                    node = gp
                else:
                    if node == parent.left:
                        node = parent
                        self.__rotate_right(node)
                        parent = node.parent
                        gp = parent.parent
                    parent.color = RedBlackNode.COLORS.BLACK.value
                    gp.color = RedBlackNode.COLORS.RED.value
                    self.__rotate_left(gp)
        self.__root.color = RedBlackNode.COLORS.BLACK.value

    def __transplant(self, u: RedBlackNode, v: RedBlackNode):
        if u.parent is None:
            self.__root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent
        u.parent = None

    def __find_node(self, key) -> RedBlackNode:
        current = self.__root
        while current is not None:
            if key < current.data[0].columns[self.key_col]:
                current = current.left
            elif key > current.data[0].columns[self.key_col]:
                current = current.right
            else:
                return current
        return None

    def __minimum(self, node: RedBlackNode) -> RedBlackNode:
        while node.left is not None:
            node = node.left
        return node

    def erase(self, key) -> list[DataEntry]:
        z = self.__find_node(key)
        if z is None:
            return []

        removed = z.data[:]
        y = z
        y_original_color = y.color

        if z.left is None:
            x = z.right
            parent = z.parent
            self.__transplant(z, z.right)
        elif z.right is None:
            x = z.left
            parent = z.parent
            self.__transplant(z, z.left)
        else:
            y = self.__minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                parent = y
            else:
                self.__transplant(y, y.right)
                y.right = z.right
                if y.right is not None:
                    y.right.parent = y
                parent = y.parent
            self.__transplant(z, y)
            y.left = z.left
            if y.left is not None:
                y.left.parent = y
            y.color = z.color

        if y_original_color == RedBlackNode.COLORS.BLACK.value:
            fix_parent = x.parent if x is not None else parent
            self.__delete_fixup(x, fix_parent)
        return removed

    def __delete_fixup(self, x: RedBlackNode, parent: RedBlackNode):
        while x != self.__root and self.__node_color(x) == RedBlackNode.COLORS.BLACK.value:
            if parent is not None and x == parent.left:
                w = parent.right
                if w is None:
                    x = parent
                    parent = x.parent
                    continue
                if (self.__node_color(getattr(w, 'left', None)) == RedBlackNode.COLORS.BLACK.value and
                    self.__node_color(getattr(w, 'right', None)) == RedBlackNode.COLORS.BLACK.value):
                    w.color = RedBlackNode.COLORS.RED.value
                    x = parent
                    parent = x.parent
                else:
                    if self.__node_color(getattr(w, 'right', None)) == RedBlackNode.COLORS.BLACK.value:
                        if getattr(w, 'left', None) is not None:
                            w.left.color = RedBlackNode.COLORS.BLACK.value
                        w.color = RedBlackNode.COLORS.RED.value
                        self.__rotate_right(w)
                        w = parent.right
                    w.color = parent.color
                    parent.color = RedBlackNode.COLORS.BLACK.value
                    if getattr(w, 'right', None) is not None:
                        w.right.color = RedBlackNode.COLORS.BLACK.value
                    self.__rotate_left(parent)
                    x = self.__root
                    break
            else:
                if parent is None:
                    break
                w = parent.left
                if w is None:
                    x = parent
                    parent = x.parent
                    continue
                if (self.__node_color(getattr(w, 'right', None)) == RedBlackNode.COLORS.BLACK.value and
                    self.__node_color(getattr(w, 'left', None)) == RedBlackNode.COLORS.BLACK.value):
                    w.color = RedBlackNode.COLORS.RED.value
                    x = parent
                    parent = x.parent
                else:
                    if self.__node_color(getattr(w, 'left', None)) == RedBlackNode.COLORS.BLACK.value:
                        if getattr(w, 'right', None) is not None:
                            w.right.color = RedBlackNode.COLORS.BLACK.value
                        w.color = RedBlackNode.COLORS.RED.value
                        self.__rotate_left(w)
                        w = parent.left
                    w.color = parent.color
                    parent.color = RedBlackNode.COLORS.BLACK.value
                    if getattr(w, 'left', None) is not None:
                        w.left.color = RedBlackNode.COLORS.BLACK.value
                    self.__rotate_right(parent)
                    x = self.__root
                    break
        if x is not None:
            x.color = RedBlackNode.COLORS.BLACK.value

    def inorder(self) -> list[DataEntry]:
        def inner(node: RedBlackNode) -> list[DataEntry]:
            if node is None:
                return []
            return inner(node.left) + [*node.data] + inner(node.right)
        return inner(self.__root)

    def preorder(self) -> list[DataEntry]:
        def inner(node: RedBlackNode) -> list[DataEntry]:
            if node is None:
                return []
            return [*node.data] + inner(node.left) + inner(node.right)
        return inner(self.__root)

    def postorder(self) -> list[DataEntry]:
        def inner(node: RedBlackNode) -> list[DataEntry]:
            if node is None:
                return []
            return inner(node.left) + inner(node.right) + [*node.data]
        return inner(self.__root)