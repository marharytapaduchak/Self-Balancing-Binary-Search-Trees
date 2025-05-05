"""
Implements database table functional
"""

from data_entry import ColumnType, DataEntry

class DatabaseTable:
    """
    Represents database table
    """

    __columns_count_size = 2
    __enum_column_type_size = 1

    def __init__(self, tree, column_types):
        self.__tree = tree
        self.__column_types = column_types

    @classmethod
    def read_from_file(cls, tree_type, filename):
        """
        Creates tree from content in file
        """

        with open(filename, "rb") as file:
            content = file.read()

        columns_count = int.from_bytes(content[:DatabaseTable.__columns_count_size])
        key_col = int.from_bytes(content[DatabaseTable.__columns_count_size:DatabaseTable.__columns_count_size * 2])
        column_types = [
            int.from_bytes(content[
                DatabaseTable.__columns_count_size * 2 + DatabaseTable.__enum_column_type_size * i:
                DatabaseTable.__columns_count_size * 2 + DatabaseTable.__enum_column_type_size * (i + 1)
            ]) for i in range(columns_count)
        ]
        column_sizes = [ColumnType.get_size(column_type) for column_type in column_types]
        row_size = sum(column_sizes)
        rows_offset = DatabaseTable.__columns_count_size * 2 + DatabaseTable.__enum_column_type_size * columns_count

        tree = tree_type(key_col)

        for row_ind in range((len(content) - rows_offset) // row_size):
            data_entry_columns = []
            curr_offset = 0
            for column_size, column_type in zip(column_sizes, column_types):
                data_entry_columns.append(ColumnType.from_bytes(content[
                    rows_offset + row_ind * row_size + curr_offset:
                    rows_offset + row_ind * row_size + curr_offset + column_size
                ], column_type))
                curr_offset += column_size

            tree.insert(DataEntry(data_entry_columns))

        return cls(tree, column_types)

    def write_to_file(self, filename):
        """
        Writes to file from content in tree
        """

        total_res = bytes()

        total_res += len(self.__column_types).to_bytes(DatabaseTable.__columns_count_size, "big")
        total_res += self.__tree.key_col.to_bytes(DatabaseTable.__columns_count_size, "big")
        for column_type in self.__column_types:
            total_res += column_type.to_bytes(DatabaseTable.__enum_column_type_size, "big")

        for data_entry in self.__tree.inorder():
            for data_entry_col, col_type in zip(data_entry.columns, self.__column_types):
                total_res += ColumnType.to_bytes(data_entry_col, col_type)

        with open(filename, "wb") as file:
            file.write(total_res)

    @property
    def tree(self):
        """
        Gets tree data structure
        """

        return self.__tree
