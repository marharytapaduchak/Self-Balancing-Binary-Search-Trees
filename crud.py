"""
Database CRUD Operations Module

This module provides an interface for performing CRUD operations on various
tree-based database implementations. It supports multiple tree data structures
(AVL, B-Tree, Red-Black, Splay, Treap) and provides a simple SQL-like query interface.
"""

from typing import Any
from data_entry import ColumnType
from database import Database
from avl_tree import AVLTree
from b_tree import SmallBTree, MediumBTree, BigBTree, TwoThreeTree
from red_black_tree import RedBlackTree
from splay_tree import SplayTree
from treap import Treap


class QueryError(Exception):
    """Custom exception for query parsing and execution errors."""


def validate_table_name(table_name: str) -> str:
    """
    Validates a table name to ensure it contains only valid characters.

    Args:
        table_name: The name of the table to validate

    Returns:
        The validated table name

    Raises:
        QueryError: If the table name contains invalid characters
    """
    # Basic validation - could be expanded with more specific rules
    if not table_name or not isinstance(table_name, str):
        raise QueryError("Table name must be a non-empty string")

    # Check for invalid characters (basic sanitization)
    invalid_chars = "\"';\\/"
    if any(char in table_name for char in invalid_chars):
        raise QueryError(f"Table name contains invalid characters: {invalid_chars}")

    return table_name


def validate_column_names(column_names: list[str]) -> list[str]:
    """
    Validates a list of column names to ensure they contain only valid characters.

    Args:
        column_names: list of column names to validate

    Returns:
        The validated list of column names

    Raises:
        QueryError: If any column name contains invalid characters
    """
    if not column_names:
        raise QueryError("At least one column must be specified")

    validated_columns = []
    for col in column_names:
        if not isinstance(col, str):
            raise QueryError(f"Column name must be a string, got {type(col).__name__}")

        # Check for invalid characters (basic sanitization)
        invalid_chars = "\"';\\/"
        if any(char in col for char in invalid_chars):
            raise QueryError(f"Column name contains invalid characters: {invalid_chars}")

        validated_columns.append(col)

    return validated_columns


def validate_values(values: list) -> list:
    """
    Validates a list of values to be inserted into a table.

    Args:
        values: list of values to validate

    Returns:
        The validated list of values

    Raises:
        QueryError: If values are invalid
    """
    if not values:
        raise QueryError("No values provided for insertion")

    # Further validation could be added based on expected types
    return values


