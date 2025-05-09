import math
from data_entry import DataEntry
from abstract_tree import AbstractTree, AbstractTreeNode

class BTreeNode:
    def __init__(self, leaf):
        self.leaf = leaf
        self.keys = []      # Кожен елемент — це список (бакет) об'єктів DataEntry з однаковим значенням ключа.
        self.children = []  # Список дітей

class GeneralBTree:
    def __init__(self, key_col, m: int):
        self.key_col = key_col
        self.root = BTreeNode(True)
        self.t = math.ceil(m / 2)  # мінімальна ступінь

    def _key_value(self, bucket):
        """Допоміжна функція для отримання значення ключа з бакету."""
        return bucket[0].columns[self.key_col]

    def find_for_insert(self, k, x=None):
        if hasattr(k, 'columns'):
            key_ = k.columns[self.key_col]
        else:
            key_ = k
        if x is not None:
            i = 0
            while i < len(x.keys) and key_ > x.keys[i][0].columns[self.key_col]:
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
            # Якщо ключ уже існує, додаємо до існуючого бакету.
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
            while i < len(x.keys) and key_ > x.keys[i][0].columns[self.key_col]:
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
        z.keys = y.keys[t:(2 * t)]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[:t]

    # ----------------------------------------------------------------------
    # Метод видалення: erase – забезпечує повне видалення всіх входжень заданого ключа.
    # Ми реалізуємо його, викликаючи _delete доти, поки метод find не поверне порожній список.
    def erase(self, k):
        while self.find(k) != []:
            self.__delete(self.root, k)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def __delete(self, x, k):
        idx = 0
        while idx < len(x.keys) and k > x.keys[idx][0].columns[self.key_col]:
            idx += 1

        if idx < len(x.keys) and k == x.keys[idx][0].columns[self.key_col]:
            if x.leaf:
                x.keys.pop(idx)
            else:
                if len(x.children[idx].keys) >= self.t:
                    pred = self.__get_predecessor(x, idx)
                    x.keys[idx] = pred
                    self.__delete(x.children[idx], self._key_value(pred))
                elif len(x.children[idx + 1].keys) >= self.t:
                    succ = self.__get_successor(x, idx)
                    x.keys[idx] = succ
                    self.__delete(x.children[idx + 1], self._key_value(succ))
                else:
                    self.__merge(x, idx)
                    self.__delete(x.children[idx], k)
        else:
            if x.leaf:
                return

            flag = idx == len(x.keys)
            if len(x.children[idx].keys) == self.t - 1:
                self.__fill(x, idx)
            if flag and idx > len(x.keys):
                idx = len(x.keys)
            self.__delete(x.children[idx], k)

    def __fill(self, x, idx):
        if idx != 0 and len(x.children[idx - 1].keys) >= self.t:
            self.__borrow_from_prev(x, idx)
        elif idx != len(x.children) - 1 and len(x.children[idx + 1].keys) >= self.t:
            self.__borrow_from_next(x, idx)
        else:
            if idx != len(x.children) - 1:
                self.__merge(x, idx)
            else:
                self.__merge(x, idx - 1)

    def __borrow_from_prev(self, x, idx):
        child = x.children[idx]
        sibling = x.children[idx - 1]
        child.keys.insert(0, x.keys[idx - 1])
        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())
        x.keys[idx - 1] = sibling.keys.pop()

    def __borrow_from_next(self, x, idx):
        child = x.children[idx]
        sibling = x.children[idx + 1]
        child.keys.append(x.keys[idx])
        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))
        x.keys[idx] = sibling.keys.pop(0)

    def __merge(self, x, idx):
        child = x.children[idx]
        sibling = x.children[idx + 1]
        child.keys.append(x.keys[idx])
        child.keys.extend(sibling.keys)
        if not child.leaf:
            child.children.extend(sibling.children)
        x.keys.pop(idx)
        x.children.pop(idx + 1)

    def __get_predecessor(self, x, idx):
        curr = x.children[idx]
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1]

    def __get_successor(self, x, idx):
        curr = x.children[idx + 1]
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0]

    def inorder(self):
        def inorder_recursive(node, result):
            if node is None:
                return
            for i, bucket in enumerate(node.keys):
                if i < len(node.children):
                    inorder_recursive(node.children[i], result)
                result.extend(bucket)
            if len(node.children) > len(node.keys):
                inorder_recursive(node.children[-1], result)
        result = []
        inorder_recursive(self.root, result)
        return result

    def preorder(self):
        def preorder_recursive(node, result):
            if node is None:
                return
            for bucket in node.keys:
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
            for bucket in node.keys:
                result.extend(bucket)
        result = []
        postorder_recursive(self.root, result)
        return result


TwoThreeTree = lambda key_col : GeneralBTree(key_col, 3)
SmallBTree = lambda key_col : GeneralBTree(key_col, 10)
MediumBTree = lambda key_col : GeneralBTree(key_col, 35)
BigBTree = lambda key_col : GeneralBTree(key_col, 100)
