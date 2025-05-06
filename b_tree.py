"""
Implementing B-tree.
"""

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class BTreeNode:
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, key_col, t = 3):
        self.key_col = key_col
        self.root = BTreeNode(True)
        self.t = t

    def find_for_insert(self, k, x=None):
        if hasattr(k, 'columns'):
            key_ = k.columns[self.key_col]
        else:
            key_ = k
        if x is not None:
            i = 0
            while i < len(x.keys) and  key_ > x.keys[i][0].columns[self.key_col]:
                i += 1
            if i < len(x.keys) and key_ == x.keys[i][0].columns[self.key_col]:
                return x, i
            elif x.leaf:
                return None
            return self.find_for_insert(k, x.children[i])
        return self.find_for_insert(k, self.root)

    def insert(self, k):
        existing = self.find_for_insert(k)
        if existing is not None:
           existing[0].keys[existing[1]].append(k)
           return

        if len(self.root.keys) == (2 * self.t) - 1:
            temp = BTreeNode(False)
            prev_root = self.root
            self.root = temp
            temp.children = [prev_root]
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(self.root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k.columns[self.key_col] < x.keys[i][0].columns[self.key_col]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = [k]
        else:
            while i >= 0 and k.columns[self.key_col] < x.keys[i][0].columns[self.key_col]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k.columns[self.key_col] > x.keys[i][0].columns[self.key_col]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    def find(self, k, x=None):
        if hasattr(k, 'columns'):
            key_ = k.columns[self.key_col]
        else:
            key_ = k
        if x is not None:
            i = 0
            while i < len(x.keys) and  key_ > x.keys[i][0].columns[self.key_col]:
                i += 1
            if i < len(x.keys) and key_ == x.keys[i][0].columns[self.key_col]:
                return x.keys[i]
            elif x.leaf:
                return []
            return self.find(k, x.children[i])
        return self.find(k, self.root)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:t*2]
        y.keys = y.keys[:t-1]
        if not y.leaf:
            z.children = y.children[t:t*2]
            y.children = y.children[:t]
    
    def erase(self):
        pass

    def print_tree(self, x, l=0):
        print("Level ", l, " ", len(x.keys), end=":")
        for i in x.keys:
            print(i, end=" ")
        print()
        l += 1
        if len(x.children) > 0:
            for i in x.children:
                self.print_tree(i, l)

    def inorder(self):
        def inorder_recursive(node, result):
            if node is None:
                return

            for i, k in enumerate(node.keys):
                if i < len(node.children):
                    inorder_recursive(node.children[i], result)
                result += k
            if len(node.children) > len(node.keys):
                inorder_recursive(node.children[-1], result)

        result = []

        inorder_recursive(self.root, result)

        return result

    def preorder(self):
        def preorder_recursive(node, result):
            if node is None:
                return

            for same_k in node.keys:
                result += same_k

            for c in node.children:
                preorder_recursive(c, result)

        result = []

        preorder_recursive(self.root, result)

        return result

    def postorder(self):
        def postorder_recursive(node, result):
            if node is None:
                return

            for c in node.children:
                postorder_recursive(c, result)

            for same_k in node.keys:
                result += same_k

        result = []

        postorder_recursive(self.root, result)

        return result


if __name__ == "__main__":
    B = BTree(0, 30000)

    keys = [
        DataEntry([10]),
        DataEntry([50]),
        DataEntry([60]),
        DataEntry([20]),
        DataEntry([40]),
        DataEntry([61]),
        DataEntry([21]),
        DataEntry([41]),
        DataEntry([61]),
        DataEntry([21]),
        DataEntry([41]),
        DataEntry([50]),
        DataEntry([60]),
        DataEntry([20]),
        DataEntry([40]),
        DataEntry([61]),
        DataEntry([21]),
        DataEntry([41]),
        DataEntry([61]),
        DataEntry([21]),
        DataEntry([41])
    ]

    for key in keys:
        B.insert(key)

    print(B.inorder())
