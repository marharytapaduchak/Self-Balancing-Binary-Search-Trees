"""
Implements database functional
"""

import os
import shutil
from database_table import DatabaseTable

class Database:
    """
    Represents database
    """

    __config_file = "db_data.cnf"

    def __init__(self, tree_type, db_folder_path: str):
        self.__db_folder_path = db_folder_path
        self.__tree_type = tree_type
        self.__tables = {}

        if os.path.exists(f"{db_folder_path}/{Database.__config_file}"):
            with open(f"{db_folder_path}/{Database.__config_file}", "rb") as file:
                all_table_data = file.read().decode("utf-8")

            if not all_table_data:
                return

            for table_data in all_table_data.split("\n"):
                column_names = table_data.split(" ")
                table_name = column_names.pop(0)

                self.__tables[table_name] = (
                    column_names,
                    DatabaseTable.read_from_file(tree_type, f"{db_folder_path}/{table_name}")
                )

    def save(self):
        """
        Save database
        """

        if os.path.exists(self.__db_folder_path):
            shutil.rmtree(self.__db_folder_path)

        config_data = ""

        for table_name, table in self.__tables.items():
            config_data += table_name + " "
            config_data += " ".join(table[0]) + "\n"

        os.mkdir(self.__db_folder_path)
        with open(f"{self.__db_folder_path}/{Database.__config_file}", "wb") as file:
            file.write(config_data[:-1].encode("utf-8"))

        for table_name, table in self.__tables.items():
            table[1].write_to_file(f"{self.__db_folder_path}/{table_name}")

    def create_table(self, table_name: str, columns: list[tuple[str, int]], key_col: int):
        """
        Creates database table
        """

        if table_name in self.__tables:
            raise RuntimeError(f"Table with name \"{table_name}\" already exists.")

        self.__tables[table_name] = (
            [column[0] for column in columns],
            DatabaseTable(self.__tree_type(key_col), [column[1] for column in columns])
        )

    def drop_table(self, table_name: str):
        """
        Deletes table from database
        """

        if table_name not in self.__tables:
            raise RuntimeError(f"Table with name \"{table_name}\" does not exist.")

        del self.__tables[table_name]

    def drop(self):
        """
        Deletes database both from memory and filesystem.
        This will delete database from filesystem immmediately, even if save() is not called
        """

        self.__tables = {}
        if os.path.exists(self.__db_folder_path):
            shutil.rmtree(self.__db_folder_path)

    def get_tables_names(self) -> list[str]:
        """
        Gets database tables names
        """

        return list(self.__tables.keys())

    def get_table_columns_names(self, table_name) -> list[str]:
        """
        Gets database table columns names
        """

        if table_name not in self.__tables:
            raise RuntimeError(f"Table with name \"{table_name}\" does not exist.")

        return self.__tables[table_name][0]

    def get_table(self, table_name):
        """
        Gets database table
        """

        if table_name not in self.__tables:
            raise RuntimeError(f"Table with name \"{table_name}\" does not exist.")

        return self.__tables[table_name][1]

    def select(self, columns: list[str], table_name: str):
        cols_list = self.get_table_columns_names(table_name)
        cols_ind = [cols_list.index(col) for col in columns]

        selected = self.get_table(table_name).tree.inorder()
        return [[s.columns[i] for i in cols_ind] for s in selected]

if __name__ == "__main__":
    from treap import Treap
    from splay_tree import SplayTree
    from data_entry import ColumnType, DataEntry

    start_db = Database(Treap, "test_database")

    if not start_db.get_tables_names():
        start_db.create_table(
            "data",
            [["id", ColumnType.INT], ["name", ColumnType.SMALL_STRING]],
            0
        )
        start_db.create_table(
            "another_table",
            [["id", ColumnType.INT], ["name", ColumnType.SMALL_STRING], ["description", ColumnType.BIG_STRING]],
            0
        )
        start_db.get_table("another_table").tree.insert(DataEntry([0, "any_name", "htrhewnifuriuofvufyewbf"]))
        start_db.get_table("another_table").tree.insert(DataEntry([1, "another_name", "47878947fre74fr8787"]))
        start_db.save()

    loaded_db = Database(SplayTree, "test_database")
    print(loaded_db.get_tables_names())
    print(loaded_db.get_table_columns_names("another_table"))
    print(loaded_db.get_table("another_table").tree.inorder())
    loaded_db.drop_table("data")
    print(loaded_db.get_tables_names())
    loaded_db.drop()
    print(loaded_db.get_tables_names())