def parse_query(args: list[str], db: Database) -> Any | None:
    """
    Parses and executes a SQL-like query against the database.

    Args:
        args: list of query arguments/tokens
        db: Database instance to execute the query against

    Returns:
        Query results for SELECT queries, None for other operations

    Raises:
        QueryError: If the query syntax is invalid or execution fails
    """
    if not args:
        raise QueryError("Empty query")

    # Normalize arguments
    args = [s.lower().strip("(),") for s in args]
    args = [int(s) if s.isdigit() else s for s in args]

    try:
        match args[0]:
            case "select":
                # Find the FROM keyword to separate columns from table name
                try:
                    from_index = args.index("from")
                except ValueError:
                    raise QueryError("SELECT query must contain FROM keyword")

                if from_index == len(args) - 1:
                    raise QueryError("Table name missing after FROM")

                columns = args[1:from_index]
                table_name = args[from_index + 1]

                # Validate inputs
                validated_table_name = validate_table_name(table_name)
                validated_columns = validate_column_names(columns)
                if validated_columns == ["*"]:
                    validated_columns = db.get_table_columns_names(validated_table_name)

                # Execute query
                return db.select(validated_columns, validated_table_name)

            case "insert":
                # Check if the query has enough arguments
                if len(args) < 4:
                    raise QueryError("INSERT query is too short")

                # Validate the INSERT INTO syntax
                if args[1] != "into":
                    raise QueryError("INSERT query must have 'INTO' keyword")

                # Extract and validate table name
                table_name = args[2]
                if not table_name or not isinstance(table_name, str):
                    raise QueryError("Invalid table name")

                # Extract and validate values section
                values = args[3:]
                if not values:
                    raise QueryError("No values section in INSERT query")

                if values[0] != "values":
                    raise QueryError("INSERT query must have 'VALUES' keyword")

                # Extract the actual values to insert
                values = values[1:]
                if not values:
                    raise QueryError("No values provided for insertion")

                # Perform the insertion
                try:
                    db.insert(table_name, values)
                    return f"Successfully inserted data into {table_name}"
                except Exception as e:
                    raise QueryError(f"Failed to insert data: {str(e)}")
            case "create":
                # Check if the query has enough arguments
                if len(args) < 4:
                    raise QueryError("CREATE TABLE query is too short")

                # Validate the CREATE TABLE syntax
                if args[1] != "table":
                    raise QueryError("CREATE query must have 'TABLE' keyword")

                # Extract and validate table name
                table_name = args[2]
                validated_table_name = validate_table_name(table_name)

                # Extract and validate columns section
                columns = args[3:]
                if not columns or len(columns) % 2 != 0:
                    raise QueryError("CREATE TABLE query must have a valid column definition")
                column_names, column_types = columns[0::2], columns[1::2]

                # Extract column definitions
                columns = []
                for i in range(0, len(column_names)):
                    col_name = column_names[i]
                    col_type = column_types[i].upper()

                    # Validate column name and type
                    validated_col_name = validate_column_names([col_name])[0]
                    match col_type:
                        case "INT":
                            col_type = ColumnType.INT
                        case "LONG":
                            col_type = ColumnType.LONG
                        case "CHAR":
                            col_type = ColumnType.CHAR
                        case "SMALL_STRING":
                            col_type = ColumnType.SMALL_STRING
                        case "BIG_STRING":
                            col_type = ColumnType.BIG_STRING
                        case _:
                            raise QueryError(f"Unsupported column type: {col_type}")

                    columns.append((validated_col_name, col_type))

                # Create the table in the database
                db.create_table(validated_table_name, columns, 0)
                return f"Table {validated_table_name} created successfully"

            case _:
                raise QueryError(f"Unsupported command: {args[0]}")
    except Exception as e:
        # Convert any database errors to QueryError for consistent handling
        if not isinstance(e, QueryError):
            raise QueryError(f"Database error: {str(e)}")
        raise


def show_help():
    """Display help information for using the CRUD application."""
    return """
    Database CRUD Operations Tool

    Usage: python crud.py <database_name> <tree_type> [options]

    Tree Types:
      avl        - AVL Tree
      sb, small-btree - B-Tree with m = 10
      mb, medium-btree - B-Tree with m = 35
      bb, big-btree - B-Tree with m = 100
      b23, two-three-tree - B-Tree with m = 3 (two-three tree)
      rb, red-black - Red-Black Tree
      sp, splay  - Splay Tree
      tr, treap  - Treap

    Options:
      --help     - Show this help message
      -q <query> - Execute a SQL-like query
      -i         - Interactive mode

    Query Examples:
      SELECT col1 col2 FROM table_name
      INSERT INTO table_name VALUES val1 val2 val3
    """


def run_interactive_mode(db: Database):
    """
    Run the database in interactive mode, accepting queries from user input.

    Args:
        db: Database instance to execute queries against
    """
    print("Interactive mode. Type 'exit' to quit, 'help' for query syntax.")

    while True:
        try:
            user_input = input("Query> ").strip()

            if user_input.lower() == 'exit':
                print("Exiting interactive mode")
                break

            if user_input.lower() == 'help':
                print("""
                Available commands:
                  SELECT column1 column2 ... FROM table_name
                  INSERT INTO table_name VALUES value1 value2 ...
                  exit - Exit interactive mode
                  help - Show this help
                """)
                continue

            # Split the input and parse as a query
            query_parts = user_input.split()
            result = parse_query(query_parts, db)

            if result is not None:
                print("Result:", result)

        except QueryError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")


