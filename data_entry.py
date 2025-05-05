"""
Contains data entry representation
"""

class ColumnType:
    """
    Represents different types of database columns
    """

    INT = 0
    LONG = 1
    CHAR = 2
    SMALL_STRING = 3
    BIG_STRING = 4

    @staticmethod
    def get_size(column_type: int):
        """
        Gets size in bytes of type
        """

        match column_type:
            case ColumnType.INT:
                return 4
            case ColumnType.LONG:
                return 8
            case ColumnType.CHAR:
                return 1
            case ColumnType.SMALL_STRING:
                return 16
            case ColumnType.BIG_STRING:
                return 256
            case _:
                return -1

    @staticmethod
    def to_bytes(column_data, column_type: int) -> bytes:
        """
        Converts typed object into raw bytes
        """

        match column_type:
            case ColumnType.INT | ColumnType.LONG:
                return column_data.to_bytes(ColumnType.get_size(column_type), "big")
            case ColumnType.CHAR | ColumnType.SMALL_STRING | ColumnType.BIG_STRING:
                col_size = ColumnType.get_size(column_type)
                encoded = column_data[:col_size].encode("utf-8")
                return encoded + b"\0" * (col_size - len(encoded))
            case _:
                return bytes()

    @staticmethod
    def from_bytes(column_data: bytes, column_type: int):
        """
        Converts raw bytes into typed object
        """

        match column_type:
            case ColumnType.INT | ColumnType.LONG:
                return int.from_bytes(column_data)
            case ColumnType.CHAR | ColumnType.SMALL_STRING | ColumnType.BIG_STRING:
                return column_data.rstrip(b"\x00").decode("utf-8")
            case _:
                return None


class DataEntry:
    """
    Represents data entry (row) of database
    """

    def __init__(self, columns: list):
        self.columns = columns

    def __eq__(self, another: "DataEntry"):
        if len(self.columns) != len(another.columns):
            return False

        for i, val in enumerate(self.columns):
            if val != another.columns[i]:
                return False

        return True

    def __repr__(self):
        return f"<DataEntry: {repr(self.columns)}>"
