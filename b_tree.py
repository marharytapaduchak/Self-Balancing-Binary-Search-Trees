import math
from abstract_tree import AbstractTree, AbstractTreeNode

class BTreeNode(AbstractTreeNode):
    def __init__(self, leaf):
        super().__init__(None)
        self.leaf = leaf
        self.children = []

class GeneralBTree(AbstractTree):
    def __init__(self, key_col, m: int):
        super().__init__(key_col)
        self.root = BTreeNode(True)
        self.t = math.ceil(m / 2)

    def _key_value(self, bucket):
        return bucket[0].columns[self.key_col]

    def find_for_insert(self, k, x=None):
        if hasattr(k, 'columns'):
            key_ = k.columns[self.key_col]
        else:
            key_ = k
        if x is not None:
            i = 0
            while i < len(x.data) and key_ > x.data[i][0].columns[self.key_col]:
                i += 1
            if i < len(x.data) and key_ == x.data[i][0].columns[self.key_col]:
                return x, i
            elif x.leaf:
                return None
            return self.find_for_insert(k, x.children[i])
        return self.find_for_insert(k, self.root)

    def insert(self, k):
        existing = self.find_for_insert(k)
        if existing is not None:
            existing[0].data[existing[1]].append(k)
            return

        if len(self.root.data) == (2 * self.t) - 1:
            temp = BTreeNode(False)
            prev_root = self.root
            self.root = temp
            temp.children = [prev_root]
            self.split_children(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(self.root, k)

    def insert_non_full(self, x, k):
        i = len(x.data) - 1
        if x.leaf:
            x.data.append(None)
            while i >= 0 and k.columns[self.key_col] < x.data[i][0].columns[self.key_col]:
                x.data[i + 1] = x.data[i]
                i -= 1
            x.data[i + 1] = [k]
        else:
            while i >= 0 and k.columns[self.key_col] < x.data[i][0].columns[self.key_col]:
                i -= 1
            i += 1
            if len(x.children[i].data) == (2 * self.t) - 1:
                self.split_children(x, i)
                if k.columns[self.key_col] > x.data[i][0].columns[self.key_col]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    def find(self, k, x=None):
        if x is not None:
            i = 0
            while i < len(x.data) and k > x.data[i][0].columns[self.key_col]:
                i += 1
            if i < len(x.data) and k == x.data[i][0].columns[self.key_col]:
                return x.data[i]
            elif x.leaf:
                return []
            return self.find(k, x.children[i])
        return self.find(k, self.root)

    def split_children(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.data.insert(i, y.data[t - 1])
        z.data = y.data[t:(2 * t)]
        y.data = y.data[:t - 1]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[:t]

    def erase(self, k):
        while self.find(k) != []:
            self.__delete(self.root, k)
        if len(self.root.data) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def __delete(self, x, k):
        idx = 0
        while idx < len(x.data) and k > x.data[idx][0].columns[self.key_col]:
            idx += 1

        if idx < len(x.data) and k == x.data[idx][0].columns[self.key_col]:
            if x.leaf:
                x.data.pop(idx)
            else:
                if len(x.children[idx].data) >= self.t:
                    pred = self.__get_predecessor(x, idx)
                    x.data[idx] = pred
                    self.__delete(x.children[idx], self._key_value(pred))
                elif len(x.children[idx + 1].data) >= self.t:
                    succ = self.__get_successor(x, idx)
                    x.data[idx] = succ
                    self.__delete(x.children[idx + 1], self._key_value(succ))
                else:
                    self.__merge(x, idx)
                    self.__delete(x.children[idx], k)
        else:
            if x.leaf:
                return

            flag = idx == len(x.data)
            if len(x.children[idx].data) == self.t - 1:
                self.__fill(x, idx)
            if flag and idx > len(x.data):
                idx = len(x.data)
            self.__delete(x.children[idx], k)

    def __fill(self, x, idx):
        if idx != 0 and len(x.children[idx - 1].data) >= self.t:
            self.__borrow_from_prev(x, idx)
        elif idx != len(x.children) - 1 and len(x.children[idx + 1].data) >= self.t:
            self.__borrow_from_next(x, idx)
        else:
            if idx != len(x.children) - 1:
                self.__merge(x, idx)
            else:
                self.__merge(x, idx - 1)

    def __borrow_from_prev(self, x, idx):
        child = x.children[idx]
        sibling = x.children[idx - 1]
        child.data.insert(0, x.data[idx - 1])
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())
        x.data[idx - 1] = sibling.data.pop()

    def __borrow_from_next(self, x, idx):
        child = x.children[idx]
        sibling = x.children[idx + 1]
        child.data.append(x.data[idx])
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))
        x.data[idx] = sibling.data.pop(0)

    def __merge(self, x, idx):
        child = x.children[idx]
        sibling = x.children[idx + 1]
        child.data.append(x.data[idx])
        child.data.extend(sibling.data)
        if not child.leaf:
            child.children.extend(sibling.children)
        x.data.pop(idx)
        x.children.pop(idx + 1)

    def __get_predecessor(self, x, idx):
        curr = x.children[idx]
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.data[-1]

    def __get_successor(self, x, idx):
        curr = x.children[idx + 1]
        while not curr.leaf:
            curr = curr.children[0]
        return curr.data[0]

    def inorder(self):
        def inorder_recursive(node, result):
            if node is None:
                return
            for i, bucket in enumerate(node.data):
                if i < len(node.children):
                    inorder_recursive(node.children[i], result)
                result.extend(bucket)
            if len(node.children) > len(node.data):
                inorder_recursive(node.children[-1], result)
        result = []
        inorder_recursive(self.root, result)
        return result

    def preorder(self):
        def preorder_recursive(node, result):
            if node is None:
                return
            for bucket in node.data:
                result.extend(bucket)
            for child in node.children:
                preorder_recursive(child, result)
        result = []
        preorder_recursive(self.root, result)
        return result

    def postorder(self):
        def postorder_recursive(node, result):
            if node is None:
                return
            for child in node.children:
                postorder_recursive(child, result)
            for bucket in node.data:
                result.extend(bucket)
        result = []
        postorder_recursive(self.root, result)
        return result


TwoThreeTree = lambda key_col : GeneralBTree(key_col, 3)
SmallBTree = lambda key_col : GeneralBTree(key_col, 10)
MediumBTree = lambda key_col : GeneralBTree(key_col, 35)
BigBTree = lambda key_col : GeneralBTree(key_col, 100)
