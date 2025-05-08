"""
Implementing B-tree.
"""

import math

from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class BTreeNode:
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, key_col, m = 3):
        self.key_col = key_col
        self.root = BTreeNode(True)
        self.t = math.ceil(m / 2)

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
            self.split_children(temp, 0)
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
                self.split_children(x, i)
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

    def split_children(self, x, i):
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

    def erase(self, k, node=None):
        # A function to remove key k from the sub-tree rooted with this node
        if node is None:
            node = self.root

        idx = 0
        while idx < len(node.keys) and node.keys[idx][0].columns[self.key_col] < k:
            idx += 1

        if idx < len(node.keys) and node.keys[idx][0].columns[self.key_col] == k:
            if node.leaf:
                self.erase_from_leaf(idx, node)
            else:
                self.erase_from_non_leaf(idx, node)
        else:
            if node.leaf:
                return

            flag = idx == len(node.keys)
            if len(node.children[idx].keys) < self.t:
                self.fill(idx, node)

            if flag and idx > len(node.keys):
                self.erase(k, node.children[idx - 1])
            else:
                self.erase(k, node.children[idx])

    def erase_from_leaf(self, idx, node):
        # A function to remove the idx-th key from this node, which is a leaf node
        for i in range(idx + 1, len(node.keys)):
            node.keys[i - 1] = node.keys[i]
        node.keys.pop()
    
    def erase_from_non_leaf(self, idx, node):
        # A function to remove the idx-th key from this node, which is a non-leaf node
        k = node.keys[idx]

        if len(node.children[idx].keys) >= self.t:
            pred = self.get_pred(idx, node)
            node.keys[idx] = pred
            self.erase(pred, node.children[idx])
        elif len(node.children[idx].keys) >= self.t:
            succ = self.get_succ(idx, node)
            node.keys[idx] = succ
            self.erase(succ, node.children[idx + 1])
        else:
            print(1, idx)
            self.merge(idx, node)
            self.erase(k, node.children[idx])
    
    def get_pred(self, idx, node):
        # A function to get the predecessor of the key at the idx-th position in the node
        cur = node.children[idx]
        while not cur.leaf:
            cur = cur.children[-1]

        return cur.keys[-1][0].columns[self.key_col]

    def get_succ(self, idx, node):
        # A function to get the successor of the key at the idx-th position in the node
        cur = node.children[idx + 2]
        while not cur.leaf:
            cur = cur.children[0]

        return cur.keys[0][0].columns[self.key_col]
    
    def fill(self, idx, node):
        # A function to fill child C[idx] which has fewer than t-1 keys
        if idx != 0 and len(node.children[idx - 1].keys) >= self.t:
            self.borrow_from_prev(idx, node)
        elif idx != len(node.keys) and len(node.children[idx + 1].keys) >= self.t:
            self.borrow_from_next(idx, node)
        else:
            if idx != len(node.keys):
                self.merge(idx, node)
            else:
                self.merge(idx - 1, node)

    def borrow_from_prev(self, idx, node):
        # A function to borrow a key from C[idx-1] and insert it into C[idx]
        child, sibling = node.children[idx], node.children[idx - 1]

        child.keys.append(None)
        for i in range(len(child.keys) - 2, -1, -1):
            child.keys[i + 1] = child.keys[i]

        if not child.leaf:
            child.children.append(None)
            for i in range(len(child.keys) - 1, -1, -1):
                child.children[i + 1] = child.children[i]

        child.keys[0] = node.keys[idx - 1]

        if not child.leaf:
            child.children[0] = sibling.children[-1]

        node.keys[idx - 1] = sibling.keys[-1]

    def borrow_from_next(self, idx, node):
        # A function to borrow a key from C[idx+1] and place it in C[idx]
        child, sibling = node.children[idx], node.children[idx + 1]

        child.keys.append(node.keys[idx])

        if not child.leaf:
            child.children.append(sibling.children[0])

        node.keys[idx] = sibling.keys[0]

        for i in range(1, len(sibling.keys)):
            sibling.keys[i - 1] = sibling.keys[i]
        sibling.keys.pop()

        if not sibling.leaf:
            for i in range(1, len(sibling.children)):
                sibling.children[i - 1] = sibling.children[i]
            sibling.children.pop()

    def merge(self, idx, node):
        # A function to merge C[idx] with C[idx+1]
        child, sibling = node.children[idx], node.children[idx + 1]

        print(node.keys)
        print(idx)
        child.keys.append(node.keys[idx])

        for i in range(len(sibling.keys)):
            if i + self.t >= len(child.keys):
                child.keys.append(None)
            child.keys[i + self.t] = sibling.keys[i]

        if not child.leaf:
            for i in range(len(sibling.keys) + 1):
                if i + self.t >= len(child.children):
                    child.children.append(None)
                child.children[i + self.t] = sibling.children[i]

        for i in range(idx + 1, len(node.keys)):
            node.keys[i - 1] = node.keys[i]
        node.keys.pop()

        for i in range(idx + 2, len(node.keys) + 1):
            node.children[i - 1] = node.children[i]
        node.children.pop()

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
    B = BTree(0, 10)

    for key in range(10000):
        B.insert(DataEntry([key]))
    for key in range(0, 10000, 2):
        B.erase(key)

    print(B.inorder())
