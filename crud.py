from database import Database
from avl_tree import AVLTree
from b_tree import BTree
from red_black_tree import RedBlackTree
from splay_tree import SplayTree
from treap import Treap



def parse_query(args: list[str], db: Database):
    args = [s.lower() for s in args]
    match args[0]:
        case "select":
            i = 1
            columns = []
            while i < len(args):
                if args[i] == "from":
                    break
                columns.append(args[i])
                i += 1
            else:
                raise ValueError("Invalid query")

            table_name = args[i+1]
            return db.select(columns, table_name)
        case "insert":
            if args[1] != "into":
                raise ValueError("Invalid query")

            table_name = args[2]
            columns = args[3:]

        case _:
            raise ValueError("Not supported parameters")



if __name__ == "__main__":
    import sys


    argv = sys.argv

    if len(argv) == 1:
        print("Please provide valid arguments.")
        print("or run with --help")
    elif len(argv) < 3:
        if argv[1] == "-t" or argv[1] == "--test":
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
        else:
            print("Too few arguments.")
            print("run with --help")

    db_name, tree_name = argv[1:2+1]
    TreeType = None
    match tree_name.lower():
        case "avl":
            TreeType = AVLTree
        case "b"|"btree":
            TreeType = BTree
        case "rb"|"red-black":
            TreeType = RedBlackTree
        case "sp"|"splay":
            TreeType = SplayTree
        case "tr"|"treap":
            TreeType = Treap
        case _:
            raise ValueError(f"{tree_name} is not a valid tree type")

    db = Database(TreeType, db_name)
    argv = argv[3:]

    if len(argv) == 0:
        print("Too few arguments.")
        print("run with --help")
    elif argv[0] == "--help":
        #TODO
        print("""
            There should be help for you
              """)
    elif argv[0] == "-i":
        #TODO
        ...

    elif argv[0] == "-q":
        argv = argv[1:]

        try:
            print(parse_query(argv, db))
        except Exception as e:
            print("Invalid query")
            #DEBUG TODO
            print(e)
    else:
        raise ValueError("""unsupported arguments
                         run with --help""")