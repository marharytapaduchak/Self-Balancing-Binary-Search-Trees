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

    def erase(self, k, x=None):
        pass
    #     if hasattr(k, 'columns'):
    #         k = k.columns[self.key_col]


    #     if x is None:
    #         x = self.root
    #     t = self.t
    #     i = 0
    #     while i < len(x.keys) and k > x.keys[i][0].columns[self.key_col]:
    #         i += 1
    #     if x.leaf:
    #         if i < len(x.keys) and x.keys[i][0].columns[self.key_col] == k:
    #             x.keys.pop(i)
    #             return
    #         return

    #     if i < len(x.keys) and x.keys[i][0].columns[self.key_col] == k:
    #         return self.erase_internal_node(x, k, i)
    #     elif len(x.children[i].keys) >= t:
    #         self.erase(x.children[i], k)
    #     else:
    #         if i != 0 and i + 2 < len(x.children):
    #             if len(x.children[i - 1].keys) >= t:
    #                 self.erase_sibling(x, i, i - 1)
    #             elif len(x.children[i + 1].keys) >= t:
    #                 self.erase_sibling(x, i, i + 1)
    #             else:
    #                 self.erase_merge(x, i, i + 1)
    #         elif i == 0:
    #             if len(x.children[i + 1].keys) >= t:
    #                 self.erase_sibling(x, i, i + 1)
    #             else:
    #                 self.erase_merge(x, i, i + 1)
    #         elif i + 1 == len(x.children):
    #             if len(x.children[i - 1].keys) >= t:
    #                 self.erase_sibling(x, i, i - 1)
    #             else:
    #                 self.erase_merge(x, i, i - 1)
    #         self.erase(x.children[i], k)

    # def erase_internal_node(self, x, k, i):
    #     t = self.t
    #     if x.leaf:
    #         if x.keys[i][0].columns[self.key_col] == k:
    #             x.keys.pop(i)
    #             return
    #         return

    #     if len(x.children[i].keys) >= t:
    #         # чи тут ок x.keys[i] = ????
    #         x.keys[i] = self.erase_predecessor(x.children[i])
    #         return
    #     elif len(x.children[i + 1].keys) >= t:
    #         x.keys[i] = self.erase_successor(x.children[i + 1])
    #         return
    #     else:
    #         self.erase_merge(x, i, i + 1)
    #         self.erase_internal_node(x.children[i], k, self.t - 1)

    # def erase_predecessor(self, x):
    #     if x.leaf:
    #         return x.pop()
    #     n = len(x.keys) - 1
    #     if len(x.children[n].keys) >= self.t:
    #         self.erase_sibling(x, n + 1, n)
    #     else:
    #         self.erase_merge(x, n, n + 1)
    #     self.erase_predecessor(x.children[n])
    
    # def erase_successor(self, x):
    #     if x.leaf:
    #         return x.keys.pop(0)
    #     if len(x.children[1].keys) >= self.t:
    #         self.erase_sibling(x, 0, 1)
    #     else:
    #         self.erase_merge(x, 0, 1)
    #     self.erase_successor(x.children[0])
    
    # def erase_merge(self, x, i, j):
    #     cnode = x.children[i]

    #     if j > i:
    #         rsnode = x.children[j]
    #         cnode.keys.append(x.keys[i])
    #         for k in range(len(rsnode.keys)):
    #             cnode.keys.append(rsnode.keys[k])
    #             if len(rsnode.children) > 0:
    #                 cnode.children.append(rsnode.children[k])
    #         if len(rsnode.children) > 0:
    #             cnode.children.append(rsnode.children.pop())
    #         new = cnode
    #         x.keys.pop(i)
    #         x.children.pop(j)
    #     else:
    #         lsnode = x.children[j]
    #         lsnode.keys.append(x.keys[j])
    #         for i in range(len(cnode.keys)):
    #             lsnode.keys.append(cnode.keys[i])
    #             if len(lsnode.children) > 0:
    #                 lsnode.children.append(cnode.children[i])
    #         if len(lsnode.children) > 0:
    #             lsnode.children.append(cnode.children.pop())
    #         new = lsnode
    #         x.keys.pop(j)
    #         x.children.pop(i)

    #     if x == self.root and len(x.keys) == 0:
    #         self.root = new
    
    # def erase_sibling(self, x, i, j):
    #     cnode = x.children[i]
    #     if i < j:
    #         rsnode = x.children[j]
    #         cnode.keys.append(x.keys[i])
    #         x.keys[i] = rsnode.keys[0]
    #         if len(rsnode.children) > 0:
    #             cnode.children.append(rsnode.children[0])
    #             rsnode.children.pop(0)
    #         rsnode.keys.pop(0)
    #     else:
    #         lsnode = x.children[j]
    #         cnode.keys.insert(0, x.keys[i - 1])
    #         x.keys[i - 1] = lsnode.keys.pop()
    #         if len(lsnode.children) > 0:
    #             cnode.children.insert(0, lsnode.children.pop())



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