def main(argv: list[str]):
    """
    Main entry point for the CRUD application.

    Args:
        argv: Command line arguments
    """
    if len(argv) == 1:
        print("Please provide valid arguments.")
        print("Run with --help for usage information")
        return

    elif len(argv) < 3:
        if argv[1] == "-t" or argv[1] == "--test":
            run_test_mode()
            return
        elif argv[1] == "--help":
            print(show_help())
            return
        else:
            print("Too few arguments.")
            print("Run with --help for usage information")
            return

    # Extract database and tree information
    db_name, tree_name = argv[1:3]

    # Select tree implementation based on name
    try:
        TreeType = get_tree_class(tree_name)
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Run with --help to see supported tree types")
        return

    # Initialize database
    try:
        db = Database(TreeType, db_name)
    except Exception as e:
        print(f"Failed to initialize database: {str(e)}")
        return

    # Process remaining arguments
    argv = argv[3:]

    if len(argv) == 0:
        print("Too few arguments.")
        print("Run with --help for usage information")
    elif argv[0] == "--help":
        print(show_help())
    elif argv[0] == "-i":
        run_interactive_mode(db)
    elif argv[0] == "-q":
        if len(argv) < 2:
            print("Error: No query specified after -q")
            return

        argv = argv[1:]
        try:
            result = parse_query(argv, db)
            print(result)
        except QueryError as e:
            print(f"Query error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
    else:
        print(f"Unsupported argument: {argv[0]}")
        print("Run with --help for usage information")


def get_tree_class(tree_name: str):
    """
    Get the appropriate tree class based on the tree name.

    Args:
        tree_name: Name of the tree implementation to use

    Returns:
        Tree class to be used by the database

    Raises:
        ValueError: If the tree name is not recognized
    """
    match tree_name.lower():
        case "avl":
            return AVLTree
        case "sb" | "small-btree":
            return SmallBTree
        case "mb" | "medium-btree":
            return MediumBTree
        case "bb" | "big-btree":
            return BigBTree
        case "b23" | "two-three-tree":
            return TwoThreeTree
        case "rb" | "red-black":
            return RedBlackTree
        case "sp" | "splay":
            return SplayTree
        case "tr" | "treap":
            return Treap
        case _:
            raise ValueError(f"{tree_name} is not a valid tree type")


def run_test_mode():
    """Run the application in test mode to verify database functionality."""
    try:
        from data_entry import ColumnType, DataEntry

        print("Running in test mode...")

        # Initialize test database with Treap structure
        start_db = Database(Treap, "test_database")

        if not start_db.get_tables_names():
            print("Creating test tables...")

            # Create first test table
            start_db.create_table(
                "data",
                [["id", ColumnType.INT], ["name", ColumnType.SMALL_STRING]],
                0
            )

            # Create second test table with sample data
            start_db.create_table(
                "another_table",
                [["id", ColumnType.INT], ["name", ColumnType.SMALL_STRING], ["description", ColumnType.BIG_STRING]],
                0
            )

            # Insert test data
            start_db.get_table("another_table").tree.insert(DataEntry([0, "any_name", "htrhewnifuriuofvufyewbf"]))
            start_db.get_table("another_table").tree.insert(DataEntry([1, "another_name", "47878947fre74fr8787"]))
            start_db.get_table("another_table").tree.insert(DataEntry([2, "another_name1", "47878947fre74fr8787"]))
            start_db.get_table("another_table").tree.insert(DataEntry([3, "another_name2", "47878947fre74fr8787"]))

            # Save changes
            start_db.save()
            print("Test data created and saved.")

        # Load the database with a different tree structure to test compatibility
        loaded_db = Database(SplayTree, "test_database")
        print("Tables in database:", loaded_db.get_tables_names())
        print("Columns in 'another_table':", loaded_db.get_table_columns_names("another_table"))
        print("Data in 'another_table':", loaded_db.get_table("another_table").tree.inorder())

        # Test dropping a table
        loaded_db.drop_table("data")
        print("After dropping 'data' table:", loaded_db.get_tables_names())

        print("Test mode completed successfully")

    except Exception as e:
        print(f"Test mode failed: {str(e)}")


if __name__ == "__main__":
    import sys

    # Example usage:
    # python crud.py test_database rb -q select description id name from another_table
    # python crud.py test_database rb -q insert into another_table values 5 mama stranger
    argv = sys.argv
    main(argv)
