"""
Contains base class of tree and node
"""

from abc import ABC, abstractmethod

from data_entry import DataEntry

class AbstractTreeNode(ABC):
    """
    Represents tree base node
    """

    def __init__(self, data_entry: DataEntry):
        self.data = [data_entry]


class AbstractTree(ABC):
    """
    Base class of tree with required methods for database queries
    """

    def __init__(self, key_col: int):
        self.__key_col = key_col

    @property
    def key_col(self):
        """
        Getter for key column index
        """

        return self.__key_col

    @abstractmethod
    def insert(self, data_entry: DataEntry) -> None:
        """
        Inserts data entry into tree
        """

    @abstractmethod
    def find(self, key) -> list[DataEntry]:
        """
        Searches for all entries from tree by key
        """

    @abstractmethod
    def erase(self, key) -> None:
        """
        Erases data entries from tree by key
        """

    @abstractmethod
    def inorder(self) -> list[DataEntry]:
        """
        In-order tree walk
        """

    @abstractmethod
    def preorder(self) -> list[DataEntry]:
        """
        Pre-order tree walk
        """

    @abstractmethod
    def postorder(self) -> list[DataEntry]:
        """
        Post-order tree walk
        """
