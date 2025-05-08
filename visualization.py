"""
Benchmark script to compare performance of different tree implementations.
Measures and visualizes execution time of key operations: insert, find, and erase.
"""

import time
import random
import matplotlib.pyplot as plt
import numpy as np

from data_entry import DataEntry
from abstract_tree import AbstractTree
from avl_tree import AVLTree
from splay_tree import SplayTree
from red_black_tree import RedBlackTree
# from b_tree import BTree
# from btree_2_3 import BTree_2_3

class TreeBenchmark:
    """
    Benchmark class to measure and compare performance of different tree implementations.
    """

    def __init__(self, tree_classes: AbstractTree):
        """
        Initialize benchmark with tree classes to test.
        
        Args:
            tree_classes: List of tree classes that inherit from AbstractTree
        """
        self.tree_classes = tree_classes
        self.tree_names = [tree_cls.__name__ for tree_cls in tree_classes]

    def generate_data_entries(self, count: int, cols_count: int) -> DataEntry:
        """
        Generate random data entries for testing.
        
        Args:
            count: Number of data entries to generate
            cols_count: Number of columns in each data entry
            
        Returns:
            List of random DataEntry objects
        """
        entries = []
        for _ in range(count):
            cols = [random.randint(0, count * 10) for _ in range(cols_count)]
            entries.append(DataEntry(cols))
        return entries

    def measure_insert_performance(self, sizes: int, cols_count: int = 5,
                                  repeats: int = 3):
        """
        Measure insert operation performance across different tree sizes.
        
        Args:
            sizes: List of different sizes to test
            cols_count: Number of columns in data entries
            repeats: Number of times to repeat each test for averaging
            
        Returns:
            Dictionary mapping tree names to lists of average execution times
        """
        results = {name: [] for name in self.tree_names}

        for size in sizes:
            print(f"Testing insert with size {size}...")

            for tree_idx, tree_class in enumerate(self.tree_classes):
                total_time = 0

                for _ in range(repeats):
                    data_entries = self.generate_data_entries(size, cols_count)

                    tree = tree_class(0)

                    start_time = time.time()
                    for entry in data_entries:
                        tree.insert(entry)
                    end_time = time.time()

                    total_time += (end_time - start_time)

                avg_time = total_time / repeats
                results[self.tree_names[tree_idx]].append(avg_time)

        return results

    def measure_find_performance(self, sizes: int, cols_count: int = 5,
                                search_count: int = 1000, repeats: int = 3):
        """
        Measure find operation performance across different tree sizes.
        
        Args:
            sizes: List of different sizes to test
            cols_count: Number of columns in data entries
            search_count: Number of search operations to perform
            repeats: Number of times to repeat each test for averaging
            
        Returns:
            Dictionary mapping tree names to lists of average execution times
        """
        results = {name: [] for name in self.tree_names}

        for size in sizes:
            print(f"Testing find with size {size}...")

            for tree_idx, tree_class in enumerate(self.tree_classes):
                total_time = 0

                for _ in range(repeats):
                    data_entries = self.generate_data_entries(size, cols_count)
                    tree = tree_class(0)
                    for entry in data_entries:
                        tree.insert(entry)

                    search_keys = [random.randint(0, size * 10) for _ in range(search_count)]

                    start_time = time.time()
                    for key in search_keys:
                        tree.find(key)
                    end_time = time.time()

                    total_time += (end_time - start_time)

                avg_time = (total_time / repeats) / search_count
                results[self.tree_names[tree_idx]].append(avg_time)

        return results

    def measure_erase_performance(self, sizes: int, cols_count: int = 5,
                                erase_ratio: float = 0.5, repeats: int = 3):
        """
        Measure erase operation performance across different tree sizes.
        
        Args:
            sizes: List of different sizes to test
            cols_count: Number of columns in data entries
            erase_ratio: Fraction of entries to erase
            repeats: Number of times to repeat each test for averaging
            
        Returns:
            Dictionary mapping tree names to lists of average execution times
        """
        results = {name: [] for name in self.tree_names}

        for size in sizes:
            print(f"Testing erase with size {size}...")

            for tree_idx, tree_class in enumerate(self.tree_classes):
                total_time = 0

                for _ in range(repeats):
                    data_entries = self.generate_data_entries(size, cols_count)
                    tree = tree_class(0)
                    for entry in data_entries:
                        tree.insert(entry)
                    erase_count = int(size * erase_ratio)
                    keys_to_erase = random.sample([entry.columns[0] for entry in data_entries], erase_count)

                    start_time = time.time()
                    for key in keys_to_erase:
                        tree.erase(key)
                    end_time = time.time()

                    total_time += (end_time - start_time)
                avg_time = (total_time / repeats) / erase_count
                results[self.tree_names[tree_idx]].append(avg_time)

        return results

    def run_all_benchmarks(self, sizes: int):
        """
        Run all benchmark tests.
        
        Args:
            sizes: List of different tree sizes to test
            
        Returns:
            Tuple of dictionaries with results for insert, find, and erase operations
        """
        insert_results = self.measure_insert_performance(sizes)
        find_results = self.measure_find_performance(sizes)
        erase_results = self.measure_erase_performance(sizes)

        return insert_results, find_results, erase_results

    def plot_results(self, sizes: int, insert_results,
                    find_results, erase_results,
                    save_path: str = None) -> None:
        """
        Plot benchmark results.
        
        Args:
            sizes: List of sizes tested
            insert_results: Dictionary of insert timing results
            find_results: Dictionary of find timing results
            erase_results: Dictionary of erase timing results
            save_path: If provided, save plot to this path instead of displaying
        """
        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        styles = ['-o', '--s', '-.^', ':d', '-x', '--+']

        for i, tree_name in enumerate(self.tree_names):
            style = styles[i % len(styles)]
            axs[0].plot(sizes, insert_results[tree_name], style, label=tree_name)
        axs[0].set_title('Insert Performance')
        axs[0].set_xlabel('Tree Size')
        axs[0].set_ylabel('Time (seconds)')
        axs[0].legend()
        axs[0].grid(True)

        for i, tree_name in enumerate(self.tree_names):
            style = styles[i % len(styles)]
            axs[1].plot(sizes, find_results[tree_name], style, label=tree_name)
        axs[1].set_title('Find Performance')
        axs[1].set_xlabel('Tree Size')
        axs[1].set_ylabel('Time (seconds per operation)')
        axs[1].legend()
        axs[1].grid(True)

        for i, tree_name in enumerate(self.tree_names):
            style = styles[i % len(styles)]
            axs[2].plot(sizes, erase_results[tree_name], style, label=tree_name)
        axs[2].set_title('Erase Performance')
        axs[2].set_xlabel('Tree Size')
        axs[2].set_ylabel('Time (seconds per operation)')
        axs[2].legend()
        axs[2].grid(True)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def plot_log_results(self, sizes, insert_results,
                         find_results, erase_results,
                         save_path: str = None) -> None:
        """
        Plot benchmark results with logarithmic scales for clearer comparison.
        
        Args:
            sizes: List of sizes tested
            insert_results: Dictionary of insert timing results
            find_results: Dictionary of find timing results
            erase_results: Dictionary of erase timing results
            save_path: If provided, save plot to this path instead of displaying
        """
        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        styles = ['-o', '--s', '-.^', ':d', '-x', '--+']

        for i, tree_name in enumerate(self.tree_names):
            style = styles[i % len(styles)]
            axs[0].loglog(sizes, insert_results[tree_name], style, label=tree_name)
        axs[0].set_title('Insert Performance (Log Scale)')
        axs[0].set_xlabel('Tree Size (log)')
        axs[0].set_ylabel('Time (seconds) (log)')
        axs[0].legend()
        axs[0].grid(True)

        for i, tree_name in enumerate(self.tree_names):
            style = styles[i % len(styles)]
            axs[1].loglog(sizes, find_results[tree_name], style, label=tree_name)
        axs[1].set_title('Find Performance (Log Scale)')
        axs[1].set_xlabel('Tree Size (log)')
        axs[1].set_ylabel('Time per operation (log)')
        axs[1].legend()
        axs[1].grid(True)

        for i, tree_name in enumerate(self.tree_names):
            style = styles[i % len(styles)]
            axs[2].loglog(sizes, erase_results[tree_name], style, label=tree_name)
        axs[2].set_title('Erase Performance (Log Scale)')
        axs[2].set_xlabel('Tree Size (log)')
        axs[2].set_ylabel('Time per operation (log)')
        axs[2].legend()
        axs[2].grid(True)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def plot_bar_comparison(self, sizes, insert_results,
                           find_results, erase_results,
                           size_index: int = -1, save_path: str = None) -> None:
        """
        Create bar chart comparing tree performance for a specific size.
        
        Args:
            sizes: List of sizes tested
            insert_results: Dictionary of insert timing results
            find_results: Dictionary of find timing results
            erase_results: Dictionary of erase timing results
            size_index: Index of the size to use for comparison (-1 means largest)
            save_path: If provided, save plot to this path instead of displaying
        """
        selected_size = sizes[size_index]

        insert_times = [insert_results[name][size_index] for name in self.tree_names]
        find_times = [find_results[name][size_index] for name in self.tree_names]
        erase_times = [erase_results[name][size_index] for name in self.tree_names]

        x = np.arange(len(self.tree_names))
        width = 0.25

        fig, ax = plt.subplots(figsize=(10, 6))
        insert_bars = ax.bar(x - width, insert_times, width, label='Insert')
        find_bars = ax.bar(x, find_times, width, label='Find')
        erase_bars = ax.bar(x + width, erase_times, width, label='Erase')

        ax.set_title(f'Tree Performance Comparison (Size = {selected_size})')
        ax.set_xlabel('Tree Implementation')
        ax.set_ylabel('Time (seconds)')
        ax.set_xticks(x)
        ax.set_xticklabels(self.tree_names)
        ax.legend()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()


def main():
    """
    Main function to run benchmark tests.
    """
    tree_classes = [
        AVLTree,
        SplayTree,
        RedBlackTree,
        # BTree
        # BTree_2_3
    ]

    benchmark = TreeBenchmark(tree_classes)

    sizes = [100, 500, 1000, 2000, 5000, 10000]

    print("Starting benchmarks...")
    insert_results, find_results, erase_results = benchmark.run_all_benchmarks(sizes)

    print("Generating plots...")
    benchmark.plot_results(sizes, insert_results, find_results, erase_results)
    benchmark.plot_log_results(sizes, insert_results, find_results, erase_results)
    benchmark.plot_bar_comparison(sizes, insert_results, find_results, erase_results)

    print("Benchmarks completed!")


if __name__ == "__main__":
    main()
