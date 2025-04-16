"""
Contains data entry representation
"""

class DataEntry:
    """
    Represents data entry (row) of database
    """

    def __init__(self, columns: list):
        self.columns = columns

    def __eq__(self, another):
        if len(self.columns) != len(another.columns):
            return False

        for i, val in enumerate(self.columns):
            if val != another.columns[i]:
                return False

        return True

    def __repr__(self):
        return f"<DataEntry: {repr(self.columns)}>"
