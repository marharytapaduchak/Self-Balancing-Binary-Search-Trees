"""
Unit tests to check trees implementations correctness
"""

import unittest
import random

from data_entry import DataEntry
from unbalanced_tree import UnbalancedTree
from splay_tree import SplayTree
from avl_tree import AVLTree
from treap import Treap
from red_black_tree import RedBlackTree
from b_tree import TwoThreeTree, SmallBTree, MediumBTree, BigBTree

TREES_FOR_TEST = [
    UnbalancedTree,
    SplayTree,
    AVLTree,
    Treap,
    RedBlackTree,
    TwoThreeTree,
    SmallBTree,
    MediumBTree,
    BigBTree
]

class TestTree(unittest.TestCase):
    """
    Tests trees implementations correctness
    """

    def test_insert_and_inorder(self):
        """
        Tests methods insert and inorder
        """

        tests_count = 10
        test_size = 100

        for TreeType in TREES_FOR_TEST:
            for _ in range(tests_count):
                values = []
                for _ in range(test_size):
                    data_entry = DataEntry(list(range(test_size)))
                    random.shuffle(data_entry.columns)
                    values.append(data_entry)

                key_col = random.randint(0, test_size - 1)

                sorted_values = values.copy()
                sorted_values.sort(key=lambda data : data.columns[key_col])

                tree = TreeType(key_col)

                curr_values = []

                for value in values:
                    tree.insert(value)

                    new_curr_values = []
                    inserted = False
                    for val in curr_values:
                        if not inserted and value.columns[key_col] < val.columns[key_col]:
                            new_curr_values.append(value)
                            inserted = True
                        new_curr_values.append(val)
                    if not inserted:
                        new_curr_values.append(value)
                    curr_values = new_curr_values

                    self.assertListEqual(tree.inorder(), curr_values)

    def test_find(self):
        """
        Tests method find
        """

        tests_count = 10
        test_size = 100

        for TreeType in TREES_FOR_TEST:
            for _ in range(tests_count):
                values = []
                for _ in range(test_size):
                    data_entry = DataEntry(list(range(test_size)))
                    random.shuffle(data_entry.columns)
                    values.append(data_entry)

                key_col = random.randint(0, test_size - 1)

                vals_for_key_cols = {}
                for value in values:
                    if value.columns[key_col] in vals_for_key_cols:
                        vals_for_key_cols[value.columns[key_col]].append(value)
                    else:
                        vals_for_key_cols[value.columns[key_col]] = [value]

                tree = TreeType(key_col)
                for value in values:
                    tree.insert(value)

                for key_to_find in range(test_size):
                    self.assertListEqual(tree.find(key_to_find), vals_for_key_cols.get(key_to_find, []))

    def test_erase(self):
        """
        Tests method erase
        """

        tests_count = 10
        test_size = 10

        for TreeType in TREES_FOR_TEST:
            for _ in range(tests_count):
                values = []

                for _ in range(test_size):
                    data_entry = DataEntry(list(range(test_size)))
                    random.shuffle(data_entry.columns)
                    values.append(data_entry)

                key_col = random.randint(0, test_size - 1)

                sorted_values = values.copy()
                sorted_values.sort(key=lambda data : data.columns[key_col])

                tree = TreeType(key_col)
                for value in values:
                    tree.insert(value)

                keys_to_erase = list(range(test_size))
                random.shuffle(keys_to_erase)

                for key_to_erase in keys_to_erase:
                    tree.erase(key_to_erase)

                    new_sorted_values = []
                    for val in sorted_values:
                        if val.columns[key_col] != key_to_erase:
                            new_sorted_values.append(val)
                    sorted_values = new_sorted_values

                    self.assertListEqual(tree.inorder(), sorted_values)

    def test_preorder_and_postorder(self):
        """
        Tests methods preorder and postorder
        Unlike inorder, preorder and postorder are implementation-defined for different tree types,
        so it is only possible to test data entries presence and absence, not their order.
        Does not work if inorder or insert fails
        """

        tests_count = 10
        test_size = 100

        for TreeType in TREES_FOR_TEST:
            for _ in range(tests_count):
                values = []
                for _ in range(test_size):
                    data_entry = DataEntry(list(range(test_size)))
                    random.shuffle(data_entry.columns)
                    values.append(data_entry)

                key_col = random.randint(0, test_size - 1)

                tree = TreeType(key_col)

                curr_values = []

                for value in values:
                    tree.insert(value)

                    new_curr_values = []
                    inserted = False
                    for val in curr_values:
                        if not inserted and value.columns[key_col] < val.columns[key_col]:
                            new_curr_values.append(value)
                            inserted = True
                        new_curr_values.append(val)
                    if not inserted:
                        new_curr_values.append(value)
                    curr_values = new_curr_values

                    sorted_preorder = tree.preorder()
                    sorted_preorder.sort(key=lambda data : data.columns[key_col])
                    self.assertListEqual(tree.inorder(), sorted_preorder)

                    sorted_postorder = tree.postorder()
                    sorted_postorder.sort(key=lambda data : data.columns[key_col])
                    self.assertListEqual(tree.inorder(), sorted_postorder)

if __name__ == "__main__":
    unittest.main(verbosity=2)
